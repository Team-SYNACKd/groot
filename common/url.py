from urllib.parse import urlparse

class URL:
    def __init__(self, url: str) -> None:
        parsed = urlparse(url)

        self.scheme = parsed.scheme
        self.authority = parsed.netloc
        if ":" in parsed.netloc:
            self.host, port_str = parsed.netloc.split(":")
            self.port = int(port_str)
        else:
            self.host = parsed.netloc
            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443
            else: # NOTE: this is set to talk to our HTTP server only
                self.port = 8000

        if parsed.path:
            self.full_path = parsed.path
        else:
            self.full_path = '/'
        if parsed.query:
            self.full_path += "?" + parsed.query