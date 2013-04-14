import appomatic_redhogorg_data.models
import urllib
import django.http

def node(request, url):
    return django.http.HttpResponse(appomatic_redhogorg_data.models.Node.objects.get(url=url).render(request))

def tag(request, name):
    name=urllib.unquote_plus(name).decode('utf8')
    if name == "" or name == "/":
        return django.http.HttpResponse(appomatic_redhogorg_data.models.Tag.render_list(request))
    else:
        return django.http.HttpResponse(appomatic_redhogorg_data.models.Tag.objects.get(name=urllib.unquote_plus(name).decode('utf8')).render(request))
