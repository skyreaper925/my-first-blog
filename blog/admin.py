from django.contrib import admin
from .models import Post, User, Consultation

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Consultation)