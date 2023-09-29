from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:pk>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/<int:comment_id>/edit_comment/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:pk>/<int:comment_id>/delete_comment/',
         views.delete_comment, name='delete_comment'),
    path('login_only/', views.simple_view),
]
