from django.contrib import admin
from models import *




from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

#content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
#permission = Permission.objects.create(codename='can_publish',
#                                       name='Can Publish Posts',
#                                       content_type=content_type)
#user = User.objects.get(username='duke_nukem')
#group = Group.objects.get(name='wizard')
#group.permissions.add(permission)
#user.groups.add(group)

#Group.objects.create(name='editor')
#Group.objects.create(name='author')

#group = Group.objects.get(name='author')
#User.objects.filter(username="user")[0].groups.add(group)
#can_fm_list = Permission.objects.get(name='Article')
#newgroup.permissions.add(can_fm_list)
first = True
veryFirst = True

if veryFirst:

    if first:
    #    Group.objects.create(name='editor')
    #    Group.objects.create(name='author')

        group = Group.objects.get(name='author')

        article=Permission.objects.get(name="Can add article")
        group.permissions.add(article)

        article=Permission.objects.get(name="Can change article")
        group.permissions.add(article)

        article=Permission.objects.get(name="Can delete article")
        group.permissions.add(article)


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
#    fields = ['title', 'slug','body','pub_date', 'category','cover']

    def has_add_permission(self, request):
        return request.user.groups.filter(name='author').exists()

    def has_change_permission(self, request, obj=None):
        print obj
        return request.user.groups.filter(name='editor').exists() or (request.user.groups.filter(name='author').exists() and Article.objects.filter(pk=obj, author=request.user).count() >0 )

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='editor').exists() or (request.user.groups.filter(name='author').exists() and Article.objects.filter(pk=obj, author=request.user).count() >0 )


class MyModelAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['some_var'] = 'This is what I want to show'
        return super(MyModelAdmin, self).changelist_view(request, extra_context=extra_context)



admin.site.register(Article, ArticleAdmin)

admin.site.register(Category)
admin.site.register(UserProfile)