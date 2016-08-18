from django.contrib import admin
from django.conf import settings
from .models import *


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'origin', 'score', 'status', 'privilege')
    fieldsets = [
        (None, {'fields': ['title', 'status', 'privilege']}),
        (None, {'fields': ['category', 'contest', 'origin', 'flag', 'solved']}),
        (None, {'fields': ['zipfile', 'description', 'score', 'public']})
    ]


class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'docker_required', 'deployed')
    actions = ['deploy_challenge']

    def deploy_challenge(self, request, queryset):
        import zipfile, os, json, re
        success, fail = 0, 0
        for pack in queryset:
            filepath = os.path.join(settings.MEDIA_ROOT, pack.zipfile.name)
            if True:
                zip = zipfile.ZipFile(filepath)
                config = json.loads(zip.read('config.json'))
                dlpath = os.path.join(settings.MEDIA_URL, config['category'], config['title'])
                const = {}
                for item in config['statics']:
                    zip.extract(item, dlpath)
                    const[item] = os.path.join(dlpath, item)
                if 'dockerfile' in config:
                    # read dockerfile & deploy
                    const['port'] = 'some port'
                    #end
                pat = re.compile(r'#{\s*(\S+)\s*}')
                opt = {}
                if 'origin' in config:
                    opt['origin'], _ = Origin.objects.get_or_create(title=config['origin'])
                if 'contest' in config:
                    opt['contest'] = config['contest']
                if 'privilege' in config:
                    opt['privilege'] = config['privilege']
                Challenge.objects.update_or_create(
                    title=config['title'], category=config['category'],
                    score=config['score'], flag=config['flag'],
                    description=pat.sub(r'%(\1)s', config['content']) % const,
                    status='off' if 'dockerfile' in config else 'on',
                    defaults=opt
                )
                pack.title = config['title']
                pack.deployed = True
                pack.save()
                success += 1
            else:
                fail += 1
        self.message_user(request, '%d challenges deployed, %d failed' % (success, fail))




admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Package, PackageAdmin)