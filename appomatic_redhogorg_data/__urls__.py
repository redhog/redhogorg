import django.conf.urls
import appomatic_renderable.__urls__

urlpatterns = django.conf.urls.patterns('')

appomatic_renderable.__urls__.urlpatterns = django.conf.urls.patterns('',
    (r'^tag/(?P<name>.*)/?$', 'appomatic_renderable.views.tag'),
    (r'^(?P<url>.*)/?$', 'appomatic_renderable.views.node'),
)

if django.conf.settings.DEBUG:
    appomatic_renderable.__urls__.urlpatterns = django.conf.urls.patterns(
        '',
        django.conf.urls.url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django.conf.settings.MEDIA_ROOT, 'show_indexes': True}),
        django.conf.urls.url(r'', django.conf.urls.include('django.contrib.staticfiles.urls')),
    ) + appomatic_renderable.__urls__.urlpatterns
