from django.conf import settings
from django.core.cache import cache

from blog.models import Blog


def get_content_from_cache():
    if settings.CACHE_ENABLED:
        key = 'content_list'
        content_list = cache.get(key)
        if content_list is None:
            content_list = Blog.objects.all()
            cache.set(key, content_list)
    else:
        content_list = Blog.objects.all()

    return content_list
