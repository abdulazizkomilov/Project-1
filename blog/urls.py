from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<str:name>/<str:slug>/', views.single, name='single'),
    path('accounts/users/login/', views.loginPage, name='login'),
    path('accounts/users/sign-up/', views.registerPage, name='sign_up'),
    path('logout/', views.logoutPage, name='logout'),
    path('remove/<int:id>/', views.post_remove_add, name='post_remove_add'),
    path('undo-post/<int:id>/', views.post_remove, name='post_remove'),
    path('profile/favourites/', views.favourite_list, name='favourite_list'),
    path('profile/removed/', views.removed_list, name='removed_list'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('like/<int:id>/', views.like_dislike, name='like_dislike'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
]
