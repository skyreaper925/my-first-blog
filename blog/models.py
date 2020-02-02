from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
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
    period = models.IntegerField('Тип мероприятия', choices=[(1, "Лекция"), (2, "Курс")], default=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation = models.DateTimeField(default=timezone.now, editable=False)
    date = models.DateTimeField('Дата проведения лекции-консультации', default=timezone.now)
    email = models.EmailField('Ваша почта')
    # предназначен для ввода адреса электронной почты и создает следующую разметку:
    theme = models.TextField('Общая тема лекции-консультации')  # ограниченый размер переменной
    description = models.TextField('Подробное раскрытие темы')
    contact = models.IntegerField('Форма взаимодействия', choices=[(1, "Очно"), (2, "Заочно")], default=1)
    place = models.CharField('Место проведения', max_length=20, default="Кабинет №")
    spectators = models.TextField('Целевая аудитория')
    duration = models.TimeField('Продолжительность', default='0:45')  # формат "DD HH:MM:SS

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme

# python manage.py createsuperuser
# Имя пользователя: skyreaper
# Адрес электронной почты: volodinmaxim1995@gmail.com
# Password:
# Password (again):
