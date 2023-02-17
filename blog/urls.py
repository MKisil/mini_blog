from django.urls import path

from blog.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('articles/', ListArticle.as_view(), name='list_blogs'),
    path('article/<slug:slug_article>/', BlogDetail.as_view(), name='blog_detail'),
    path('authors/', ListAuthor.as_view(), name='list_authors'),
    path('author/<slug:author>', AuthorDetail.as_view(), name='author_detail'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add-comment/', CommentCreate.as_view(), name='add_comment'),
    path('edit-comment/<slug:slug_article>/<int:pk>/', CommentUpdate.as_view(), name='edit_comment'),
    path('delete-comment/<slug:slug_article>/<int:pk>/', CommentDelete.as_view(), name='delete_comment'),
    path('create-author/', AuthorCreate.as_view(), name='create_author'),
    path('create-article/<int:author_id>/', ArticleCreate.as_view(), name='create_article'),
    path('success_article/', SuccessArticleCreate.as_view(), name='success_article_create'),
    path('limit_article/', LimitArticleCreate.as_view(), name='limit_article'),
    path('my_article/', MyArticle.as_view(), name='my_articles'),
    path('delete_article/<int:pk>/', DeleteArticle.as_view(), name='delete_article'),
]
