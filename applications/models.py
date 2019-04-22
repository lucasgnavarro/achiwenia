import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from useraccounts.models import UserRole, UserProfile


# Create your models here.
class Application(models.Model):
    title = models.CharField(blank=None, max_length=60)
    description = models.CharField(blank=None, max_length=255)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='app-id')
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '({id}) {title} [{app_id}]'.format(id=self.id, title=self.title, app_id=self.uid)

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')


class ApplicationConfig(models.Model):
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, null=False, blank=False,
        related_name='config', related_query_name='config'
    )
    login_bg_img = models.ImageField(null=True, blank=True, verbose_name=_('Login screen Image'),
                                     upload_to='login_bg_img/')

    def __str__(self):
        return '({id}) - {login_img}'.format(id=self.id, login_img=self.login_bg_img)

    class Meta:
        verbose_name = 'Application Configuration'


class ApplicationUrl(models.Model):
    url = models.URLField(blank=None, max_length=255, unique=True)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, null=False, blank=False, related_name='url'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{url} ({application})'.format(url=self.url, application=self.application.title)


class ApplicationByUser(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, null=False, blank=False, related_name='app_by_user'
    )
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='app_by_user'
    )
    is_staff = models.BooleanField(default=False)
    user_role = models.ForeignKey(UserRole, null=False, blank=False, default='CST', on_delete=models.PROTECT)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{username} [{status}]'.format(
            username=self.user.username,
            status='Enabled' if self.enabled else 'Disabled'
        )

    class Meta:
        verbose_name = _('Users by App')
        verbose_name_plural = _('Users by App')
        unique_together = ('application', 'user_role')
