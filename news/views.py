from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category
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
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['categories'] = post.categories.all()
        return context

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

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_Post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


    def form_valid(self, form):
        form.instance.post_type = 'news'
        response = super().form_valid(form)
        form.instance.categories.set(form.cleaned_data['categories'])
        return response

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_Post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.categories.set(form.cleaned_data['categories'])
        return response


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

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user in category.subscribers.all():
        messages.info(request,'Вы уже подписаны на данную категорию')
    else:
        category.subscribers.add(request.user)
        messages.success(request, f'Вы успешно подписались на категорию {category.name}.')
    return redirect('news_list')

