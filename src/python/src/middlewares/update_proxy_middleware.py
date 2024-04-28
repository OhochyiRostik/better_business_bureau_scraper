from scrapy import Request


class UpdateProxyMiddleware:
    def process_response(self, request, response, spider):
        if (response.status == 403 or response.status == 502) and 'proxy' in request.meta:
            # Remove the proxy from the request meta to force a retry without the proxy
            del request.meta['proxy']
            # Retry the request without the proxy
            return request
        return response
