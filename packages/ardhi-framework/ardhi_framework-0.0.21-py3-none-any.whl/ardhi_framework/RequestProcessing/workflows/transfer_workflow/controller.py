from transfer.views import TransferWorkflowView
from rest_framework.response import Response
from django.utils.translation import gettext as _


class TransferAppUpdateView:

    def __init__(self, request, node_code) -> None:
        self.request = request
        self.node_code = node_code

    def run_main_call_function(self):
        main_class_view = TransferWorkflowView()
        main_class_view.request = self.request
        main_class_view.format_kwarg = []
        try:

            res = getattr(main_class_view, self.node_code.lower())(self.request)
        except Exception as e:

            return False, _(f'{self.node_code.lower()} Error: {e}')

        if isinstance(res, Response):
            if res.status_code >= 400:
                return False, res.data['details']
            else:
                return True, res.data
        else:
            return False, 'Not successful response'


