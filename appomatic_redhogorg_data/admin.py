import appomatic_redhogorg_data.models
import django.contrib.admin
import mptt.admin
import autocomplete.widgets
import fcdjangoutils.fields

django.contrib.admin.site.register(appomatic_redhogorg_data.models.Tag, mptt.admin.MPTTModelAdmin)
class NodeAdmin(autocomplete.widgets.AutocompleteModelAdmin):
        related_search_fields = {'tags': ('name',)}
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Category)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Source)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Article, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.File, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Image, NodeAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Project, NodeAdmin)
