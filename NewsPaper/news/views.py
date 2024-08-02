from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 2

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

class PostSearchView(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news_search_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(post_type='news')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

class NewsCreateView(PostCreateView):
    post_type = 'news'

class NewsUpdateView(PostUpdateView):
    pass

class NewsDeleteView(PostDeleteView):
    pass

class ArticleCreateView(PostCreateView):
    post_type = 'article'

class ArticleUpdateView(PostUpdateView):
    pass

class ArticleDeleteView(PostDeleteView):
    pass


