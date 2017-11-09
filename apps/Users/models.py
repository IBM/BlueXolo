from celery.result import AsyncResult
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.Products.models import Source
from .managers import UserManager


class Task(models.Model):
    CATEGORIES = (
        (1, "Extract"),
        (2, "Run Script"),
    )
    name = models.CharField(_('name'), max_length=200)
    task_id = models.CharField(_('task id'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    category = models.IntegerField(choices=CATEGORIES, default=2)
    task_info = models.TextField(blank=True)
    task_result = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """The AbstractBaseUser is used because we need authentication with email.
        https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-a-custom-user-model
    """
    email = models.CharField(_('email address'), unique=True, max_length=30)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is staff'))
    products = models.ManyToManyField(Source, blank=True)
    tasks = models.ManyToManyField(Task, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def get_full_name(self):
        """Return first name and last name in a single string"""
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        """Return only the first name"""
        return "{0}".format(self.first_name)

    def send_email_user(self, subject, message, from_email=None, **kwargs):
        """Send a email for this user"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_all_tasks(self):
        """Return last 6 tasks fo this user"""
        user_tasks = []
        for task in self.tasks.all().order_by('-created_at')[:6]:
            res = AsyncResult(task.task_id)
            if res.ready() and res.state != task.state:
                task.state = res.state
                task.task_info = res.result or ''
                task.save()
            user_tasks.append(task)
        return user_tasks
