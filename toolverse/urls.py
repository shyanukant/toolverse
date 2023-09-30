from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.views.static import serve
from menus.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("menus.urls")),
    path('content/', include("contents.urls")),
    path('auth/', include("authz.urls")),
    path('brands/', include("brands.urls")),
    path('account/', include("allauth.urls")),
    path('404/', custom_404, name="404")

] 

handler404 = custom_404
# if settings.DEBUG:
    # do not do this in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)