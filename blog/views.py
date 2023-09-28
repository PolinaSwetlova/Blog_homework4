from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from blog.models import Category, Post, Comment, User
from django.db.models import Q
from .forms import PostForm, CommentForm, UserForm
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, Http404


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)

@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user == comment.author:
            comment.delete()
            return redirect('blog:post_detail', pk=pk)
    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)


def index(request):
    template_name = 'blog/index.html'
    page_obj = Post.sorting_objects.select_related(
        'author', 'location', 'category'
    ).filter(category__is_published=True
             ).order_by('-pub_date')
    paginator = Paginator(page_obj, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template_name, context)
    
@login_required
def profile(request, username):
    template_name = 'blog/post_list.html'
    #profile = User.objects.get(username=username)
    try:
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'pages/404.html', status=404)
    user_post = get_list_or_404(
        Post.sorting_objects.select_related(
            'author', 'location', 'category'
        ).filter(
            author__username=username,
            is_published = True
        ).order_by('-pub_date')
    )
    paginator = Paginator(user_post, 10)
    page_number = request.GET.get('page')
    user_post = paginator.get_page(page_number)
    context = {'profile': profile,
               'page_obj': user_post}
    return render(request, template_name, context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            profile_url = reverse('blog:profile', args=[request.user.username])
            return redirect(profile_url)
    else:
        form = UserForm(instance=request.user)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


class PostFormMixin:
    form_class = PostForm
    template_name = 'blog/create.html'


class PostListView(ListView):
    model = Post
    paginate_by = 10
    ordering = 'created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 


class PostCreateView(PostFormMixin, CreateView):
    model = Post

    def get_success_url(self):
        post = self.object
        return reverse_lazy('blog:post_detail', kwargs={'pk': post.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.pub_date <= timezone.now():
            form.instance.is_published = True
        return super().form_valid(form)


class PostUpdateView(PostFormMixin, UpdateView):
    model = Post

    def get_success_url(self):
        post = self.object
        return reverse_lazy('blog:post_detail', kwargs={'pk': post.pk})
        
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    ordering = 'created_at'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context
    

def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category_post = get_list_or_404(
        Post.sorting_objects.select_related(
            'author', 'location', 'category'
        ).filter(
            category__slug=category_slug).order_by('-pub_date'),
        category__is_published=True
    )
    paginator = Paginator(category_post, 10)
    page_number = request.GET.get('page')
    category_post = paginator.get_page(page_number)
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(
            slug=category_slug,
            is_published=True)
    )
    context = {'category': category,
               'page_obj': category_post}
    return render(request, template_name, context)
