import django.db.models
import ckeditor.fields
import mptt.models
import fcdjangoutils.modelhelpers
import fcdjangoutils.middleware
import fcdjangoutils.fields
import fcdjangoutils.monkeypatching
import django.template
import datetime
import django.utils.http
from django.conf import settings
import django.contrib.auth.models
import django.core.urlresolvers
import django.db.models
import django.db.models.fields.related
import django.utils.functional
import django.db.models.query
from django.db.models import Q
import appomatic_renderable.models

class Project(appomatic_renderable.models.Article):
    github_username = django.db.models.CharField(max_length=50)
    repository_name = django.db.models.CharField(max_length=50)

class Font(Project):
    openfontlibrary_fontname = django.db.models.CharField(max_length=50)

@fcdjangoutils.monkeypatching.patch(appomatic_renderable.models.Tag)
def render__link__html(self, request, context):
    return u"<a href='%s'><i class='icon-tag'></i> %s</a>" % (self.get_absolute_url(), self)
