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
import django.core.urlresolvers

def get_basetypes(t):
    basetypes = []
    def get_basetypes(t):
        basetypes.append("%s.%s" % (t.__module__, t.__name__))
        for tt in t.__bases__:
            get_basetypes(tt)
    get_basetypes(t)
    return basetypes

TypeType = type

class Renderable(fcdjangoutils.modelhelpers.SubclasModelMixin):
    @property
    def types(self):
        return ' '.join(t.replace(".", "-") for t in get_basetypes(TypeType(self)))

    @fcdjangoutils.modelhelpers.subclassproxy
    def context(self, request, style = 'page.html'):
        return {'obj': self.subclassobject}

    @fcdjangoutils.modelhelpers.subclassproxy
    def render(self, request, style = 'page.html', context_arg = {}):
        subtype = ''
        if hasattr(self, 'render_subtype'):
            subtype = "/" + self.render_subtype
        context = self.context(request, style)
        context.update(context_arg)
        return django.template.loader.select_template(
            ["%s%s/%s" % (t.replace(".", "/"), subtype, style)
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

    def get_admin_url(self):
        return django.core.urlresolvers.reverse(
            'admin:%s_%s_change' % (self._meta.app_label,
                                    self._meta.module_name),
            args=[self.id])


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

    def breadcrumb(self, include_self=False):
        return self.get_ancestors(include_self=include_self)

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
                items = ""
                if parent is None:
                    items = "<li><a href='/'>Home</a></li>"
                items += "\n".join("<li><a href='%s'>%s</a>%s</li>" % (child.get_absolute_url(),
                                                                       child.name,
                                                                       menutree(child))
                                   for child in children)
                return "<ul class='%s'>%s</ul>" % (
                    " ".join(csscls),
                    items)
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
        return django.core.urlresolvers.reverse('appomatic_redhogorg_data.views.node', kwargs={'url': self.url[1:]})

    @property
    def tag(self):
        res = Tag.objects.filter(name = self.title)
        if not len(res):
            return None
        return res[0]

    def breadcrumb(self):
        if self.tag:
            return self.tag.breadcrumb()
        tags = self.tags.all()
        if len(tags):
            return tags[0].breadcrumb(include_self=True)
        return []

    class Meta:
        ordering = ('-published', 'title', )

    @classmethod
    def get(cls):
        Obj = cls
        class Res(object):
            def __getattribute__(self, url):
                return Obj.objects.get(url = "/" + url.replace("__", "/"))
        return Res()


class Collection(Node):
    @fcdjangoutils.modelhelpers.subclassproxy
    def items(self):
        return []

class ListCollection(Collection):
    nodes = django.db.models.ManyToManyField(Node, null=True, blank=True, through='ListCollectionMember', related_name='in_list_collection')
    
    def items(self):
        relations = ListCollectionMember.objects.filter(collection = self)

        return Node.objects.filter(
            member_in_list_collection__in = relations
            ).annotate(
            ordering = django.db.models.Min('member_in_list_collection__ordering')
            ).order_by('ordering').distinct()

class ListCollectionMember(django.db.models.Model):
    collection = django.db.models.ForeignKey(ListCollection, related_name="members")
    node = django.db.models.ForeignKey(Node, related_name='member_in_list_collection')
    ordering = django.db.models.FloatField(default = 0)    

class Article(Node):
    summary = ckeditor.fields.RichTextField(blank=True, null=True)
    content = ckeditor.fields.RichTextField()

class File(Node):
    content = django.db.models.FileField(upload_to='.')
    description = ckeditor.fields.RichTextField(blank=True, null=True)

class Image(Node):
    content = django.db.models.ImageField(upload_to='.')
    description = ckeditor.fields.RichTextField(blank=True, null=True)

class Project(Article):
    github_username = django.db.models.CharField(max_length=50)
    repository_name = django.db.models.CharField(max_length=50)

class Font(Project):
    openfontlibrary_fontname = django.db.models.CharField(max_length=50)

class StaticTemplate(Node):
    render_subtype = django.db.models.CharField(
        max_length=50,
        choices=(
            ('MainMenu', 'Main menu'),
            ('Badge/FaceBook', 'FaceBook badge'),
            ('Badge/GitHub', 'GitHub badge'),
            ('Badge/Twitter', 'Twitter badge'),
            ('Badge/LinkedIn', 'LinkedIn badge')
            ))
