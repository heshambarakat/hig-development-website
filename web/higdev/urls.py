from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from apps.leads.views import submit_lead
from apps.core.views import newweb_preview
from apps.seo.views import robots_txt
from apps.tracking.views import track_event


urlpatterns = [
    path("", lambda request: redirect("/ar/", permanent=False), name="root_redirect"),
    path("ar/", newweb_preview, {"lang": "ar"}, name="primary_home_ar"),
    path("en/", newweb_preview, {"lang": "en"}, name="primary_home_en"),
    path("django-admin/", admin.site.urls),
    path("higadmin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("newweb", newweb_preview, name="newweb_preview"),
    path("newweb/", newweb_preview, name="newweb_preview_slash"),
    path("newweb/<str:lang>/", newweb_preview, name="newweb_preview_lang"),
    path("leads/submit/", submit_lead, name="submit_lead"),
    path("tracking/event/", track_event, name="track_event"),
]

urlpatterns += i18n_patterns(
    path("", include(wagtail_urls)),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
