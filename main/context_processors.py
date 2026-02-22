from django.conf import settings

def site_info(request):
    return {
        'site_name': 'Parasitoid',
        'site_name_suffix': 'Pod',
        'sidebar_apps': [
            {'name': 'Type Challenge', 'url': '/typechallenge', 'icon': '🔥'},
            {'name': 'Mystery Wheels', 'url': '#', 'icon': '🛞'},
            {'name': 'Pod Press', 'url': '/blog', 'icon': '📰'},
            {'name': 'Gallery', 'url': '/gallery', 'icon': '🐝'},
        ]
    }
