from rest_framework import serializers

from ardhi_framework.models import EventChangeLogModel
from ardhi_framework.utils import mask_private_data


class UserDetailsField(serializers.DictField):
    """
    User details are dynamic. This field masks all private data if the user is not staff or the user is not the actor

    """

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):

        if isinstance(data, dict):
            # masking if not staff and not authorized or current user
            if self.context['is_staff'] or self.context['user'] == data['user_id']:
                for k, v in data.items():
                    if k in ['phone_number', 'email', 'krapin', 'registration_number', 'id_num', 'idnum', 'phone_num']:
                        # masks all private data
                        data[k] = mask_private_data(v)
        return data


class RemarksSerializer(serializers.Serializer):
    """
    Serializes remarks for all applications in the system
    """
    remarks = serializers.CharField(max_length=1000)
    actor_details = UserDetailsField()
    actor_role = serializers.CharField(max_length=100)


class EventChangeLogModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the EventChangeLog model.

    This serializer is designed to convert EventChangeLog model instances into
    representations that can be rendered into JSON or other content types. It allows
    for the deserialization of input data to validate and convert it back into
    model instance data. Serializers play a crucial role in Django REST Framework
    to handle transport and storage of data efficiently.

    Attributes
    ----------
    Meta : class
        Inner Meta class where the model to be serialized and fields to be included
        or excluded are defined for use with EventChangeLog.
    """
    class Meta:
        model = EventChangeLogModel
        fields = '__all__'

