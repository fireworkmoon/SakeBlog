# Django博客项目实践指南

## 1. 项目概述

### 1.1 功能特性
- 用户认证系统
- 博客文章管理
- 文章分类
- 分页显示
- 响应式界面

### 1.2 技术栈
- Django：Web框架
- SQLite：数据库
- Bootstrap：前端框架
- Django模板：前端渲染

## 2. 代码解析

### 2.1 用户认证实现
```python
# models.py
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# views.py
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```
- 使用Django内置用户系统
- 权限控制
- 表单处理

### 2.2 文章管理实现
```python
# models.py
class Post(models.Model):
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']

# views.py
class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
```
- 模型设计
- 列表视图
- 详情视图
- 分页功能

### 2.3 分类系统实现
```python
# models.py
class Category(models.Model):
    name = models.CharField('分类名', max_length=100)
    description = models.TextField('描述', blank=True)

# views.py
class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Post.objects.filter(category=cate)
```
- 分类模型
- 分类视图
- 关联查询

## 3. 项目扩展建议

### 3.1 添加评论功能
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
```

### 3.2 添加标签系统
```python
class Tag(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')
```

### 3.3 添加搜索功能
```python
from django.db.models import Q

def post_search(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )
```

## 4. 性能优化

### 4.1 数据库优化
```python
# 使用select_related减少查询
posts = Post.objects.select_related('author', 'category').all()

# 添加索引
class Post(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['created_time']),
            models.Index(fields=['title']),
        ]
```

### 4.2 缓存实现
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})
```

### 4.3 模板优化
```html
{% load static %}
{% cache 300 sidebar %}
    {# 侧边栏内容 #}
{% endcache %}
```

## 5. 测试指南

### 5.1 模型测试
```python
from django.test import TestCase

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.category = Category.objects.create(name='测试')

    def test_post_creation(self):
        post = Post.objects.create(
            title='测试文章',
            content='测试内容',
            author=self.user,
            category=self.category
        )
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.title)
```

### 5.2 视图测试
```python
class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
```

## 6. 部署注意事项

### 6.1 安全设置
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# 设置安全中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

# 启用HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 6.2 静态文件处理
```python
# settings.py
STATIC_ROOT = '/var/www/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 收集静态文件
python manage.py collectstatic
```

### 6.3 数据库配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
    }
}
```

## 7. 常见问题解决

### 7.1 数据迁移
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 回滚迁移
python manage.py migrate posts 0001
```

### 7.2 静态文件问题
```python
# 开发环境
DEBUG = True
STATICFILES_DIRS = [BASE_DIR / 'static']

# 生产环境
DEBUG = False
STATIC_ROOT = '/var/www/static/'
```

### 7.3 性能问题
```python
# 使用查询优化器
from django.db.models import Prefetch

posts = Post.objects.prefetch_related(
    Prefetch('comments', queryset=Comment.objects.select_related('author'))
)

# 使用缓存
from django.core.cache import cache

def get_post_cache(post_id):
    key = f'post_{post_id}'
    post = cache.get(key)
    if post is None:
        post = Post.objects.get(id=post_id)
        cache.set(key, post, 3600)
    return post
``` 