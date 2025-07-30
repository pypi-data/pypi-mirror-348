from rest_framework import permissions


class AuthenticatedUserPermission(permissions.BasePermission):
    """
    Represents a permission check for authenticated users.

    This class is designed to encapsulate the logic for determining whether
    a user is authenticated and has the required permissions for a specific
    operation. It integrates into a broader permission system and can be used
    to restrict or allow access to functionality based on authentication
    status.

    Attributes
    ----------
    is_authenticated : bool
        Indicates whether the user is authenticated.
    required_permission : str
        Represents the specific permission required for the action.

    Application
    -----------
    It overrides all 'Allow Any' permissions, and requires all users to be authenticated.

    """

    role_name = None

    def has_permission(self, request, view):
        return request.is_authenticated


class StaffPermission(AuthenticatedUserPermission):
    """
    Represents a staff member's permission system.

    The StaffPermission class manages the permissions associated with staff
    members. It provides a framework for defining and managing the access
    rights and restrictions that are applicable to staff users in a given
    context. This class is typically used in systems where role-based
    access control is enforced.
    """
    user_type = 'STAFF'


class PublicUserPermission(AuthenticatedUserPermission):
    """
    Represents public user permissions.

    This class is designed to handle the permissions associated with a public user
    within a system. It defines the permission levels that a user can have,
    allowing them access to different parts of the application based on their
    role and assigned rights.

    """
    user_type = 'PUBLIC'


class PublicProfessionalPermission(AuthenticatedUserPermission):
    # EG A public advocate, public licensed surveyor
    """
    Represents permissions and roles assigned to a public professional.

    This class defines the roles and responsibilities specific to
    public professionals such as public advocates or public licensed
    surveyors. It encapsulates permissions and functionalities
    relevant to these roles, enabling precise access control and
    regulation adherence.
    """
    user_type = 'PROFESSIONAL'


class DepartmentHeadPermission(StaffPermission):
    # for depeartment heads with superintendent powers
    """
    Represents permission levels for department heads, including
    superintendent powers.

    This class is designed to handle and define the set of permissions for
    department heads who are endowed with superintendent-level authority.
    It sets a structure for managing and distinguishing these permissions
    in a system where roles and responsibilities are distributed.

    Attributes:
        None
    """


class ReadOnlyPermission(AuthenticatedUserPermission):
    # to control view and action for read only
    """
    Controls view and action permissions to enable read-only access.

    This class is designed to handle and enforce read-only permissions for
    specific use cases. It ensures that users can only perform actions that
    do not alter the state or modify resources. Typically used in scenarios
    where viewing data is permitted, but editing is restricted. The purpose
    is to maintain data integrity while allowing necessary visibility.

    Attributes
    ----------
    None
    """



