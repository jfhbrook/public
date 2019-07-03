import urllib


class UrlRegistry:
    def __init__(self, config, applications):
        # Nice and sweet...for now.
        self.lookup = dict(**config.urls)
        self.applications = applications

    def get_application_by_url(self, url):
        parsed = urllib.parse.urlparse(url)

        return self.get_application_by_scheme(parsed.scheme)

    def get_application_by_scheme(self, scheme):
        if scheme not in self.lookup:
            return None

        key = self.lookup[scheme]

        return self.applications.entries.get(key)
