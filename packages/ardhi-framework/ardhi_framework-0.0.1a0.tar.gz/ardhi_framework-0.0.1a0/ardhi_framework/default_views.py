"""
For consolidated functions, this will provide basic views for common actions
Now: the command to start a service or an application will generate base views, but generally.
However, each application will be required to define its own parameters for views
"""

from .generics import ArdhiModelViewSet
from .models import ArdhiBaseModel
from .serializers import RemarksSerializer


class RemarksModelViewSet(ArdhiModelViewSet):
    model: ArdhiBaseModel = 'remarks.Remarks'
    serializer_class = RemarksSerializer
    queryset = model.objects.all()







