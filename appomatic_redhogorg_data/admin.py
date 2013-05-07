import appomatic_redhogorg_data.models
import django.contrib.admin
import mptt.admin
import autocomplete.widgets
import fcdjangoutils.fields

django.contrib.admin.site.register(appomatic_redhogorg_data.models.Tag, mptt.admin.MPTTModelAdmin)
class NodeAdmin(autocomplete.widgets.AutocompleteModelAdmin):
    exclude = ('tag',)
    list_display = ('published', 'title', 'source', 'license', 'author', 'url')
    list_display_links = ('published', 'title', 'source', 'license', 'author', 'url')
    list_filter = ('source', 'license', 'author')
    search_fields = ('title', 'source__tool', 'license__name', 'author__username', 'author__first_name', 'author__last_name', 'url')
    date_hierarchy = 'published'
    related_search_fields = {'tags': ('name',)}
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Source)
class ArticleAdmin(NodeAdmin):
    related_search_fields = {'tags': ('name',),
                             'image': ('title',)}
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Article, ArticleAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.File, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Image, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Project, ArticleAdmin)

class ListCollectionMemberInline(autocomplete.widgets.AutocompleteTabularInline):
    model = appomatic_redhogorg_data.models.ListCollectionMember
    fk_name = "collection"
    related_search_fields = {'node': ('title',)}

class ListCollectionAdmin(NodeAdmin):
    inlines = [ListCollectionMemberInline]

django.contrib.admin.site.register(appomatic_redhogorg_data.models.ListCollection, ListCollectionAdmin)

django.contrib.admin.site.register(appomatic_redhogorg_data.models.StaticTemplate, NodeAdmin)
