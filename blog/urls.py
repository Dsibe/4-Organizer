from django.urls import path, include
import blog.views as blog_views

urlpatterns = [
    path('index/<path:show_only>', blog_views.index, name='blog-index'),
    path('post/<path:slug>', blog_views.display_post, name='display-post'),
    path('test_post', blog_views.test_post),
]
