from django.conf.urls import patterns, include, url
from angelhack.views import index_home, generate_impressjs, upload_file

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', index_home),
	url(r'default_impressjs',generate_impressjs),
	url(r'^upload/txt/', upload_file),
    # Examples:
    # url(r'^$', 'angelhack.views.home', name='home'),
    # url(r'^angelhack/', include('angelhack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
