from django.shortcuts import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import *

def index(request):

    articles = Article.objects.filter(public=True,draft=False)
    popular_articles = PopularArticle.objects.all()
    slider_articles=SliderArticle.objects.all()
    template = loader.get_template('news/index.html')
    context = RequestContext(request, {
        'popular_articles':popular_articles,
        'slider_articles':slider_articles,
        'articles': articles,

    })
    return HttpResponse(template.render(context))


def story(request,slug):
    try:
        article = Article.objects.filter(slug=slug)[0]
    except User.DoesNotExist:
        raise Http404()

    articles = Article.objects.filter(public=True,draft=False)
    popular_articles = PopularArticle.objects.all()
    slider_articles=SliderArticle.objects.all()
    template = loader.get_template('news/story.html')
    context = RequestContext(request, {
        'popular_articles':popular_articles,
        'slider_articles':slider_articles,
        'articles': articles,
        'article' : article
    })
    return HttpResponse(template.render(context))



from forms import UserForm, UserProfileForm

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            print user.username, user.password
            u_s = authenticate(username=user.username, password=user.password)
            print u_s

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

        return render_to_response(
            'news/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

from django.contrib.auth import authenticate, login
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")


    else:

        return render_to_response('news/login.html', {}, context)