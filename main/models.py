from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True)
    
    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short preview of the post")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']  # Newest first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate excerpt from content if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + '...'
        super().save(*args, **kwargs)

class HomepageVideo(models.Model):
    title = models.CharField(max_length=200, default="Featured Video")
    video = EmbedVideoField(help_text="Enter YouTube, Vimeo, or SoundCloud URL")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    autoplay = models.BooleanField(default=False)
    mute = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Homepage Video"
        verbose_name_plural = "Homepage Videos"

class GalleryPhoto(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    date_taken = models.DateField(default=timezone.now)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['display_order', '-date_taken']
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return self.title
