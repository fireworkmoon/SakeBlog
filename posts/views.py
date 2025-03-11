from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category

# Create your views here.

class IndexView(ListView):
    """首页视图"""
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class PostDetailView(DetailView):
    """文章详情视图"""
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

class CategoryView(ListView):
    """分类视图"""
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)
