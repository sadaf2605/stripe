from django.conf.urls import patterns, include, url
import admin
import views
import django


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stripe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
     url(r'^register/$', views.register, name='register'),
     url(r'^login/$', views.user_login, name='login'),
    # (r'^admin/', include(django.contrib.admin.site.urls)),
     url(r'^admin/', include(admin.stripe_admin_site.urls)),
)
