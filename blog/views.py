from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import CommentForm
from .forms import PostForm, ConsultationForm, SignUp
from .models import Comment
from .models import Post, Consultation, UserModel


def post_list(request):
    posts = Post.objects.order_by('-likes')
    return render(request, 'blog/suggs_list.html', {'posts': posts})


def cons_list(request):
    consultations = Consultation.objects.order_by('-creation')
    return render(request, 'main/main.html', {'consultations': consultations})


def cons_list2(request):
    consultations = Consultation.objects.order_by('-creation')
    return render(request, 'blog/post_list.html', {'consultations': consultations})


def post_new(request):
    if request.user.username:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


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


def post_detail(request, pk):  # новое представление данных
    post = get_object_or_404(Post, pk=pk)
    conses = Consultation.objects.filter(posts=post)
    if request.user == post.author:
        return render(request, 'blog/post_detail.html', {'post': post, 'conses': conses})
    else:
        return render(request, 'blog/post_detail_not_owner.html', {'post': post, 'conses': conses})


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
    if request.user.username:
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
    else:
        return HttpResponseRedirect('login')


def cons_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.user != consultation.owner:
        return render(request, 'blog/consultation_detail_not_owner.html', {'consultation': consultation})
    else:
        return render(request, 'blog/consultation_detail.html',
                      {'consultation': consultation, 'members': consultation.members.all()})


def cons_edit(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=cons)
        if form.is_valid():
            cons = form.save(commit=True)
            cons.owner = request.user
            cons.save()
            return redirect('consultation_detail', pk=cons.pk)
    else:
        form = ConsultationForm(instance=cons)
    return render(request, 'blog/consultation_edit.html', {'form': form})


def profile(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'blog/profile.html', {'consultation': consultation})


def main_profile(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'blog/main_profile.html', {'cons': cons})


liked = []


def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user not in liked:
        post.likes += 1
        liked.append(request.user)
    else:
        post.likes -= 1
    post.save()
    return HttpResponseRedirect("suggs/")


def grades(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    user.grades += 1
    user.save()
    return HttpResponseRedirect("profile/")


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


def new_member(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if request.user.username:
        cons.members.add(request.user)
        cons.save()
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/")


def create(request, pk):
    cons = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            cons = form.save(commit=False)
            cons.owner = request.user
            cons.creation = timezone.now()
            cons.email = request.user.email
            cons.save()
            return redirect('consultation_detail', pk=cons.pk)
    else:
        form = ConsultationForm()
    return render(request, 'blog/consultation_edit.html', {'form': form})


def comment(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    cons.comments += CharField()
    cons.save()
    return redirect("consultation_detail", pk=cons.pk)


template_name = 'post/article.html'
comment_form = CommentForm


def get(self, request, *args, **kwargs):
    article = get_object_or_404(Consultation, id=self.kwargs['article_id'])
    context = {}
    context.update(csrf(request))
    user = request.user
    # Помещаем в контекст все комментарии, которые относятся к статье
    # попутно сортируя их по пути, ID автоинкрементируемые, поэтому
    # проблем с иерархией комментариев не должно возникать
    context['comments'] = article.comment_set.all().order_by('path')
    context['next'] = article.get_absolute_url()
    # Будем добавлять форму только в том случае, если пользователь авторизован
    if user.is_authenticated:
        context['form'] = self.comment_form

    return render_to_response(template_name=self.template_name, context=context)


# Декораторы по которым, только авторизованный пользователь
# может отправить комментарий и только с помощью POST запроса
@login_required
@require_http_methods(["POST"])
def add_comment(request, article_id):
    form = CommentForm(request.POST)
    article = get_object_or_404(Consultation, id=article_id)

    if form.is_valid():
        comment = Comment()
        comment.path = []
        comment.article_id = article
        comment.author_id = request.user
        comment.content = form.cleaned_data['comment_area']
        comment.save()

        # Django не позволяет увидеть ID комментария по мы не сохраним его,
        # хотя PostgreSQL имеет такие средства в своём арсенале, но пока не будем
        # работать с сырыми SQL запросами, поэтому сформируем path после первого сохранения
        # и пересохраним комментарий
        try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment.id)
        except ObjectDoesNotExist:
            comment.path.append(comment.id)

        comment.save()

    return redirect(article.get_absolute_url())

# 1) выяснить, почему пользователь начинает существовать только после входа, а не после регистрации
# 2) выяснить, почему не работает редактирование модели пользователя (редактирует, но потом не может вернуться на main_profile)
# 3) Добавить грейды
