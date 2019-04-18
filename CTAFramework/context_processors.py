from django.conf import settings

def sitewide(request):
  return {
    'PLATFORM_VERSION': settings.PLATFORM_VERSION,
    'CONTENT_ONLY': request.GET.get('content_only', False)
  }