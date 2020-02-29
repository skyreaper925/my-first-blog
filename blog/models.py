from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    # создаём поля для объекта модели поста, который будет находится в бд
    title = models.CharField("Тема консультации", max_length=200)  # ограниченый размер переменной
    text = models.TextField("Раскрытие темы")  # текст для поста
    published_date = models.DateTimeField(blank=True, null=True)  # дата
    likes = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class UserModel(AbstractUser):
    form = models.CharField(max_length=2)
    # grades = models.IntegerField(default=0)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Consultation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    creation = models.DateTimeField(default=timezone.now, editable=False)
    date = models.DateTimeField("Дата проведения лекции-консультации", default=timezone.now)
    email = models.EmailField("Ваша почта",
                              default="")  # предназначен для ввода адреса электронной почты и создает следующую разметку:
    theme = models.TextField("Общая тема лекции-консультации", default="")  # ограниченый размер переменной
    description = models.TextField("Подробное раскрытие темы", default="")
    spectators = models.TextField("Целевая аудитория", default="")
    duration = models.TimeField("Продолжительность в формате HH:MM", default=timezone.now)  # формат "DD HH:MM:SS
    members = models.ManyToManyField(UserModel, related_name='+')  # участники консультации
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, default="", blank=True, null=True)
    contact = models.IntegerField('Форма взаимодействия', choices=[(1, "Очно"), (2, "Заочно")], default="")
    place = models.CharField('Место проведения', max_length=20, default="")

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme


class Comment(models.Model):
    class Meta:
        db_table = "comments"

    path = ArrayField(models.IntegerField())
    article_id = models.ForeignKey(Article)
    author_id = models.ForeignKey(User)
    content = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата комментария', default=timezone.now)

    def __str__(self):
        return self.content[0:255]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level
