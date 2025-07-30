from rest_framework.decorators import action

from ardhi_framework.permissions.base_permissions import AuthenticatedUserPermission, StaffPermission, \
    PublicUserPermission


def custom_view_action(
    methods=None,
    detail=False,
    url_path=None,
    url_name=None,
    permission_classes=None,
    **kwargs
):
    """
    A decorator similar to @action, preconfigured for officer actions.
    Sets `func.officer_action = True` and applies DRF's @action decorator,
    while allowing override of permission_classes and other action arguments.
    """

    permission_classes = permission_classes or [AuthenticatedUserPermission, ]

    def decorator(func):
        # Apply DRF's action decorator with the injected/overridable parameters
        decorated = action(
            methods=methods or ['get', 'post', 'put'],
            detail=detail,
            url_path=url_path,
            url_name=url_name,
            permission_classes=permission_classes,
            **kwargs
        )(func)
        return decorated

    return decorator


def return_decorator(permission_classes):
    return custom_view_action(permission_classes=permission_classes)


def officer_action_view(func):
    """
    Decorator for officer actions like approve, reject, etc
    """
    permission_classes = [StaffPermission, ]
    return return_decorator(permission_classes)


def public_action_view(func):
    """
    Action view for public users
    """
    permission_classes = [PublicUserPermission, ]
    return return_decorator(permission_classes)


def snitch_action(func):
    """
    Decorator to report all actions taken on a parcel, or report
    requires func.parcel_number from the func/class
    """
    parcel_number = func.parcel_number


def states(func):
    """
    Validates and updates states of an application
    Accepts:
    current_node - for validation of permission for action
    next_node - try to automate this. If given, update. If not, maintain the state, pass action
    """


