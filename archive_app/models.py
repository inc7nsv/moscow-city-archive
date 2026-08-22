from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Адрес статьи', max_length=220, unique=True)
    summary = models.TextField('Краткое описание', max_length=500)
    cover = models.ImageField('Изображение карточки', upload_to='articles/covers/')
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


class ArticleBlock(models.Model):
    BLOCK_TYPES = (
        ('text', 'Текст'),
        ('image', 'Изображение'),
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name='Статья',
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    block_type = models.CharField('Тип блока', max_length=10, choices=BLOCK_TYPES)
    text = models.TextField('Текст', blank=True)
    image = models.ImageField('Изображение', upload_to='articles/content/', blank=True, null=True)
    image_alt = models.CharField('Описание изображения', max_length=255, blank=True)
    caption = models.CharField('Подпись', max_length=255, blank=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Блок статьи'
        verbose_name_plural = 'Блоки статьи'

    def __str__(self):
        return f'{self.article.title}: {self.get_block_type_display()} #{self.order}'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archive_comments', verbose_name='Автор')
    text = models.TextField('Комментарий', max_length=2000)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_visible = models.BooleanField('Показывать', default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author.username}: {self.text[:40]}'


class AboutPage(models.Model):
    title = models.CharField('Заголовок', max_length=200, default='Об организации')
    text = models.TextField('Текст')
    image = models.ImageField('Изображение', upload_to='pages/about/', blank=True, null=True)
    image_alt = models.CharField('Описание изображения', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Страница «Об организации»'
        verbose_name_plural = 'Страница «Об организации»'

    def __str__(self):
        return self.title


class ContactsPage(models.Model):
    organization_name = models.CharField('Название организации', max_length=255, default='Государственный архив города Москвы')
    address = models.CharField('Адрес', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=100, blank=True)
    email = models.EmailField('Электронная почта', blank=True)
    working_hours = models.CharField('Режим работы', max_length=255, blank=True)
    additional_info = models.TextField('Дополнительная информация', blank=True)

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return self.organization_name


class Feedback(models.Model):
    name = models.CharField('Имя', max_length=150)
    email = models.EmailField('Электронная почта')
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение', max_length=5000)
    created_at = models.DateTimeField('Дата обращения', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return f'{self.name}: {self.subject}'
