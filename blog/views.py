from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import PostForm, ConsultationForm, SignUp
from .models import Post, Consultation, UserModel


def post_list(request):
    posts = Post.objects.order_by('-likes')
    return render(request, 'blog/suggs_list.html', {'posts': posts})


def cons_list(request):
    consultations = Consultation.objects.order_by('-creation')
    print(consultations)
    return render(request, 'blog/post_list.html', {'consultations': consultations})

def post_detail(request, pk):  # новое представление данных 
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def user_new(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
    else:
        form = SignUp()
    return render(request, 'blog/signup.html', {'form': form})


def cons_new(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.owner = request.user
            consultation.creation = timezone.now()
            consultation.email = request.user.email
            consultation.save()
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm()
    return render(request, 'blog/consultation_edit.html', {'form': form})

def cons_detail(request, pk):  # новое представление данных 
    consultation = get_object_or_404(Consultation, pk = pk)
    return render(request, 'blog/consultation_detail.html', {'consultation': consultation})


def cons_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.user != consultation.owner:
        return render(request, 'blog/consultation_detail_not_owner.html', {'consultation': consultation})
    else:
        return render(request, 'blog/consultation_detail.html', {'consultation': consultation})

def cons_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save(commit=True)
            consultation.owner = request.user
            consultation.save()
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'blog/consultation_edit.html', {'form': form})


def profile(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'blog/profile.html', {'consultation': consultation})


def main_profile(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'blog/main_profile.html', {'cons': cons})


def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return HttpResponseRedirect("suggs/")


# def grades(request, pk):
#     user = get_object_or_404(UserModel, pk = pk)
#     user.grades += 1
#     user.save()
#     return HttpResponseRedirect("profile/")

def delete_cons(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return HttpResponseRedirect("/profile/")


def profile_edit(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == "POST":
        form = SignUp(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
    else:
        form = SignUp(instance=user)
    return render(request, 'blog/profile_edit.html', {'form': form})

# 1) выяснить, почему пользователь начинает существовать только после входа, а не после регистрации
# 2) выяснить, почему не работает редактирование модели пользователя (редактирует, но потом не может вернуться на main_profile)
# 3) Добавить грейды
# 4) deploy to heroku
