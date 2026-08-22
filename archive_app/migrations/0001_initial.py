# Generated manually for the ready-to-run student project.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Об организации', max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pages/about/', verbose_name='Изображение')),
                ('image_alt', models.CharField(blank=True, max_length=255, verbose_name='Описание изображения')),
            ],
            options={'verbose_name': 'Страница «Об организации»', 'verbose_name_plural': 'Страница «Об организации»'},
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=220, unique=True, verbose_name='Адрес статьи')),
                ('summary', models.TextField(max_length=500, verbose_name='Краткое описание')),
                ('cover', models.ImageField(upload_to='articles/covers/', verbose_name='Изображение карточки')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи', 'ordering': ['-published_at']},
        ),
        migrations.CreateModel(
            name='ContactsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(default='Государственный архив города Москвы', max_length=255, verbose_name='Название организации')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, max_length=100, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта')),
                ('working_hours', models.CharField(blank=True, max_length=255, verbose_name='Режим работы')),
                ('additional_info', models.TextField(blank=True, verbose_name='Дополнительная информация')),
            ],
            options={'verbose_name': 'Контактная информация', 'verbose_name_plural': 'Контактная информация'},
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('subject', models.CharField(max_length=200, verbose_name='Тема')),
                ('message', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Обработано')),
            ],
            options={'verbose_name': 'Обращение', 'verbose_name_plural': 'Обращения', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ArticleBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('block_type', models.CharField(choices=[('text', 'Текст'), ('image', 'Изображение')], max_length=10, verbose_name='Тип блока')),
                ('text', models.TextField(blank=True, verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles/content/', verbose_name='Изображение')),
                ('image_alt', models.CharField(blank=True, max_length=255, verbose_name='Описание изображения')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Подпись')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='archive_app.article', verbose_name='Статья')),
            ],
            options={'verbose_name': 'Блок статьи', 'verbose_name_plural': 'Блоки статьи', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Показывать')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='archive_app.article', verbose_name='Статья')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archive_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии', 'ordering': ['created_at']},
        ),
    ]
