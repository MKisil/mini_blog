from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import *

from blog.forms import *
from blog.models import Blog, Author, Comment
import datetime


class Home(TemplateView):
    template_name = 'blog/index.html'


class ListArticle(ListView):
    model = Blog
    paginate_by = 3

    def get_queryset(self):
        queryset = cache.get('queryset')

        if not queryset:
            queryset = Blog.objects.filter(draft=False).select_related('author')
            cache.set('queryset', queryset, 600)

        return queryset


class ListAuthor(ListView):
    model = Author
    paginate_by = 3

    def get_context_data(self, **kwargs):
        object_list = cache.get('object_list')

        if not object_list:
            object_list = Author.objects.filter(blog__draft=False).distinct()
            cache.set('object_list', object_list, 900)

        return super().get_context_data(object_list=object_list, **kwargs)


class BlogDetail(DetailView):
    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug_article'


class AuthorDetail(DetailView):
    model = Author
    slug_field = 'slug'
    slug_url_kwarg = 'author'


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request, *args):
    logout(request)
    return redirect('home')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CommentCreate(View):

    def post(self, request, *args, **kwargs):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.META.get('HTTP_REFERER'))


class CommentUpdate(UpdateView):
    model = Comment
    form_class = EditCommentForm
    template_name = 'blog/cud/comment_edit.html'

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'slug_article': self.kwargs['slug_article']})


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'blog/cud/comment_delete.html'

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'slug_article': self.kwargs['slug_article']})


class AuthorCreate(CreateView):
    model = Author
    form_class = CreateAuthorForm
    template_name = 'blog/cud/author_create.html'

    def get_success_url(self, author_id):
        return reverse('create_article', kwargs={'author_id': author_id})

    def form_valid(self, form):
        author = form.save(commit=False)
        author.save()
        return redirect(self.get_success_url(author.id))


class ArticleCreate(CreateView):
    model = Blog
    form_class = CreateArticleForm
    template_name = 'blog/cud/article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author_id = self.kwargs.get('author_id')
        article.save()
        try:
            from .tools import send_telegram, make_msg
            send_telegram(make_msg(article))
        except ImportError:
            pass
        return redirect('success_article_create')

    def get(self, request, *args, **kwargs):
        author = Author.objects.get(pk=kwargs['author_id'])

        if author.blog_set.exists():
            if author.blog_set.latest().date == datetime.date.today():
                return redirect('limit_article')
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)


class SuccessArticleCreate(TemplateView):
    template_name = 'blog/messages/success_article_create.html'


class LimitArticleCreate(TemplateView):
    template_name = 'blog/messages/limit_article_create.html'


class MyArticle(TemplateView):
    template_name = 'blog/author_articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published_articles'] = self.request.user.author.blog_set.filter(draft=False)
        context['unpublished_articles'] = self.request.user.author.blog_set.filter(draft=True)
        return context


class DeleteArticle(DeleteView):
    model = Blog
    template_name = 'blog/cud/article_delete.html'
    success_url = reverse_lazy('home')
