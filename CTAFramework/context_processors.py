from django.conf import settings

def sitewide(request):
  return {
    'PLATFORM_VERSION': settings.PLATFORM_VERSION,
    'CONTENT_ONLY': request.GET.get('content_only', False)
  }

def botpress_endpoint(request):
  return {
    'BOTPRESS_ENDPOINT': settings.BOTPRESS_ENDPOINT
  }