import logging

from firebase_functions import https_fn
from firebase_admin import credentials, initialize_app

from shared.auth_middleware import authenticate
from shared.models import PropertyCreate, PropertyUpdate
from shared.property_repository import PropertyRepository

# Initialize Firebase Admin
# cred = credentials.ApplicationDefault()
# initialize_app(cred)

logger = logging.getLogger(__name__)


@https_fn.on_request()  # Use Firebase's decorator
def handle_property_crud(request: https_fn.Request) -> https_fn.Response:
    """Handle CRUD operations for properties."""
    try:
        # Authenticate request (adapt to Firebase Authentication if needed)
        auth_result = authenticate(request)
        if not auth_result.success:
            return auth_result.response

        user_id = auth_result.user_id
        method = request.method
        path = request.path

        repo = PropertyRepository()

        if method == 'POST' and path == '/properties':
            try:
                property_data = PropertyCreate(**request.get_json())
            except ValueError as e:
                return {'error': 'Invalid property data: ' + str(e)}, 400

            property_obj = repo.create_property(property_data, user_id)
            return {'data': property_obj.dict()}, 201

        elif method == 'GET' and path.startswith('/properties/'):
            property_id = path.split('/')[-1]  # Consider using a more robust path parsing method
            property_obj = repo.get_property(property_id)
            if not property_obj:
                return {'error': 'Property not found'}, 404
            return {'data': property_obj.dict()}, 200

        elif method == 'PUT' and path.startswith('/properties/'):
            property_id = path.split('/')[-1]
            try:
                property_data = PropertyUpdate(**request.get_json())
            except ValueError as e:
                return {'error': 'Invalid property data: ' + str(e)}, 400

            property_obj = repo.get_property(property_id)
            if not property_obj:
                return {'error': 'Property not found'}, 404
            if property_obj.owner_user_id != user_id:
                return {'error': 'Unauthorized'}, 403

            updated_property = repo.update_property(property_id, property_data)
            return {'data': updated_property.dict()}, 200

        elif method == 'DELETE' and path.startswith('/properties/'):
            property_id = path.split('/')[-1]
            property_obj = repo.get_property(property_id)
            if not property_obj:
                return {'error': 'Property not found'}, 404
            if property_obj.owner_user_id != user_id:
                return {'error': 'Unauthorized'}, 403

            success = repo.delete_property(property_id)
            return {'success': success}, 200 if success else 404

        return {'error': 'Invalid endpoint'}, 404

    except Exception as e:
        logger.exception(e)
        return {'error': str(e)}, 500