from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout, login, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView

from apps.Users.views import RequestAccessView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.Products.urls')),
    url(r'^apis/', include('apps.apis.urls')),
    #url(r'^apis/docs/', include('rest_framework_docs.urls')),
    url(r'^servers/', include('apps.Servers.urls')),
    url(r'^testings/', include('apps.Testings.urls')),
    url(r'^users/', include('apps.Users.urls')),
    url(r'^request-access/', RequestAccessView.as_view(), name='request-access'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name="reset-password"),
    url(r'^password_reset/done/$',
        PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$',
        PasswordResetCompleteView.as_view(), name='password_reset_complete')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
