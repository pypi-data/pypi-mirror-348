from singer_sdk.pagination import BaseHATEOASPaginator

class FreshservicePaginator(BaseHATEOASPaginator):
    """Gets the next URL from the Links header in the response. This is standard HATEOAS and the Meltano SDK supports it"""
    def get_next_url(self, response):
        next_page_url = response.links.get('next', {}).get('url')
        return next_page_url
