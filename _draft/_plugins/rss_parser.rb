require 'feedjira'
require 'net/http'
require 'uri'
require 'nokogiri'  # Para parsing HTML
require 'open-uri'  # Para fetch de páginas

module Jekyll
  class RSSParser < Generator
    def generate(site)
      feed_url = 'https://geoengineeringwatch.org/feed/'  # URL do feed

      def fetch_content(url, max_redirects = 5)
        raise ArgumentError, 'Muitos redirecionamentos' if max_redirects == 0
        uri = URI(url)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = (uri.scheme == 'https')
        request = Net::HTTP::Get.new(uri)
        request['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        response = http.request(request)

        if [301, 302].include?(response.code.to_i)
          location = response['location']
          Jekyll.logger.info "Redirecionando para: #{location}"
          return fetch_content(location, max_redirects - 1)
        end

        unless response.code == '200'
          raise "Erro HTTP: #{response.code} - #{response.message}"
        end

        unless response.content_type.include?('xml') || response.content_type.include?('rss') || response.content_type.include?('atom')
          raise "Tipo de conteúdo inválido: #{response.content_type}"
        end

        response.body
      end

      def fetch_full_details(page_url)
        begin
          doc = Nokogiri::HTML(URI.open(page_url, 'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'))
          content = doc.css('.article-content').inner_html.strip
          content.empty? ? nil : content
        rescue => e
          Jekyll.logger.error "Erro ao fetch detalhes de #{page_url}: #{e.message}"
          nil
        end
      end

      begin
        content = fetch_content(feed_url)
        feed = Feedjira.parse(content)
        rss_items = feed.entries.map do |entry|
          full_details = fetch_full_details(entry.url)
          body = ""
          body += "#{entry.summary}\n\n" if entry.summary
          body += full_details if full_details
          body = entry.summary if body.empty?

          {
            'title' => entry.title,
            'url' => entry.url,
            'published' => entry.published,
            'summary' => entry.summary,
            'content' => body  # Corpo enriquecido com detalhes
          }
        end
        site.data['rss_items'] = rss_items
        Jekyll.logger.info "RSS importado: #{rss_items.size} itens processados."
      rescue Feedjira::NoParserAvailable => e
        Jekyll.logger.error "Erro de parsing: #{e.message}. Trecho do conteúdo:"
        Jekyll.logger.error content[0..500]
      rescue => e
        Jekyll.logger.error "Erro no plugin RSS: #{e.message}"
      end
    end
  end
end
