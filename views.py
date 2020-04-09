from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import PostForm, ConsultationForm, SignUp, FilterDate
from .models import Post, Consultation, UserModel


def post_list(request):
    posts = Post.objects.order_by('-likes')
    return render(request, 'suggestions/list_suggs.html', {'posts': posts, 'request': request})


def comment_list(request):
    comments = Comment.objects.order_by('-likes')
    return render(request, 'suggestions/list_suggs.html', {'comments': comments, 'request': request})


def cons_list(request):
    consultations = Consultation.objects.order_by('-creation')
    form = FilterDate(request.GET)
    if form.is_valid():
        if form.cleaned_data["dateFrom"]:
            consultations = consultations.filter(date__gte=form.cleaned_data["dateFrom"])
        if form.cleaned_data["dateTo"]:
            consultations = consultations.filter(date__lte=form.cleaned_data["dateTo"])
        if form.cleaned_data["search"]:
            if ' ' in form.cleaned_data["search"]:
                consultations = consultations.annotate(similarity=Greatest(
                    TrigramSimilarity('theme', form.cleaned_data["search"]),
                    TrigramSimilarity('description', form.cleaned_data["search"]))).filter(
                    similarity__gte=0.1).order_by('-similarity')

                # consultations = consultations.annotate(
                #     similarity=TrigramSimilarity('theme', form.cleaned_data["search"]), ).filter(
                #     similarity__gte=0.1).order_by('-similarity')
            else:
                vector = SearchVector('theme', weight='A') + SearchVector('description', weight='B')
                # или там, или там, или вместе
                query = SearchQuery(form.cleaned_data["search"])
                consultations = consultations.annotate(rank=SearchRank(vector, query)). \
                    filter(rank__gte=0.1).order_by('-rank')
        if form.cleaned_data["contact"]:
            consultations = consultations.filter(contact=int(form.cleaned_data["contact"][0]))
        if form.cleaned_data["hashtags"]:
            q_lst = form.cleaned_data["hashtags"][1:len(form.cleaned_data["hashtags"])].split("#")
            print(q_lst)
            consultations = consultations.filter(hashtag__in=q_lst)
    return render(request, 'consultations/main.html',
                  {'request': request, 'consultations': consultations, 'form': form})


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
        return render(request, 'suggestions/new_sugg.html', {'form': form})
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
    return render(request, 'suggestions/post_edit.html', {'form': form})


def post_detail(request, pk):  # новое представление данных
    post = get_object_or_404(Post, pk=pk)
    conses = Consultation.objects.filter(posts=post)
    if request.user == post.author:
        return render(request, 'suggestions/sugg_detail.html', {'post': post, 'conses': conses})
    else:
        return render(request, 'suggestions/sugg_detail.html', {'post': post, 'conses': conses})


def user_new(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
    else:
        form = SignUp()
    return render(request, 'user/signup.html', {'form': form})


def cons_new(request):
    if request.user.username:
        if request.method == "POST":
            form = ConsultationForm(request.POST)
            if form.is_valid():
                consultation = form.save(commit=False)
                consultation.owner = request.user
                consultation.creation = timezone.now()
                consultation.email = request.user.email
                consultation.hashtag = consultation.hashtag[1:len(consultation.hashtag)].split("#")
                print(consultation.hashtag)
                consultation.save()
                return redirect('consultation_detail', pk=consultation.pk)
        else:
            form = ConsultationForm()
        return render(request, 'consultations/create_consultation.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


def cons_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.user != consultation.owner:
        return render(request, 'consultations/consultation_notOwner.html',
                      {'consultation': consultation}, {'memberCount': consultation.memberCount})
    else:
        return render(request, 'consultations/consultation_owner.html',
                      {'consultation': consultation, 'members': consultation.members.all()},
                      {'memberCount': consultation.memberCount})


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
    return render(request, 'consultations/create_consultation.html', {'form': form})


def profile(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'user/profile.html', {'consultation': consultation})


def main_profile(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'user/main_profile.html', {'cons': cons})


def my_conses(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'consultations/my_conses.html', {'cons': cons})


def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.username:
        post.likes += 1
        post.save()
        return HttpResponseRedirect("suggs/")
    else:
        return HttpResponseRedirect("login/")


# def grades(request, pk):  
#     user = get_object_or_404(UserModel, pk = pk)
#     user.grades += 1
#     user.save()
#     return HttpResponseRedirect("profile/")

def delete_cons(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return HttpResponseRedirect("/myconses/")


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
    return render(request, 'user/profile_edit.html', {'form': form})


def new_member(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if request.user.username:
        cons.members.add(request.user)
        cons.memberCount += 1
        cons.save()
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/")


def bye_member(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if request.user.username in cons.members:
        cons.members.remove(request.user)
        cons.memberCount -= 1
        cons.save()
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/")


def similar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    conses = Consultation.objects.filter(posts=post)
    return render(request, 'suggestions/similar.html', {'conses': conses})


def create(request, pk):
    if request.user.username:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = ConsultationForm(request.POST)
            if form.is_valid():
                consultation = form.save(commit=False)
                consultation.owner = request.user
                consultation.creation = timezone.now()
                consultation.email = request.user.email
                consultation.posts = post
                consultation.save()
                return redirect('consultation_detail', pk=consultation.pk)
        else:
            form = ConsultationForm()
        return render(request, 'consultations/create_consultation.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


class ReviewAdd(CreateView):
    model = Review
    form_class = ReviewAddForm
    # template_name = 'school/review_add.html'
    success_url = 'reviewsend'

    def form_valid(self, form):
        obj = form.save(commit=False)
        cons = get_object_or_404(Consultation)
        # cons = get_object_or_404(Consultation, slug=self.kwargs['slug'])
        obj.cons = cons
        obj.save()
        slug = self.kwargs['slug']
        subject = 'Отзыв'
        # message = u'Перейдите по ссылке для активации отзыва ' +
        # 'http://ваш_сайт/school/' + '%s' % slug + '/verification/' + '%s' % obj.id
        email = form.cleaned_data['email']
        from_email = 'info@vodibezopasno.com'
        send_mail(subject, message, from_email, [email, ])
        return super(ReviewAdd, self).form_valid(form)
