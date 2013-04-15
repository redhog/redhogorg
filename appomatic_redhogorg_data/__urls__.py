import django.conf.urls

urlpatterns = django.conf.urls.patterns('',
    (r'^tag/(?P<name>.*)/?$', 'appomatic_redhogorg_data.views.tag'),
    (r'^(?P<url>.*)/?$', 'appomatic_redhogorg_data.views.node'),
)

if django.conf.settings.DEBUG:
    urlpatterns = django.conf.urls.patterns(
        '',
        django.conf.urls.url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django.conf.settings.MEDIA_ROOT, 'show_indexes': True}),
        django.conf.urls.url(r'', django.conf.urls.include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
