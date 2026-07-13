from django.http import Http404
from django.shortcuts import render


class HIGNotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and not request.path.startswith("/higadmin/"):
            return self.render_404(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404) and not request.path.startswith("/higadmin/"):
            return self.render_404(request)
        return None

    def render_404(self, request):
        language = "en" if request.path.startswith("/en/") else "ar"
        return render(
            request,
            "404.html",
            {
                "language": language,
                "home_url": f"/{language}/",
            },
            status=404,
        )
