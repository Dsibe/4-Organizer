from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template import Context, Template
from django.shortcuts import render
from .models import Post


def index(request):
    posts = Post.objects.all()
    posts_w_imgs = []

    for post in posts:
        img_path = static(post.img_path)
        posts_w_imgs.append((post, img_path))
    
    print(posts_w_imgs)
    
    return render(request, 'main/blog.html', context={'posts': posts_w_imgs})


def display_post(request, id):
    post = Post.objects.get(id=id)

    template = Template(f'{{% load static %}}\n{post.body}')
    c = Context({})
    body = template.render(c)

    img_path = static(post.img_path)

    return render(request,
                  'main/blog_post.html',
                  context={
                      'post': post,
                      'body': body,
                      'img_path': img_path,
                  })
