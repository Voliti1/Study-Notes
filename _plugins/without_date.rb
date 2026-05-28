module Jekyll
  class PostReader
    def read_posts(dir)
      read_publishable(dir, "_posts", Document::DATELESS_FILENAME_MATCHER)
    end

    def read_drafts(dir)
      read_publishable(dir, "_drafts", Document::DATELESS_FILENAME_MATCHER)
    end
  end

  class Document
    def parse_date_and_slug(basename)
      if basename =~ DATE_FILENAME_MATCHER
        self.date = Utils.parse_date("#{Regexp.last_match(1)}-#{Regexp.last_match(2)}-#{Regexp.last_match(3)}", "Document date")
        self.slug = Regexp.last_match(4)
        self.ext = Regexp.last_match(5)
      elsif basename =~ DATELESS_FILENAME_MATCHER
        self.date = File.exist?(path) ? File.mtime(path) : Time.now
        self.slug = Regexp.last_match(1)
        self.ext = Regexp.last_match(2)
      else
        raise ArgumentError, "Document '#{relative_path}' does not have a valid filename."
      end
    end
  end
end
