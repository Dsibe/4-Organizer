from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template import Context, Template
from django.shortcuts import render, HttpResponse
from .models import Post


def index(request, show_only):
    posts = Post.objects.all()
    categories = [post.category for post in posts]
    categories = list(set(categories))

    if show_only != 'all':
        posts = posts.filter(category=show_only)

    posts = list(reversed(posts))
    posts_w_imgs = []

    for post in posts:
        img_path = static(post.img_path)
        posts_w_imgs.append((post, img_path))

    posts_w_imgs.sort(key=lambda i: getattr(i[0], 'creation_date'),
                      reverse=True)

    return render(request,
                  'main/blog.html',
                  context={
                      'posts': posts_w_imgs,
                      'categories': categories
                  })


def display_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return HttpResponse('404 error: psot not found')

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


def test_post(request):
    return render(request, 'main/test_post.html')
