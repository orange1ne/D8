from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView
)
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
from .filters import PostFilter, PostCategoryFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostCategoryFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_politics_sub'] = not self.request.user.groups.filter(name='politics_subs').exists()
        context['is_not_music_sub'] = not self.request.user.groups.filter(name='music_subs').exists()
        context['is_not_sport_sub'] = not self.request.user.groups.filter(name='sport_subs').exists()
        context['is_not_education_sub'] = not self.request.user.groups.filter(name='education_subs').exists()
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

                html_content = render_to_string(
                    'post_created.html',
                    {
                        'post': request.POST,
                    }
                )
                post_category = str(list((Category.objects.filter(id=int(request.POST['post_category']))))[0])
                group = post_category.lower() + '_subs'
                receivers = []
                for user in User.objects.filter(groups__name=group):
                    receivers.append(user.email)
                msg = EmailMultiAlternatives(
                    subject=request.POST['name'],
                    body=request.POST['text'],
                    from_email='',
                    to=[receivers],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # send_mail(
                #     subject=request.POST['name'],
                #     message=request.POST['text'],
                #     from_email='',
                #     recipient_list=[receivers],
                # )

                return HttpResponseRedirect('/news/post/create')
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.category = 'news'
                form.save()

                html_content = render_to_string(
                    'post_created.html',
                    {
                        'post': request.POST,
                    }
                )
                post_category = str(list((Category.objects.filter(id=int(request.POST['post_category']))))[0])
                group = post_category.lower() + '_subs'
                receivers = []
                for user in User.objects.filter(groups__name=group):
                    receivers.append(user.email)
                msg = EmailMultiAlternatives(
                    subject=request.POST['name'],
                    body=request.POST['text'],
                    from_email='',
                    to=[receivers],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # send_mail(
                #     subject=request.POST['name'],
                #     message=request.POST['text'],
                #     from_email='',
                #     recipient_list=[receivers],
                # )

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


@login_required
def subscribe_pol(request):
    user = request.user
    politics = Group.objects.get(name='politics_subs')
    if not request.user.groups.filter(name='politics_subs').exists():
        politics.user_set.add(user)
    return redirect('http://127.0.0.1:8000/news/?post_category=1')


@login_required
def subscribe_music(request):
    user = request.user
    politics = Group.objects.get(name='music_subs')
    if not request.user.groups.filter(name='music_subs').exists():
        politics.user_set.add(user)
    return redirect('http://127.0.0.1:8000/news/?post_category=2')


@login_required
def subscribe_sport(request):
    user = request.user
    politics = Group.objects.get(name='sport_subs')
    if not request.user.groups.filter(name='sport_subs').exists():
        politics.user_set.add(user)
    return redirect('http://127.0.0.1:8000/news/?post_category=3')


@login_required
def subscribe_edu(request):
    user = request.user
    politics = Group.objects.get(name='education_subs')
    if not request.user.groups.filter(name='education_subs').exists():
        politics.user_set.add(user)
    return redirect('http://127.0.0.1:8000/news/?post_category=4')
