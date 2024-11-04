import firebase_functions as functions
from firebase_admin import credentials
from shared.auth_middleware import authenticate
from shared.models import SearchCriteria
from shared.search_strategies import SearchStrategyEngine
from firebase_functions import https_fn, options

# Initialize Firebase Admin
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred)

@https_fn.on_request(cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "delete", "put"],
    )
) 
def handle_property_search(request):
    """Handle property search operations."""
    try:
        if request.method != 'POST':
            return {'error': 'Method not allowed'}, 405
        search_data = request.get_json()
        criteria = SearchCriteria(**search_data)
        
        search_strategy = SearchStrategyEngine()
        results = search_strategy.search(criteria)
        
        return {
            'data': [property.dict() for property in results],
            'count': len(results)
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500