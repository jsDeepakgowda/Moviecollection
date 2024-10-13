from django.utils.deprecation import MiddlewareMixin
from threading import Lock

class RequestCounterMiddleware(MiddlewareMixin):
    count = 0
    lock = Lock()

    def process_request(self, request):
        with RequestCounterMiddleware.lock:
            RequestCounterMiddleware.count += 1
        print(f"Request count incremented: {RequestCounterMiddleware.count}")

    def process_response(self, request, response):
        response['X-Request-Count'] = RequestCounterMiddleware.count
        print(f"Response count set: {RequestCounterMiddleware.count}")
        return response
