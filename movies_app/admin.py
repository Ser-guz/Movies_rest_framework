from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Movie, Actor, Genre, MovieShort, RatingStar, Rating, Review
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ['id', 'name', 'url']
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильмов"""
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShortInline(admin.TabularInline):
    """Кадры из фильма на странице фильма"""
    model = MovieShort
    extra = 0
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ['id', 'get_poster', 'title', 'category', 'url', 'draft']
    list_display_links = ('title',)
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [ReviewInline, MovieShortInline]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    actions = ['publish', 'unpublish']
    list_editable = ('draft',)
    readonly_fields = ('get_poster', )
    fieldsets = (
        (None, {
            "fields": (('title', 'tagline'),)
        }),
        (None, {
            "fields": (('description', 'get_poster'), )
        }),
        (None, {
            "fields": ('poster', )
        }),
        (None, {
            "fields": (('year', 'country'), 'world_premiere')
        }),
        ('Актеры', {
            "classes": ('collapse',),
            "fields": (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            "fields": (('budget', 'fees_in_country', 'fees_in_world'),)
        }),
        ('Дополнительно', {
            "fields": (('url', 'draft'),)
        }),
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="170"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            massege_bit = "1 запись была обновлена"
        else:
            massege_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{massege_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            massege_bit = "1 запись была обновлена"
        else:
            massege_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{massege_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_pemitions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_pemitions = ('change',)

    get_poster.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ['id', 'name', 'email', 'movie', 'parent']
    list_display_links = ('name',)
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ['id', 'name', 'age', 'get_image']
    list_display_links = ('name',)
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ['id', 'name', 'url']
    list_display_links = ('name',)


@admin.register(MovieShort)
class MovieShortAdmin(admin.ModelAdmin):
    """Кадры к фильму"""
    list_display = ['id', 'movie', 'title', 'get_image']
    list_display_links = ('movie',)
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Звезды рейтинга"""
    list_display = ['id', 'value']
    list_display_links = ('value',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ['id', 'movie', 'star', 'ip']
    list_display_links = ('movie',)


admin.site.site_title = 'Проект "rest"'
admin.site.site_header = 'Проект "rest"'
