# frozen_string_literal: true
# #region agent log
require "json"

Jekyll::Hooks.register :site, :post_write do |site|
  log_path = File.join(site.source, "debug-17d49f.log")
  File.open(log_path, "a") do |f|
    p09_keys = site.tags.keys.select { |k| k.to_s.downcase == "p09" }
    p09_data = p09_keys.map { |k| { "key" => k, "count" => site.tags[k].size } }
    f.puts(JSON.generate({
      "sessionId" => "17d49f",
      "runId" => "jekyll-post-write",
      "hypothesisId" => "B",
      "location" => "_plugins/debug_vazatoga_permalinks.rb:post_write",
      "message" => "p09 tag keys after normalize",
      "data" => { "keys" => p09_data, "key_count" => p09_keys.size },
      "timestamp" => (Time.now.to_f * 1000).to_i
    }))
    tracked = %w[T-207 T-255 T-256 T-257 T-258 T-259 T-260 T-261 T-262]
    site.posts.docs.each do |post|
      corpus = post.data["id_corpus"].to_s
      next unless tracked.include?(corpus)
      dated = post.url.to_s.include?("2026-08-20") || post.url.to_s.include?("2026-05-29")
      payload = {
        "sessionId" => "17d49f",
        "runId" => "jekyll-post-write",
        "hypothesisId" => "A",
        "location" => "_plugins/debug_vazatoga_permalinks.rb:post_write",
        "message" => "resolved post url",
        "data" => {
          "id_corpus" => corpus,
          "timeline_id" => post.data["timeline_id"],
          "url" => post.url,
          "basename" => post.basename,
          "permalink_fm" => post.data["permalink"],
          "url_includes_date_prefix" => dated
        },
        "timestamp" => (Time.now.to_f * 1000).to_i
      }
      f.puts(JSON.generate(payload))
    end
  end
end
# #endregion
