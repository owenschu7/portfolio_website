
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # let core handle the home page
    path('gRPC/', include('gRPC_demo.urls')),
    path('projects/', include('projects.urls')),
]







# lowkey not sure why this is here (ai generated)
# This is required during development so Django can find your uploaded images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
