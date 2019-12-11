from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    # создаём поля для объекта модели поста, который будет находится в бд
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # ссылка на другую модель
    title = models.CharField(max_length=200) # ограниченый размер переменной
    text = models.TextField() # текст для поста
    created_date = models.DateTimeField(default=timezone.now) # дата
    published_date = models.DateTimeField(blank=True, null=True) # дата

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=100) # ограниченый размер переменной, потому что user не должен быть большим
    password = models.TextField() # пароль может быть любой длины

    def __str__(self):
        return self.username
    

    def publish(self):
        self.save()

class Consultation(models.Model):
    creation = models.DateTimeField(default=timezone.now) 
    date = models.DateTimeField(default=timezone.now) 
    email = models.EmailField() #предназначен для ввода адреса электронной почты и создает следующую разметку:
    theme = models.TextField()  # ограниченый размер переменной
    discription = models.TextField() 
    spectators = models.TextField() 
    longliness = models.DurationField("longliness в формате DD HH:MM:SS") #формат "DD HH:MM:SS

    def publish(self):
        self.creation = timezone.now()
        self.save()


    def __str__(self):
        return self.theme