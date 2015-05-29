from django.contrib import admin
from models import *
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType


class StripeAdminSite(admin.AdminSite):
    #site_header = 'Monty Python administration'
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['some_var'] = 'This is what I want to show'
        return super(StripeAdminSite, self).index(request,extra_context)


class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, *kwwargs):
        if request.user.is_superuser or request.user==obj.author or "editor" in request.user.groups.values_list('name', flat=True):
            super(ArticleAdmin,self).save_model(request, obj, *kwwargs)
        else:
            obj.author=None
            super(ArticleAdmin,self).save_model(request, obj, *kwwargs)

    def queryset(self, request):
        qs = super(ArticleAdmin, self).queryset(request)

        if request.user.is_superuser or "editor" in request.user.groups.values_list('name', flat=True):
            return qs
        else:
            return qs.filter(author=request.user)
#    fields = ['title', 'slug','body','pub_date', 'category','cover']
    pass

#    def has_add_permission(self, request):
#        return request.user.groups.filter(name='author').exists()

#    def has_change_permission(self, request, obj=None):
#        print obj
#        return request.user.groups.filter(name='editor').exists() or (request.user.groups.filter(name='author').exists() and Article.objects.filter(pk=obj, author=request.user).count() >0 )

#    def has_delete_permission(self, request, obj=None):
#        return request.user.groups.filter(name='editor').exists() or (request.user.groups.filter(name='author').exists() and Article.objects.filter(pk=obj, author=request.user).count() >0 )







stripe_admin_site = StripeAdminSite(name='Stripe')


stripe_admin_site.register(Article, ArticleAdmin)

stripe_admin_site.register(Category)

from django.contrib.auth.admin import UserAdmin
stripe_admin_site.register(User, UserAdmin)

stripe_admin_site.register(UserProfile)
stripe_admin_site.register(PopularArticle)
stripe_admin_site.register(SliderArticle)












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
veryFirst = False

if veryFirst:

    if first:
        Group.objects.get_or_create(name='editor')
        Group.objects.get_or_create(name='author')


        article=Permission.objects.get(name="Can add article")
        group.permissions.add(article)

        article=Permission.objects.get(name="Can change article")
        group.permissions.add(article)

        article=Permission.objects.get(name="Can delete article")
        group.permissions.add(article)

        article=Permission.objects.get(name="Can view article")
        group.permissions.add(article)
        print "permissions",group.permissions



def author_group_permissions(sender, **kwargs):
    author=Group.objects.get_or_create(name='author')[0]
    for p in ["add","change","delete"]:
        perm=Permission.objects.get(name="Can "+p+" article")

        author.permissions.add(perm)
        print perm," on ","article", "granted for editor"



def editor_group_permissions(sender, **kwargs):
    editor=Group.objects.get_or_create(name='editor')[0]
    for m in ["article", "popular article", "slider article"]:
        for p in ["add","change","delete"]:
            perm=Permission.objects.get(name="Can "+p+" "+m)
            editor.permissions.add(perm)
            print perm," on ",m, "granted for editor"









from django.db.models import signals
signals.post_syncdb.connect(editor_group_permissions)
signals.post_syncdb.connect(author_group_permissions)



from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

def add_view_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a view permission too all our
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            print "Added view permission for %s" % content_type.name

# check for all our view permissions after a syncdb
#post_syncdb.connect(add_view_permissions)