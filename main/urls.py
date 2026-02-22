from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('typechallenge/', views.typechallenge, name='typechallenge'),
    path('wheels/', views.wheels, name='wheels'),
    path('appendices/', views.appendices, name='appendices'),
    path('replaytool/', views.replaytool, name='replaytool'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:photo_id>/', views.gallery_photo, name='gallery_photo'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
