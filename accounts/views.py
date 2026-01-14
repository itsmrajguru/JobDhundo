# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')   # ✅ matches template

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out.')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Username and password required.')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/signup.html')
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
        messages.success(request, 'Account created! Please login.')
        return redirect('login')
    return render(request, 'accounts/signup.html')   # ✅ matches template

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def home_view(request):
    return render(request, 'accounts/home.html')   # ✅ jobs removed for now

@login_required
def edit_profile(request):
    # get or create profile for logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mainpage")   # ✅ after saving, go to main page
    else:
        form = ProfileForm(instance=profile)  # ✅ pre-populate with saved data

    return render(request, "accounts/profile.html", {"form": form})



@login_required
def mainpage_view(request):
    return render(request, 'accounts/mainpage.html')

@login_required
def resumebuilder_view(request):
    return render(request, 'accounts/resumebuilder.html')

@login_required
def messages_view(request):
    return render(request, 'accounts/messages.html')

@login_required
def achievements_view(request):
    return render(request, 'accounts/achievements.html')

from .services.jobs_api import search_jobs

def mainpage_view(request):
    query = request.GET.get("q", "").strip()
    if query:
        # Domain-based jobs when searching
        data = search_jobs(query)
    else:
        # Latest jobs when no search
        data = search_jobs("")
    jobs = data.get("results", [])
    return render(request, "accounts/mainpage.html", {"jobs": jobs, "query": query})
