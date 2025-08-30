from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='post_list'),
    path("custom-blog", views.ArticleListCustomBenchmarkView.as_view(), name='post_list_custom')
]
