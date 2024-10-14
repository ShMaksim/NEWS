from django.urls import path
from .views import NewsListView, NewsDetailView, PostSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView
from .views import subscribe_to_category
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('',cache_page(60)(NewsListView.as_view()), name='news_list'),
    path('<int:pk>/', cache_page(300)(NewsDetailView.as_view()), name='news_detail'),
    path('search/', cache_page(300)(PostSearchView.as_view()), name='news_search'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),
]

