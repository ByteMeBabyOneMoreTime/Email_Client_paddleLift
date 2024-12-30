# your_project/middleware.py
from django.utils.deprecation import MiddlewareMixin

class NoRedirectOnOptionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            return None  # Do not redirect OPTIONS requests
        return None

