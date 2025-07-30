

def officer_action_view(func):
    """
    Decorator for officer actions like approve, reject, etc
    """
    func.officer_action = True
    return func


def public_action_view(func):
    """
    Action view for public users
    """


def snitch_action(func):
    """
    Decorator to report all actions taken on a parcel, or report
    require func.parcel_number from the func/class
    """


def states(func):
    """
    Validates and updates states of an application
    Accepts:
    current_node - for validation of permission for action
    next_node - try to automate this. If given, update. If not, maintain the state, pass action
    """


