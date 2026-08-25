from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, BlogPost, HomepageVideo, GalleryPhoto

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from .models import MatchupUpload, GlobalDataset
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

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

def wheel(request):
    return render(request, 'main/wheel.html')

def builder(request):
    return render(request, 'main/builder.html')

MAX_UPLOAD_KEYS = 2000  # sanity limit — not expecting abuse, but cheap to guard against

@require_POST
@csrf_protect
def upload_matchup_data(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    entries = body.get('entries')
    if not isinstance(entries, dict):
        return JsonResponse({'error': "'entries' must be an object"}, status=400)

    if len(entries) == 0:
        return JsonResponse({'error': 'No entries provided'}, status=400)

    if len(entries) > MAX_UPLOAD_KEYS:
        return JsonResponse({'error': 'Too many entries in one upload'}, status=400)

    submitter_name = str(body.get('submitter_name', ''))[:80]

    upload = MatchupUpload.objects.create(
        submitter_name=submitter_name,
        payload=entries,
    )

    return JsonResponse({'status': 'received', 'upload_id': upload.id})


@require_GET
def get_global_data(request):
    dataset = GlobalDataset.objects.first()
    data = dataset.data if dataset else {}
    return JsonResponse(data)

@staff_member_required
def review_uploads(request):
    pending = MatchupUpload.objects.filter(status='pending')
    return render(request, 'main/review_uploads.html', {'uploads': pending})


@staff_member_required
def review_upload_detail(request, upload_id):
    upload = get_object_or_404(MatchupUpload, id=upload_id, status='pending')
    dataset, _ = GlobalDataset.objects.get_or_create(id=1)  # ensure the singleton row exists
    global_data = dataset.data

    if request.method == 'POST':
        accepted_keys = request.POST.getlist('accept_key')

        for key in accepted_keys:
            if key in upload.payload:
                dataset.data[key] = upload.payload[key]

        dataset.save()

        upload.status = 'approved' if accepted_keys else 'rejected'
        upload.reviewed_at = timezone.now()
        upload.review_note = request.POST.get('review_note', '')
        upload.save()

        return redirect('review_uploads')

    # GET — build the per-key diff for display
    diff_rows = []
    for key, incoming_value in upload.payload.items():
        diff_rows.append({
            'key': key,
            'current': global_data.get(key),
            'incoming': incoming_value,
            'is_new': key not in global_data,
        })

    return render(request, 'main/review_upload_detail.html', {
        'upload': upload,
        'diff_rows': diff_rows,
    })

