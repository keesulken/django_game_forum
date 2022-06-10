from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # одна из 2-х вещей,
    # которые я хотел бы пофиксить, это чтобы автор тоже содержал username. Если вы это читаете, значит я ещё не
    # повторил материал по гитхабу и не исправил это, а то на рефакторинге я слишком поздно понял, что мне это нужно
    # и очень не хотелось сносить БД ещё раз)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating = 0  # можно и обнулять self.rating в принципе, главное, чтобы наша функция не добавляла автору
        # рейтинга при каждом её применении
        author_posts = Post.objects.filter(author=self)
        author_comments = Comment.objects.filter(author=self.user)
        for comm in author_comments:
            sum_rating += comm.rating
        for post in author_posts:
            sum_rating += post.rating*3
            if Comment.objects.filter(related_post=post).exists():
                for j in Comment.objects.filter(related_post=post):
                    sum_rating += j.rating
        self.rating = sum_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    ARTICLES = 'Articles'
    NEWS = 'News'
    post_types = [(ARTICLES, 'Статьи'), (NEWS, 'Новости')]
    author = models.ForeignKey(Author, on_delete=models.SET('deleted'))  # вторая вещь. Я слишком поздно вспомнил,
    # что хотел проверить, будет ли оно работать. Просто в документации в качестве аргумента обычно передавалась
    # внеклассовая функция, так что я не уверен, будет ли хватать просто строки. Но логика, думаю, ясна - если автор
    # удалён, то просто вместо username отображем нужное значение
    type = models.CharField(max_length=64, choices=post_types)
    publishing_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('PostCategory')
    title = models.CharField(max_length=256)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'  # 124 же? Или 125? Или 123? Надо будет посчитать...

    def __str__(self):
        return f'{self.title[:25]}'

    def get_absolute_url(self):
        return f'/news/{self.pk}'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET('deleted'))  # комменты думаю тоже есть смысл оставлять,
    # если автор удалён
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
