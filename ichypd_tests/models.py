from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PersonalDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.PositiveIntegerField(null=True, blank=True)

    created = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = _('personal details')
        verbose_name_plural = _('personal details')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
