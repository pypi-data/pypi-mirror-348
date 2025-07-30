from transfer.generic_funcs.RequestProcessing.workflows.flows import WorkflowNode, BaseNode
from transfer.generic_funcs.RequestProcessing.workflows.transfer_workflow.controller import TransferAppUpdateView


class ValidNode(WorkflowNode, TransferAppUpdateView):
    node_code = 'INITIALIZE_APPLICATION'
    next_node = BaseNode(node_code='VERIFICATION_PAYMENT')
    previous_node = BaseNode(node_code=None)
    success_execution_mesage = "Application request successfully created."

    def __init__(self, request, instance=None, data=..., **kwargs) -> None:
        TransferAppUpdateView.__init__(self, request, self.node_code)
        WorkflowNode.__init__(self, instance, data, **kwargs)
        assert instance.node_code == self.node_code
        self.instance = instance
        self.data = data

    def run_forward(self):
        if True:
            self.move_to_next_node()
        return True, 'Successfully run'

    def run_notify_applicant(self):
        self.notify_user(None, 'Oh, workflow is working just fine')
        return True, 'Notifications sent successfully.'

    def run_notify_other_users(self):
        """Please set this under threaded actions"""
        return True, 'Notifications sent successfully.'




