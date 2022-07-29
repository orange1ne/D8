from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView
)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
@permission_required('news.add_post', raise_exception=True)
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        if 'post' in request.path:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.category = 'post'
                form.save()
                return HttpResponseRedirect('/news/post/create')
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.category = 'news'
                form.save()
                return HttpResponseRedirect('/news/news/create')

    return render(request, 'post_create.html', {'form': form})


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'
