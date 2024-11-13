import logging

from firebase_functions import https_fn, options

from application.properties_facade_service import PropertiesFacadeService
from infrastructure.auth_middleware import authenticate
from infrastructure.property_repository import PropertyRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "delete", "put"],
    )
)
def handle_property_crud(request: https_fn.Request) -> https_fn.Response:
    """
    Presentation Layer: Handles CRUD operations for properties.

    Relationships:
    - Uses properties_facade_service from the application layer for property CRUD operations.
    - Indirectly depends on property_repository through properties_facade_service in the infrastructure layer for data access.
    - Potentially uses auth_middleware through properties_facade_service in the infrastructure layer for authentication.
    """
    method = request.method
    path = request.path

    try:
        # Authenticate request (adapt to Firebase Authentication if needed)
        auth_result = authenticate(request)

        if not auth_result.success:
            return auth_result.response

        user_id = auth_result.user_id
        user_email = auth_result.user_email

        repo = PropertyRepository()
        properties_facade = PropertiesFacadeService()

        if method == 'POST' and path == '/properties':
            return properties_facade.create_properties(repo, request, user_email, user_id)

        elif method == 'GET' and path.startswith('/properties/'):
            return properties_facade.get_properties(repo, path)

        elif method == 'GET' and path.startswith('/user/properties'):
            return properties_facade.get_user_properties(repo, user_id)

        elif method == 'PUT' and path.startswith('/properties/'):
            return properties_facade.update_property(repo, path, request, user_id)

        elif method == 'DELETE' and path.startswith('/properties/'):
            return properties_facade.delete_property(repo, path, user_id)

        return {'error': 'Invalid endpoint'}, 404

    except Exception as e:
        logger.error(f"Error handling request: {e}")
        return {'error': 'Internal server error'}, 500