import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import os.path
import datetime
from django.conf import settings
import django.core.files.storage
import django.db.models.fields.files
import appomatic_redhogorg_import.baseimport
import codecs
import markdown
import git

class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "gitimport"
    help = 'Imports a directory of git repositories. The directory must reside under %s' % settings.MEDIA_ROOT
    args = '<path>'

    def add(self, path):
        for name in os.listdir(path):
            repopath = os.path.join(path, name)
            if not os.path.exists(os.path.join(repopath, ".git")): continue
            content = ''
            for readme in ("README.md", "readme.md", "README.txt", "readme.txt", "README", "readme"):
                readme = os.path.join(repopath, readme)
                if os.path.exists(readme):
                    with codecs.open(readme, mode="r", encoding="utf-8") as f:
                        content = f.read()
                    if readme.lower().endswith(".md"):
                        content = markdown.markdown(content)
                    break

            repo = git.Repo(repopath)
            assert repo.bare == False

            remote = repo.remotes.origin.url

            if 'github.com' not in remote:
                print "IGNORING %s (%s not a github repo)" % (name, remote)

            remote = remote.split("github.com")[1][1:] # Remove everything before github.com/ or github.com:
            remote = remote.split("/")

            if remote[1] != name + ".git":
                print "IGNORING %s (remote name %s not same as local name)" % (name, remote[1])

            info = {
                "source": self.source,
                "author": self.user,
                "license": self.license,
                "url": "/" + name,
                "content": content,
                "title": name,
                "repository_name": name,
                "github_username": remote[0],
                "published": datetime.datetime.utcfromtimestamp(repo.heads.master.commit.committed_date)}

            tags = ["Software"]

            projecttype = 'project'
            infopath = repopath + ".__info__.py"
            if os.path.exists(infopath):
                data = {}
                execfile(infopath, data)
                if 'title' in data:
                    info['title'] = data['title']
                if 'openfontlibrary_fontname' in data:
                    info['openfontlibrary_fontname'] = data['openfontlibrary_fontname']
                if 'tags' in data:
                    tags = data['tags']
                if 'projecttype' in data:
                    projecttype = data['projecttype']
            
            if projecttype == 'project':
                Project = appomatic_redhogorg_data.models.Project
            elif projecttype == 'font':
                Project = appomatic_redhogorg_data.models.Font

            projects = Project.objects.filter(url = info['url'])

            if len(projects):
                project = projects[0]
                for key, value in info.iteritems():
                    setattr(project, key, value)
            else:
                project = Project(**info)
            project.save()
            for tag in tags:
                project.tags.add(self.add_tag(tag))

    def handle2(self, path, *args, **options):
        self.importroot = path
        if self.importroot.endswith('/'): self.importroot = self.importroot[:-1]

        self.set_source(self.importroot)
        self.add(path)
