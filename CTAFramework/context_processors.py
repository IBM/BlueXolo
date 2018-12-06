from django.conf import settings

def sitewide(request):
  return {
    'PLATFORM_VERSION': settings.PLATFORM_VERSION
  }