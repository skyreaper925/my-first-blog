from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    # создаём поля для объекта модели поста, который будет находится в бд
    title = models.CharField("Тема консультации", max_length=200)  # ограниченый размер переменной
    text = models.TextField("Раскрытие темы")  # текст для поста
    published_date = models.DateTimeField(blank=True, null=True)  # дата
    good_date = models.DateTimeField("Удобная дата проведения", default=timezone.now)  # удобная дата проведения
    likes = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class UserModel(AbstractUser):
    form = models.CharField(max_length=2)
    vk = models.CharField(max_length=200, default="", blank=True, null=True)
    # grades = models.IntegerField(default=0)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    text = models.TextField("Раскрытие темы", max_length=140)  # текст для поста
    published_date = models.DateTimeField(blank=True, null=True)  # дата

class Consultation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    creation = models.DateTimeField(default=timezone.now, editable=False)
    memberCount = models.IntegerField('Количество участников', default=0, editable=False)
    date = models.DateTimeField("Дата проведения лекции-консультации", default=timezone.now)
    email = models.EmailField("Ваша почта", default="")  # предназначен для ввода адреса электронной почты
    theme = models.TextField("Общая тема лекции-консультации", default="")
    description = models.TextField("Подробное раскрытие темы", default="")
    spectators = models.TextField("Целевая аудитория", default="")
    duration = models.CharField('Продолжительность консультации', max_length=20, default="")
    members = models.ManyToManyField(UserModel, related_name='+')  # участники консультации
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, default="", blank=True, null=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, default="", blank=True, null=True)
    contact = models.IntegerField('Форма взаимодействия', choices=[(1, "Очно"), (2, "Заочно")], default="")
    place = models.CharField('Место проведения', max_length=20, default="")
    hashtag = models.CharField('Место проведения', max_length=200, default="")
    hashtags = []

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme


class Review(models.Model):
    name = models.CharField(max_length=300, verbose_name='Имя')
    born = models.DateField(default=timezone.now, verbose_name='Дата создания')
    cons = models.ForeignKey(Consultation, verbose_name='Школа')
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default='5', verbose_name='Рейтинг')
    body = models.TextField(verbose_name='Описание')
    email = models.EmailField()
    verificated = models.BooleanField(default=False, verbose_name='Активен')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __unicode__(self):
        return u'%s' % self.name
