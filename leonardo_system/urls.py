from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
                       url(r'^packages/', include('leonardo_system.package.urls')),
                       url(r'^maintenance/', include('leonardo_system.maintenance.urls')),
                       )
