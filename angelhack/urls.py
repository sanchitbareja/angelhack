from django.conf.urls import patterns, include, url
from angelhack.views import index_home, generate_impressjs, upload_file, login, login_authenticate, logout, signup, loggedout, invalid, past_toasts

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', index_home),
	url(r'^default_impressjs/$',generate_impressjs),
	url(r'^upload/txt/$', upload_file),
	url(r'^impressify/txt/$',index_home),

    url(r'^accounts/login/$', login),
    url(r'^accounts/login_authenticate/$', login_authenticate),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/signup/$', signup),
    url(r'^accounts/loggedout/$', loggedout),
    url(r'^accounts/invalid/$', invalid),

    url(r'^past/toasts/$', past_toasts),

    # Examples:
    # url(r'^$', 'angelhack.views.home', name='home'),
    # url(r'^angelhack/', include('angelhack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
