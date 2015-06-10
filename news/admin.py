from django.contrib import admin
from models import *
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q

import django.db.models

from tinymce.widgets import TinyMCE

class StripeAdminSite(admin.AdminSite):

    #site_header = 'Monty Python administration'
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        if request.user.is_superuser or "editor" in request.user.groups.values_list():
            user_not_approved=User.objects.filter(Q(is_staff=False))
            extra_context['user_not_approved'] = user_not_approved

            article_to_approve=Article.objects.filter(public=False,draft=False)
            extra_context['article_to_approve'] = article_to_approve


            print user_not_approved


        if "author" in request.user.groups.values_list('name',flat=True):
            author_articles=Article.objects.filter(author=request.user)

            draft_article=author_articles.filter(draft=True)
            print request.user
            extra_context['draft_article'] = draft_article

            editors_desk_article=author_articles.filter(public=False,draft=False)
            extra_context['editors_desk_article'] = editors_desk_article

            published_article=author_articles.filter(public=True)
            extra_context['published_article'] = published_article


        return super(StripeAdminSite, self).index(request,extra_context)


    def approve_author(self,request,username,):
        if request.user.is_superuser or "editor" in request.user.groups.values_list():

            try:
                u=User.objects.get(username=username)
            except User.DoesNotExist:
                pass
                #raise Http404()

            u.is_staff=True;
            user=u.save() #
            g = Group.objects.get(name='author')
            g.user_set.add(u)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def reject_author(self,request,username,):
        if request.user.is_superuser or "editor" in request.user.groups.values_list():

            try:
                u=User.objects.get(username=username)
            except User.DoesNotExist:
                pass
                #raise Http404()

            if not u.is_staff:
                u.delete()



        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def approve_article(self,request,id):
        if request.user.is_superuser or "editor" in request.user.groups.values_list():
            try:
                article=Article.objects.get(id=id)
                article.public=True
                article.save()
            except Article.DoesNotExist:
                pass
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    def reject_article(self,request,id):
        try:
            article=Article.objects.get(id=id)
            if request.user.is_superuser or "editor" in request.user.groups.values_list() or article.author==request.user:
                article.delete()
        except Article.DoesNotExist:
            pass

        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    def request_publish_article(self,request,id):
        if "author" in request.user.groups.values_list('name',flat=True):
            try:
                article=Article.objects.get(id=id)
                print article
                article.draft=False
                article.save()
            except Article.DoesNotExist:
                pass
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




    def get_urls(self):
        #self.admin_site.admin_view(self.approve_staff)
        urls = super(StripeAdminSite, self).get_urls()
        from django.conf.urls import url
        my_urls = [
            url(r'^author/approve/(?P<username>\w+)/$', self.approve_author),
            url(r'^author/reject/(?P<username>\w+)/$', self.reject_author),
            url(r'^Article/approve/(?P<id>\d+)/$', self.approve_article),
            url(r'^Article/reject/(?P<id>\d+)/$', self.reject_article),
            url(r'^Article/request/(?P<id>\d+)/$', self.request_publish_article),
        ]

        return my_urls + urls



class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    change_form_template = 'admin/news/change_form.html'

    def change_view(self, request,object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        #if type(extra_context) is not dict:
        #    print extra_context
            #extra_context={}
        extra_context["show_save_as_draft"] = True
        return super(ArticleAdmin, self).change_view(request,object_id, form_url, extra_context)

    prepopulated_fields = {'slug': ('title',) }
    def save_model(self, request, obj, *kwwargs):


        if not obj.id:
            obj.slug = slugify(obj.title)
            
        if request.user.is_superuser or request.user==obj.author or "editor" in request.user.groups.values_list('name', flat=True):
            if '_save_as_draft' in request.POST.keys():
                obj.draft = True
                print "draaaaaaaaaaaft button"
            super(ArticleAdmin,self).save_model(request, obj, *kwwargs)
        else:
            #obj.author=None
            from django.contrib import messages
            return messages.error(request,'Error message')
            #super(ArticleAdmin,self).save_model(request, obj, *kwwargs)


    def queryset(self, request):
        qs = super(ArticleAdmin, self).queryset(request)

        if request.user.is_superuser or "editor" in request.user.groups.values_list('name', flat=True):
            return qs
        else:
            return qs.filter(author=request.user)
#    fields = ['title', 'slug','body','pub_date', 'category','cover']
    pass


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}



stripe_admin_site = StripeAdminSite(name='Stripe')


stripe_admin_site.register(Article, ArticleAdmin)

stripe_admin_site.register(Category,CategoryAdmin)

from django.contrib.auth.admin import UserAdmin
stripe_admin_site.register(User, UserAdmin)

stripe_admin_site.register(UserProfile)
stripe_admin_site.register(PopularArticle)
stripe_admin_site.register(SliderArticle)




def author_group_permissions(sender, **kwargs):
    author=Group.objects.get_or_create(name='author')[0]
    for p in ["add","change","delete"]:
        perm=Permission.objects.get(name="Can "+p+" Article")

        author.permissions.add(perm)
        print perm," on ","Article", "granted for editor"



def editor_group_permissions(sender, **kwargs):
    editor=Group.objects.get_or_create(name='editor')[0]


    for m in ["Article", "popular Article", "slider Article"]:
        for p in ["add","change","delete"]:
            perm=Permission.objects.get(name="Can "+p+" "+m)
            editor.permissions.add(perm)
            print perm," on ",m, "granted for editor"


    ct = ContentType.objects.get(app_label='auth', model='user')
    staff_approve_perm=Permission.objects.get_or_create(codename='can_approve_staff',
                                                        name="Can approve staff",
                                                        content_type=ct)[0]
    print staff_approve_perm," on ","staff", "granted for editor"
    editor.permissions.add(staff_approve_perm)


from django.db.models import signals
signals.post_syncdb.connect(editor_group_permissions)
signals.post_syncdb.connect(author_group_permissions)