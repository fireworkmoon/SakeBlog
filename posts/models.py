from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField('分类名', max_length=100)
    description = models.TextField('描述', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    """博客文章模型"""
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField('阅读量', default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加阅读量"""
        self.views += 1
        self.save(update_fields=['views'])
