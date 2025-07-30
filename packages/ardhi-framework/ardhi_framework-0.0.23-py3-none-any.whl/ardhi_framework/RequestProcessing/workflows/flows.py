from django.db.models import Model
from django.utils.translation import gettext_lazy as _
import importlib

from ardhi_framework.property_processing.transactibility_validator import TransactableParcel


class BaseNode(object):
    node_code = None

    def __init__(self, node_code=None) -> None:
        if node_code is not None:
            self.node_code = node_code

    def is_autoprocessed(self):
        """Override to process this node automatically, when called as the next node,
        Then move to the next node; and so on"""
        return False

class Node(BaseNode):
    previous_node: BaseNode = None
    next_node: BaseNode = None

    def __init__(self, node_code=None, **kwargs) -> None:
        super().__init__(node_code=node_code)

        self.tasks_methods = []
        self.number_of_tasks = 0

    def has_permissions(self):
        # Check if user has permissions for this node
        return True, 'Proceed'  # Placeholder for actual permission check

    def get_tasks(self):
        self.tasks_methods = [
            method for method in dir(self) if method.startswith('run_') and callable(getattr(self, method))
        ]
        return True, 'Success'

    def handle_task(self, task):
        # Run a single task
        method_name = f'{task}'
        if hasattr(self, method_name):
            success, info = getattr(self, method_name)()
            if not success:
                return False, info
            else:
                return True, info
        else:
            return False, _(f'Invalid task defined: {task}')

    def execute_tasks(self):
        self.get_tasks()
        for task in self.tasks_methods:
            success, resp = self.handle_task(task)
            if not success:
                return False, resp
        return True, 'Successfully executed tasks'


class WorkflowNode(Node):
    """Defines node actions"""

    def __init__(self, instance, data, node_code=None, validate_parcel=False, **kwargs) -> None:
        super().__init__(node_code or instance.node_code, **kwargs)
        self.data = data
        self.instance = instance
        self.validate_parcel_can_transact = validate_parcel
        self.kwargs = kwargs

    def move_to_next_node(self):
        if self.next_node.node_code:
            self.instance.node_code = self.next_node.node_code
            self.instance.save()

            if self.next_node.is_autoprocessed:
                """Recall workflow for new code"""
                self.move_to_next_node()

            return True, f'Forwarded to {self.next_node.node_code}'
        # raise NotImplementedError('Forward method must be implemented.')
        return False, f'Could not forward instance'

    def move_to_previous_node(self):
        if self.previous_node.node_code:
            self.instance.node_code = self.previous_node.node_code
            self.instance.save()
            return True, 'Returned to {}'.format(self.previous_node.node_code)
        return False, 'Could not return instance'

    def skip_to_node(self, node: BaseNode):
        if node and node.node_code:
            self.instance.node_code = node.node_code
            self.instance.save()
            return True, f'Moved to {node.node_code}'

        return False, f'Failed to move instance to {node.node_code}'

    def run_has_permissions(self):
        return self.has_permissions()

    def run_validate_parcel(self, parcel_number=None):
        if self.validate_parcel_can_transact:
            if not parcel_number:
                if not hasattr(self.instance, 'parcel_number'):
                    return False, 'Specify parcel number'
                parcel_number = self.instance.parcel_number
            return TransactableParcel(
                parcel_number=parcel_number,
                context=self.kwargs['context']
            ).parcel_is_transactable(validate=True)
        return True, 'Successful'

    def notify_user(self, receiver, message):

        return True, 'Notification sent successfully.'


class WorkflowInstance(object):
    instance_model: Model = None

    def __init__(self, request, workflow_name, instance_pk, data={}, instance_model=None):
        self.request = request
        self.instance_pk = instance_pk
        self.instance = None
        self.data = data
        self.workflow_name = workflow_name
        if instance_model:
            self.instance_model = instance_model

    def get_current_node(self, node_code=None):
        if node_code is None:
            node_code = self.instance.node_code.lower()
        # get file path with
        node_path = f'workflow_engine.{self.workflow_name}.node_{node_code}'
        try:
            file_ = importlib.import_module(node_path)
            node_class = getattr(file_, 'ValidNode')(request=self.request, instance=self.instance, data=self.data)

        except ModuleNotFoundError:
            return False, _(f"{node_path} not defined.")
        except AttributeError as e:
            return False, f'Unable to get {node_path}'

        return True, node_class

    def _has_node_code(self):
        if not hasattr(self.instance, 'node'):
            return False, _('Model instance must have a node to use workflows')
        if getattr(self.instance, 'node', None) is None:
            return False, _('Node must be set for the instance')
        return True, 'Has node'

    def get_instance(self):
        try:
            self.instance = self.instance_model.objects.get(pk=self.instance_pk)
        except self.instance_model.DoesNotExist:
            return False, _(f'Invalid instance pk: {self.instance_pk}')
        except Exception as e:
            return False, _(f'Unable to get instance, {e}')
        success, res = self._has_node_code()
        if not success:
            return False, res
        return True, 'Success'

    def execute(self):
        if self.instance_pk != 'initialize':
            success, res = self.get_instance()
            if not success:
                return False, res
            success, node_or_info = self.get_current_node()
            if not success:
                return False, node_or_info
        else:
            success, node_or_info = self.get_current_node('initialize')
            if not success:
                return False, node_or_info
        success, info = node_or_info.execute_tasks()
        if not success:
            return False, info
            # pass custom success info
        if node_or_info.success_execution_mesage:
            info = node_or_info.success_execution_mesage
        return True, info


