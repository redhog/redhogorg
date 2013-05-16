INSTALLED_APPS = ['appomatic_websitebase', 'endless_pagination']
MIDDLEWARE_CLASSES=['fcdjangoutils.middleware.EarlyResponse',
                    'fcdjangoutils.middleware.GlobalRequestMiddleware']
TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request']
