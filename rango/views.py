from rango.forms import UserForm, UserProfileForm, MemeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from rango.models import Category, Meme, UserProfile
from datetime import datetime
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

def index(request):
    meme_list = Meme.objects.order_by('-likes')

    paginator = Paginator(meme_list,1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    visitor_cookie_handler(request)

    response =  render(request, 'rango/index.html', {'page_obj': page_obj})
    return response


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        meme_list = Meme.objects.filter(category=category)
        paginator = Paginator(meme_list,1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context_dict['page_obj'] = page_obj
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['page_obj'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_meme(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = MemeForm()

    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                meme = form.save(commit=False)
                meme.category = category
                meme.likes = 0
                meme.dislikes = 0
                meme.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                        category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/upload.html', context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))

            else:
                return HttpResponse("Your account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)

    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

class LikeMemeView(View):
    @method_decorator(login_required)
    def get(self, request):
        meme_id = request.GET['meme_id']

        try:
            meme = Meme.objects.get(id=int(meme_id))
        except Meme.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        meme.likes = meme.likes + 1
        meme.save()

        return HttpResponse(meme.likes)

class DislikeMemeView(View):
    @method_decorator(login_required)
    def get(self, request):
        meme_id = request.GET['meme_id']

        try:
            meme = Meme.objects.get(id=int(meme_id))
        except Meme.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        meme.dislikes = meme.dislikes + 1
        meme.save()

        return HttpResponse(meme.dislikes)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'rango/profile.html', context_dict)
