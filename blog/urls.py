from django.contrib.auth import views as v
from django.urls import path

from . import views

urlpatterns = [
    path('', views.cons_list, name='cons_list'),
    path('suggs/', views.post_list, name='suggs_list'),
    path('cons/<int:pk>/', views.cons_detail, name='consultation_detail'),
    path('sugg/<int:pk>/', views.post_detail, name='post_detail'),
    path('sugg/new/', views.post_new, name='sugg_new'),
    path('cons/<int:pk>/edit/', views.cons_edit, name='consultation_edit'),
    path('sugg/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('profile/', views.main_profile, name='main_profile'),
    path('profile/edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('cons/new/', views.cons_new, name='consultation_new'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('signup/', views.user_new, name='signup'),
    path('login/', v.LoginView.as_view(), name='login'),
    path('delete/<int:pk>/', views.delete_cons, name='cons_delete'),
    path('<int:pk>', views.likes, name='likes'),
    # path('<int:pk>/grade/', views.grades, name='grade'),
]
