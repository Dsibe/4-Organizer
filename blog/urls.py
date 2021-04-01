from django.urls import path, include
import blog.views as blog_views

urlpatterns = [
    path('', blog_views.index, name='blog-index'),
    path('post/<int:id>', blog_views.display_post, name='display-post'),
]
