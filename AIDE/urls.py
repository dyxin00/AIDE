from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AIDE.views.home', name='home'),
    # url(r'^AIDE/', include('AIDE.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'jw.views.index', name='index'),
    url('^captcha$', 'jw.views.captcha', name='captcha'),
    url('^login_jw$', 'jw.views.login_jw', name='login_jw'),
)
