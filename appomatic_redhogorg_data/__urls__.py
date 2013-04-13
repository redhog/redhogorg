import django.conf.urls

urlpatterns = django.conf.urls.patterns('',
    (r'^tag/(?P<name>.*)/?$', 'appomatic_redhogorg_data.views.tag'),
    (r'^node(?P<url>.*)/?$', 'appomatic_redhogorg_data.views.node'),
)
