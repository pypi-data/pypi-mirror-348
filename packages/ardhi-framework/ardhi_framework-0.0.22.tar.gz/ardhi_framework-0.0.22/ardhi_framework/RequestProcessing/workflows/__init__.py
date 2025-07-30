from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import importlib
from django.db import transaction

logger = logging.getLogger(__name__)


class FlowView(APIView):

    def post(self, request, flow_type, instance_pk):

        if '_workflow' in flow_type:
            flow_type = flow_type.replace('_workflow', '')
        module_path = f'workflow_engine.{flow_type}_workflow'

        try:
            module = importlib.import_module(module_path)
            workflow_class = getattr(module, 'RunWorkflow')(request=request, instance_pk=instance_pk,
                                                            data=self.request.data)

        except (ModuleNotFoundError, AttributeError):
            return Response(f"Process Workflow for {flow_type} not defined.", status=404)

        with transaction.atomic():  # use atomic for rollback in case of fail
            sp = transaction.savepoint()
            success, info = workflow_class.run()
            if not success:
                transaction.savepoint_rollback(sp)
                return Response({'details': info}, status=400)

            return Response({'details': info}, status=200)

