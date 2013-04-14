import appomatic_redhogorg_data.models
import urllib

def node(request, url):
    return appomatic_redhogorg_data.models.Node.objects.get(url=url).render(request)

def tag(request, name):
    name=urllib.unquote_plus(name).decode('utf8')
    if name == "" or name == "/":
        return appomatic_redhogorg_data.models.Tag.render_list(request)
    else:
        return appomatic_redhogorg_data.models.Tag.objects.get(name=urllib.unquote_plus(name).decode('utf8')).render(request)
