from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [
    #url(r'^list', RfsnListView.as_view(), name='rfsn-list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myapp/', include('myproject.myapp.urls')),
    url(r'^$', RedirectView.as_view(url='/myapp/upload_file/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
