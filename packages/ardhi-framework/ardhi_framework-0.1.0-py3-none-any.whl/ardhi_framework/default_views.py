"""
For consolidated functions, this will provide basic views for common actions
Now: the command to start a service or an application will generate base views, but generally.
However, each application will be required to define its own parameters for views
"""

from ardhi_framework.generics import ArdhiModelViewSet
from ardhi_framework.models import ArdhiBaseModel
from ardhi_framework.serializers import RemarksSerializer


class RemarksModelViewSet(ArdhiModelViewSet):
    model: ArdhiBaseModel = 'remarks.Remarks'
    serializer_class = RemarksSerializer
    queryset = model.objects.all()







