import appomatic_redhogorg_data.models
import appomatic_renderable.admin
import django.contrib.admin

django.contrib.admin.site.register(appomatic_redhogorg_data.models.Project, appomatic_renderable.admin.ArticleAdmin)
django.contrib.admin.site.register(appomatic_redhogorg_data.models.Font, appomatic_renderable.admin.ArticleAdmin)
