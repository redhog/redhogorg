import appomatic_redhogorg_data.models
import django.contrib.admin
import mptt.admin
import autocomplete.widgets
import fcdjangoutils.fields

django.contrib.admin.site.register(appomatic_redhogorg_data.models.Tag, mptt.admin.MPTTModelAdmin)
class NodeAdmin(autocomplete.widgets.AutocompleteModelAdmin):
        list_display = ('published', 'title', 'source', 'license', 'author', 'url')
        list_display_links = ('published', 'title', 'source', 'license', 'author', 'url')
        list_filter = ('source', 'license', 'author')
        search_fields = ('title', 'source__tool', 'license__name', 'author__username', 'author__first_name', 'author__last_name', 'url')
        date_hierarchy = 'published'
        related_search_fields = {'tags': ('name',)}
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Category)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Source)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Article, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.File, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Image, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Project, NodeAdmin)
