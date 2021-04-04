from rango.forms import UserForm, UserProfileForm, MemeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from rango.models import Category, Meme

def index(request):
    category_list = Category.objects.order_by('-likes')
    meme_list = Meme.objects.order_by('-likes')[:1]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['memes'] = meme_list

    return render(request, 'rango/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        memes = Meme.objects.filter(category=category)
        context_dict['memes'] = memes
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['memes'] = None
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
        
        
    return render(request, 'rango/register.html', context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})


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