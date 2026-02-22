from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import HomepageVideo, Project, BlogPost, GalleryPhoto  # Import all your models

# Use AdminVideoMixin in a single registration
class HomepageVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('updated_at',)

# Register with the class directly
admin.site.register(HomepageVideo, HomepageVideoAdmin)

# Your other models can stay the same
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', 'technologies')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'is_published')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Dates', {
            'fields': ('published_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'is_featured', 'display_order')
    list_filter = ('is_featured', 'date_taken')
    search_fields = ('title', 'caption')
    list_editable = ('display_order', 'is_featured')

    fieldsets = (
        ('Photo Information', {
            'fields': ('title', 'caption', 'image')
        }),
        ('Metadata', {
            'fields': ('date_taken', 'is_featured', 'display_order')
        }),
    )

    # Preview thumbnail in list view
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 38px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'
