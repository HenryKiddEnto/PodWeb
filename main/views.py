from django.shortcuts import render, get_object_or_404
from .models import Project, BlogPost, HomepageVideo, GalleryPhoto

def home(request):
    try:
        video = HomepageVideo.objects.filter(is_active=True).latest('updated_at')
    except HomepageVideo.DoesNotExist:
        video = None

    return render(request, 'main/home.html', {'video': video})

def typechallenge(request):
    return render(request, 'main/typechallenge.html')

# Podpress views
def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'main/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'main/blog_detail.html', {'post': post})

def gallery(request):
    return render(request, 'main/gallery.html')

def wheels(request):
    return render(request, 'main/wheels.html')

def replaytool(request):
    return render(request, 'main/replaytool.html')

def appendices(request):
    return render(request, 'main/appendices.html')

# Gallery view
def gallery(request):
    photos = GalleryPhoto.objects.all()
    return render(request, 'main/gallery.html', {'photos': photos})

# Optional: Detail view for individual photos
def gallery_photo(request, photo_id):
    photo = get_object_or_404(GalleryPhoto, id=photo_id)
    return render(request, 'main/gallery_photo.html', {'photo': photo})
