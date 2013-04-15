import django.db.models
import ckeditor.fields
import mptt.models
import fcdjangoutils.modelhelpers
import django.template
import datetime
import django.utils.http
from django.conf import settings
import fcdjangoutils.middleware
import django.contrib.auth.models

def get_basetypes(t):
    basetypes = []
    def get_basetypes(t):
        basetypes.append("%s.%s" % (t.__module__, t.__name__))
        for tt in t.__bases__:
            get_basetypes(tt)
    get_basetypes(t)
    return basetypes

class Renderable(fcdjangoutils.modelhelpers.SubclasModelMixin):
    @fcdjangoutils.modelhelpers.subclassproxy
    def context(self, request, style = 'page.html'):
        return {'obj': self.subclassobject}

    @fcdjangoutils.modelhelpers.subclassproxy
    def render(self, request, style = 'page.html', context_arg = {}):
        context = self.context(request, style)
        context.update(context_arg)
        return django.template.loader.select_template(
            ["%s/%s" % (t.replace(".", "/"), style)
             for t in get_basetypes(type(self))]
            ).render(
            django.template.RequestContext(
                    request,
                    context))
    
    @classmethod
    def list_context(cls, request, style = 'page.html'):
        return {"objs": cls.objects.all()}

    @classmethod
    def render_list(cls, request, style = 'page.html', context_arg = {}):
        context = cls.list_context(request, style)
        context.update(context_arg)
        return django.template.loader.select_template(
            ["%s-list/%s" % (t.replace(".", "/"), style)
             for t in get_basetypes(cls)]
            ).render(
            django.template.RequestContext(
                    request,
                    context))

    @fcdjangoutils.modelhelpers.subclassproxy
    def render_as(self):
        obj = self
        class Res(object):
            def __getattribute__(self, style):
                return obj.render(fcdjangoutils.middleware.get_request(), style + ".html")
        return Res()

class Tag(mptt.models.MPTTModel, Renderable):
    name = django.db.models.CharField(max_length=50)
    parent = mptt.models.TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        unique_together = (("name", "parent"),)
        ordering = ('name', )        

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        nodes = Node.objects.filter(title = self.name)
        if len(nodes):
            return nodes[0].get_absolute_url()
        else:
            return django.core.urlresolvers.reverse('appomatic_redhogorg_data.views.tag', kwargs={'name': django.utils.http.urlquote_plus(self.name)})

    @classmethod
    def list_context(cls, request, style = 'page.html'):
        return {"objs": cls.objects.filter(parent = None)}

    @classmethod
    def menutree(cls):
        def menutree(parent = None):
            if parent:
                children = parent.children.all()
            else:
                children = cls.objects.filter(parent=None)
            if len(children) == 0:
                return ""
            else:
                csscls = ["menu"]
                if parent is None: csscls.append("menubar")
                return "<ul class='%s'>%s</ul>" % (
                    " ".join(csscls),
                    "\n".join("<li><a href='%s'>%s</a>%s</li>" % (child.get_absolute_url(),
                                                                  child.name,
                                                                  menutree(child))
                              for child in children))
        if not getattr(cls, "_menutree", None):
            cls._menutree = menutree()
        return cls._menutree

class Source(django.db.models.Model):
    tool = django.db.models.CharField(max_length=50)
    argument = django.db.models.CharField(max_length=1024)

    def __unicode__(self):
        return "%s: %s" % (self.tool, self.argument)

class License(django.db.models.Model):
    name = django.db.models.CharField(max_length=50)
    url = django.db.models.CharField(max_length=1024)

    def __unicode__(self):
        return "<a href='%s'>%s</a>" % (self.url, self.name)

class Node(django.db.models.Model, Renderable):
    url = django.db.models.CharField(max_length=1024, unique=True)
    tags = django.db.models.ManyToManyField(Tag, null=True, blank=True, related_name='nodes')
    title = django.db.models.CharField(max_length=50)
    published = django.db.models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    source = django.db.models.ForeignKey(Source, null=True, blank=True)
    license = django.db.models.ForeignKey(License, null=True, blank=True)
    author = django.db.models.ForeignKey(django.contrib.auth.models.User, null=True, blank=True)

    @fcdjangoutils.modelhelpers.subclassproxy
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return django.core.urlresolvers.reverse('appomatic_redhogorg_data.views.node', kwargs={'url': self.url})

    @property
    def tag(self):
        res = Tag.objects.filter(name = self.title)
        if not len(res):
            return None
        return res[0]

    class Meta:
        ordering = ('-published', 'title', )        

class Category(Node):
    @fcdjangoutils.modelhelpers.subclassproxy
    def context(self, request, style = 'page.html'):
        context = Node.context(self, request, style)
        nodes = {}
        for tag in self.tags.all():
            nodes.update(dict(
                    (node.url, node.subclassobject)
                    for node in tag.nodes.all()
                    if node.id != self.id))
        context['nodes'] = nodes
        return context

class Article(Node):
    summary = ckeditor.fields.RichTextField(blank=True, null=True)
    content = ckeditor.fields.RichTextField()

    def __unicode__(self):
        return self.title

class File(Node):
    content = django.db.models.FileField(upload_to='.')
    description = ckeditor.fields.RichTextField(blank=True, null=True)

class Image(Node):
    content = django.db.models.ImageField(upload_to='.')
    description = ckeditor.fields.RichTextField(blank=True, null=True)

class Project(Article):
    github_username = django.db.models.CharField(max_length=50)
    repository_name = django.db.models.CharField(max_length=50)
