import datetime

from django.db import models
from django.db.models.signals import post_save

from ardhi_framework.exceptions import FraudDetectionError
from ardhi_framework.fields import UserDetailsField, FreezeStateField, ArdhiPrimaryKeyField


class ArdhiModelManager(models.Manager):
    pass


class ArdhiBaseModel(models.Model):
    id = ArdhiPrimaryKeyField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = UserDetailsField()
    last_modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    deleted_by = UserDetailsField()

    class Meta:
        abstract = True

    objects = ArdhiModelManager()

    def delete(self, using=None, keep_parents=False):
        # no deletion allowed
        raise FraudDetectionError("Action flagged as fraudulent.")

    def update(self, *args, **kwargs):
        # Update and log all information. Freeze in state data
        if kwargs.get('is_deleted'):
            kwargs['deleted_by'] = self.get_current_actor()
            kwargs['date_deleted'] = datetime.datetime.now()

        return super().update(*args, **kwargs)

    def create(self, *args, **kwargs):
        kwargs['created_by'] = self.get_current_actor()

        return super().create(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # log information
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_current_actor(self):
        return self.created_by


class ArdhiModel(ArdhiBaseModel):
    """
    This model prevents deletion of objects
    Logs all entries, updates, creation, etc
    Every model must have date updated, date created, and last modified
    """
    # readonly field for serializers
    fz = FreezeStateField()


@post_save(sender=ArdhiBaseModel, dispatch_uid="ArdhiBaseModel_post_save")
def update_frozen_state_instance(sender, instance, created, **kwargs):
    if not created:
        instance.last_modified = datetime.datetime.now()
        instance.save(
            update_fields=['last_modified']
        )



