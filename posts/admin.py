from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_time']
    fields = ['name', 'description']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_time', 'modified_time', 'views']
    fields = ['title', 'content', 'excerpt', 'category', 'author']

    def save_model(self, request, obj, form, change):
        if not change:  # 新增文章时
            obj.author = request.user
        super().save_model(request, obj, form, change)
