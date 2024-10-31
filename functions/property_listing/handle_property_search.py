import firebase_admin
import firebase_functions as functions
from firebase_admin import credentials
from shared.auth_middleware import authenticate
from shared.models import SearchCriteria
from shared.search_strategies import CompositeSearchStrategy
from firebase_functions import https_fn

# Initialize Firebase Admin
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred)

@https_fn.on_request()  # Use Firebase's decorator
def handle_property_search(request):
    """Handle property search operations."""
    try:
        # Authenticate request
        auth_result = authenticate(request)
        if not auth_result.success:
            return auth_result.response
        
        if request.method != 'POST':
            return {'error': 'Method not allowed'}, 405
            
        search_data = request.get_json()
        criteria = SearchCriteria(**search_data)
        
        # Use composite search strategy to handle multiple search criteria
        search_strategy = CompositeSearchStrategy()
        results = search_strategy.search(criteria)
        
        return {
            'data': [property.dict() for property in results],
            'count': len(results)
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500