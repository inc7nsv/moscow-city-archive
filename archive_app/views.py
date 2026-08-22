from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, FeedbackForm, RegisterForm
from .models import AboutPage, Article, ContactsPage


def home(request):
    query = request.GET.get('q', '').strip()
    articles = Article.objects.filter(is_published=True).prefetch_related('blocks')

    if query:
        articles = articles.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(blocks__text__icontains=query)
        ).distinct()

    return render(request, 'archive_app/home.html', {'articles': articles, 'query': query})


@require_http_methods(['GET', 'POST'])
def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.prefetch_related('blocks', 'comments__author'),
        slug=slug,
        is_published=True,
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'Для добавления комментария необходимо авторизоваться.')
            return redirect(f"/login/?next={request.path}")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()

    comments = article.comments.filter(is_visible=True).select_related('author')
    return render(
        request,
        'archive_app/article_detail.html',
        {'article': article, 'comments': comments, 'comment_form': form},
    )


def about(request):
    page = AboutPage.objects.first()
    return render(request, 'archive_app/about.html', {'page': page})


def contacts(request):
    page = ContactsPage.objects.first()
    return render(request, 'archive_app/contacts.html', {'page': page})


@require_http_methods(['GET', 'POST'])
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше обращение отправлено.')
            return redirect('feedback')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = FeedbackForm(initial=initial)

    return render(request, 'archive_app/feedback.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация выполнена. Вы вошли в систему.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def sitemap_page(request):
    return render(request, 'archive_app/sitemap.html')


def custom_404(request, exception):
    return render(request, 'archive_app/404.html', status=404)
