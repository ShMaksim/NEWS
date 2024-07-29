from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = "Свежие новости каждую среду!"
        return context

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
