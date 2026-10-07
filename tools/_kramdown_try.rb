# frozen_string_literal: true
require "kramdown"
src = File.read(ARGV[0], encoding: "UTF-8")
html = Kramdown::Document.new(src, input: "kramdown", hard_wrap: false).to_html
File.write(ARGV[1], html, encoding: "UTF-8")
warn "ok bytes=#{html.bytesize}"
