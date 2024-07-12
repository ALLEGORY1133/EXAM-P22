# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path, include
#
# # from events.admin import event_admin_site
# from rebel.admin import rebel_admin_site
# from root.settings import MEDIA_URL, MEDIA_ROOT
#
# urlpatterns = [
#                   path('', include('rebel.urls')),
#                   # path('entity-admin/', admin.site.urls),
#                   # path('event-admin/', event_admin_site.urls),
#                   path('rebel/', rebel_admin_site.urls),
#               ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
#
# admin.site.site_header = "UMSRA Admin"
# admin.site.site_title = "UMSRA Admin Portal"
# admin.site.index_title = "Welcome to UMSRA Researcher Portal"
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apps.urls')),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)

