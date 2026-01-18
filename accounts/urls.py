# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path("mainpage/", views.mainpage_view, name="mainpage"),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),   # ✅ consistent
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('resumebuilder/', views.resumebuilder_view, name='resumebuilder'),
    path('messages/', views.messages_view, name='messages'),
    path("jobs/", views.jobs, name="jobs"),
]
