# Django 学习指南

## 1. Django 核心概念

### 1.1 MTV架构

Django采用MTV（Model-Template-View）架构模式：
```
- Model：数据模型，处理数据逻辑
- Template：模板，处理显示逻辑
- View：视图，处理业务逻辑
```

### 1.2 项目结构

```
django_blog/
├── manage.py          # 项目管理脚本
├── blog/              # 项目配置目录
│   ├── __init__.py
│   ├── settings.py    # 项目设置
│   ├── urls.py       # URL配置
│   ├── asgi.py       # ASGI配置
│   └── wsgi.py       # WSGI配置
└── posts/            # 应用目录
    ├── __init__.py
    ├── admin.py      # 管理后台配置
    ├── apps.py       # 应用配置
    ├── models.py     # 数据模型
    ├── views.py      # 视图函数
    ├── urls.py       # 应用URL配置
    └── templates/    # 模板文件
```

### 1.3 配置系统（Settings）

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'posts.apps.PostsConfig',  # 注册应用
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
    }
]
```

- 应用配置
- 数据库配置
- 模板配置
- 静态文件配置
- 中间件配置

### 1.4 URL配置（URLconf）

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

# posts/urls.py
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
]
```

- URL模式
- 路径转换器
- 命名URL模式
- 包含其他URLconf

### 1.5 视图系统（Views）

```python
# 函数视图
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

# 类视图
class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    paginate_by = 10
```

- 函数视图
- 类视图
- 通用视图
- 混入类（Mixins）

### 1.6 模型系统（Models）

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
```

- 字段类型
- 关系字段
- 元数据选项
- 模型管理器
- 查询API

### 1.7 模板系统（Templates）

```html
{% extends "base.html" %}

{% block content %}
<h1>{{ post.title }}</h1>
<p>{{ post.content|linebreaks }}</p>
{% if user.is_authenticated %}
    <a href="{% url 'edit_post' post.pk %}">编辑</a>
{% endif %}
{% endblock %}
```

- 模板继承
- 变量和过滤器
- 标签
- 上下文处理器

### 1.8 表单处理（Forms）

```python
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
```

- 表单类型
- 字段验证
- 表单渲染
- ModelForm

### 1.9 认证系统（Authentication）

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def create_post(request):
    # 视图逻辑

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
```

- 用户认证
- 权限系统
- 装饰器和混入类
- 会话管理

## 2. 高级特性

### 2.1 中间件（Middleware）

```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 请求处理前的逻辑
        response = self.get_response(request)
        # 响应处理后的逻辑
        return response
```

- 请求/响应处理
- 异常处理
- 会话处理
- 认证处理

### 2.2 信号系统（Signals）

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        # 处理新创建的文章
        pass
```

- 内置信号
- 自定义信号
- 信号接收器
- 异步信号

### 2.3 缓存系统（Cache）

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
```

- 缓存后端
- 视图缓存
- 模板片段缓存
- 底层缓存API

### 2.4 管理站点（Admin）

```python
from django.contrib import admin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
```

- 模型注册
- 自定义显示
- 过滤和搜索
- 自定义操作

## 3. 最佳实践

### 3.1 项目组织

- 应用划分
- 配置管理
- 代码复用
- 版本控制

### 3.2 性能优化

- 数据库优化
- 缓存策略
- 静态文件处理
- 延迟加载

### 3.3 安全考虑

- CSRF保护
- XSS防护
- SQL注入防护
- 密码存储

### 3.4 测试策略

- 单元测试
- 集成测试
- 测试客户端
- 测试覆盖率

## 4. 部署指南

### 4.1 生产环境配置

```python
# production_settings.py
DEBUG = False
ALLOWED_HOSTS = ['example.com']
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'
```

### 4.2 WSGI/ASGI服务器

```bash
# 使用Gunicorn
gunicorn blog.wsgi:application

# 使用Daphne（ASGI）
daphne blog.asgi:application
```

### 4.3 静态文件部署

```bash
python manage.py collectstatic
```

## 5. 常见问题解决

### 5.1 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5.2 静态文件处理

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 5.3 错误处理

```python
# urls.py
handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.server_error'
``` 