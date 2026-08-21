# frozen_string_literal: true

# Jekyll treats "p09" and "P09" as different tags, but jekyll-archives
# slugifies both to /tags/p09/. The second write overwrites the first,
# so the public page can show 1 post while /tags/ lists 40.
Jekyll::Hooks.register :documents, :post_init do |doc|
  next unless doc.collection&.label == "posts"

  tags = doc.data["tags"]
  if tags.is_a?(Array)
    doc.data["tags"] = tags.map { |t| t.to_s.strip.downcase }
  elsif tags.is_a?(String)
    doc.data["tags"] = tags.split(/[,\s]+/).reject(&:empty?).map { |t| t.strip.downcase }
  end
end
