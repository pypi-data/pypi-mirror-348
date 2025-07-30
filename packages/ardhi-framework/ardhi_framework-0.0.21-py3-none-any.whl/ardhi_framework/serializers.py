from rest_framework import serializers

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


class RemarksSerializer(serializers.ModelSerializer):
    """
    Serializes remarks for all applications in the system
    """

    # modify to allow create

    class Meta:
        model = 'remarks.Remarks'
        fields = [
            'remarks',
            'actor_details',
            'actor_role'
        ]

    remarks = serializers.CharField(max_length=1000)
    actor_details = UserDetailsField()
    actor_role = serializers.CharField(max_length=100)



