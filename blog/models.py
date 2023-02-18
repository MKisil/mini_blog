from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField


class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager,
                     self).get_queryset().select_related('user')


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Стаття')
    author = models.ForeignKey('Author', verbose_name='Автор статті', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name='Дата публікації')
    slug = AutoSlugField(populate_from='title', max_length=255, unique=True, db_index=True, verbose_name="URL")
    draft = models.BooleanField('Чернетка', default=True, auto_created=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        get_latest_by = 'date'
        ordering = ['-date']


class Author(models.Model):
    user = models.OneToOneField(User, verbose_name='Користувач, який є автором', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=70, verbose_name='Ім\'я автора')
    biography = models.TextField('Біографія')
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'
        ordering = ['name']


class Comment(models.Model):
    objects = CommentManager()
    article = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name='Стаття')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    text = models.TextField(verbose_name='Коментар')

    def __str__(self):
        return f"Коментарій до статті - {self.article}"

    class Meta:
        verbose_name = 'Коментарій'
        verbose_name_plural = 'Коментарії'
