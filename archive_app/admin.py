from django.contrib import admin
from .models import AboutPage, Article, ArticleBlock, Comment, ContactsPage, Feedback


class ArticleBlockInline(admin.StackedInline):
    model = ArticleBlock
    extra = 1
    fields = ('order', 'block_type', 'text', 'image', 'image_alt', 'caption')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleBlockInline]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at', 'is_visible')
    list_filter = ('is_visible', 'created_at')
    search_fields = ('author__username', 'article__title', 'text')
    readonly_fields = ('article', 'author', 'text', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        return request.user.is_superuser and not AboutPage.objects.exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ContactsPage)
class ContactsPageAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'phone', 'email')

    def has_add_permission(self, request):
        return request.user.is_superuser and not ContactsPage.objects.exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.site_header = 'Администрирование городского архива Москвы'
admin.site.site_title = 'Архив Москвы'
admin.site.index_title = 'Управление содержимым сайта'
