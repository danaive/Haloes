# -*- coding: utf-8 -*-
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
    list_display = ('title', 'uploader', 'docker_required', 'deployed')
    actions = ['deploy_challenge']

    def deploy_challenge(self, request, queryset):
        import zipfile, os, json, re, string
        success, fail = 0, 0
        for pack in queryset:
            # try:
            if True:
                zp = zipfile.ZipFile(pack.zipfile.path)
                config = json.loads(zp.read('config.json'))
                # assert not filter(lambda x: x not in string.printable, pack.title)
                config['content'] = zp.read(config['description']).decode('utf-8')
                dlpath = os.path.join(settings.MEDIA_URL, config['category'], pack.title)
                extpath = os.path.join(settings.MEDIA_ROOT, config['category'], pack.title)
                const = {}
                for item in config['statics']:
                    zp.extract(item, extpath)
                    const[item] = os.path.join(dlpath, item)
                pat = re.compile(r'#{\s*(\S+)\s*}')
                opt = {}
                if 'dockerfile' in config:
                    opt['privilege'] = 0
                    # read dockerfile & deploy
                    const['port'] = 'some port'
                    # end
                if 'origin' in config:
                    opt['origin'], _ = Origin.objects.get_or_create(title=config['origin'])
                if 'contest' in config:
                    opt['contest'] = config['contest']
                if 'privilege' in config:
                    opt['privilege'] = config['privilege']
                Challenge.objects.update_or_create(
                    title=config['title'],
                    category=config['category'],
                    score=config['score'],
                    flag=config['flag'],
                    description=pat.sub(r'%(\1)s', config['content']) % const,
                    status='off' if 'dockerfile' in config else 'on',
                    defaults=opt
                )
                pack.deployed = True
                pack.save()
                success += 1
            # except:
            else:
                fail += 1
        self.message_user(request, '%d challenges deployed, %d failed' % (success, fail))


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Package, PackageAdmin)
