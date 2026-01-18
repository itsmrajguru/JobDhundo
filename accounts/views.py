# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from .services.jobs_api import search_jobs   # keep if you use jobs API

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
    return render(request, 'accounts/login.html')

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
    return render(request, 'accounts/signup.html')

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mainpage")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})

@login_required
def mainpage_view(request):
    # ✅ Get search query from GET params
    query = request.GET.get("q", "").strip()

    # ✅ Call Adzuna jobs API (via your service wrapper)
    data = search_jobs(query) if query else search_jobs("")
    jobs = data.get("results", [])[:4]

    # ✅ Pass query into template so heading can switch
    return render(
        request,
        "accounts/mainpage.html",
        {
            "jobs": jobs,
            "query": query,   # used in template to show "Results for ..."
        }
    )

@login_required
def resumebuilder_view(request):
    return render(request, 'accounts/resumebuilder.html')

@login_required
def messages_view(request):
    return render(request, 'accounts/messages.html')

@login_required
def jobs(request):
    # get search query from GET params
    query = request.GET.get("q", "").strip()

    # call Adzuna jobs API (same logic as main page)
    data = search_jobs(query) if query else search_jobs("")
    jobs = data.get("results", [])

    return render(
        request,
        "accounts/jobs.html",
        {
            "jobs": jobs,
            "query": query,
        }
    )
