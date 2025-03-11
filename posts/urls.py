from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
] 