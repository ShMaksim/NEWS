import pytz
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.utils.translation import gettext as _
from django.utils import timezone
from django.http.response import HttpResponse

class Index(View):
    def get(self, request):
        current_time = timezone.now()
        categories = Category.objects.all()
        context = {
            'current_time': current_time,
            'timezones': pytz.common_timezones,
            'categories': categories,
        }
        return HttpResponse(render(request, 'index.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        context['current_time'] = current_time
        context['next_news'] = _("Latest news every Wednesday!")
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
        messages.info(request, _('You are already subscribed to this category'))
    else:
        category.subscribers.add(request.user)
        messages.success(request, _('You have successfully subscribed to a category %(category_name)s.') % {'category_name': category.name})
    return redirect('news_list')

class NewsListView(View):
    def get(self, request):
        news_list = Post.objects.filter(post_type='news').order_by('-created_at')
        categories = Category.objects.all()

        context = {
            'news_list': news_list,
            'categories': categories,
        }

        return render(request, 'news/news_list.html', context)

