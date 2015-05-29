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






stripe_admin_site = StripeAdminSite(name='Stripe')


stripe_admin_site.register(Article, ArticleAdmin)

stripe_admin_site.register(Category)

from django.contrib.auth.admin import UserAdmin
stripe_admin_site.register(User, UserAdmin)

stripe_admin_site.register(UserProfile)
stripe_admin_site.register(PopularArticle)
stripe_admin_site.register(SliderArticle)



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