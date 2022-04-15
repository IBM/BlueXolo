from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = """check_media_dirs
        Usage:
        python manage.py (or ./manage.py) check_media_dirs

        Will create the required directories for media files
    """

    def handle(self, *args, **kwargs):
        required_dirs = [
            "test_keywords",
            "zip",
            "test_result",
            "test_cases",
            "test_suites",
            "keywords",
            "profiles"
        ] 

        try:        
            for dir in required_dirs:
                path = "{0}/{1}".format(settings.MEDIA_ROOT, dir)
                if not os.path.isdir(path):
                    print(path)
                    os.mkdir(path)
        except:
            raise Exception("Error during media directories creation")
        else:
            print("Required media directories are created")