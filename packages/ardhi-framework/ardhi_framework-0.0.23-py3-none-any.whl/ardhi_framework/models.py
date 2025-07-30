import datetime

from django.db import models
from django.db.models.signals import post_save

from ardhi_framework.exceptions import FraudDetectionError
from ardhi_framework.fields import UserDetailsField, FreezeStateField, ArdhiPrimaryKeyField, ParcelNumberField


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
        raise FraudDetectionError("Action flagged as fraudulent. Deletion not allowed.")

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

    class Meta:
        abstract = True


@post_save(sender=ArdhiBaseModel)
def update_frozen_state_instance(sender, instance, created, **kwargs):
    if not created:
        instance.last_modified = datetime.datetime.now()
        instance.save(
            update_fields=['last_modified']
        )


class DepartmentParcelRegistryModel(ArdhiModel):
    parcel_number = ParcelNumberField(unique=True)


class EventChangeLogModel(ArdhiModel):
    event_type = models.CharField(max_length=255)
    description = models.TextField()
    data_in = FreezeStateField()
    parcel_number = models.ForeignKey(DepartmentParcelRegistryModel, on_delete=models.SET_NULL, null=True, blank=True,)
    application_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Change Log Activity'
        verbose_name_plural = 'Change Logs Activity'

    def fetch_parcel_number(self):
        return self.parcel_number


class ParcelRelatedDocumentsModel(ArdhiModel):
    """
    This model is used to store generated documents, including uploads, titles, etc
    """
    parcel_number = models.ForeignKey(DepartmentParcelRegistryModel, on_delete=models.SET_NULL, null=True, blank=True,)
    document_id = models.CharField(max_length=255, null=True, blank=True)
    doc_data = FreezeStateField(null=True, blank=True)  # stores doc data especially for on the fly documents



