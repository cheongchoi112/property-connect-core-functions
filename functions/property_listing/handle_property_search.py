from firebase_functions import https_fn, options
from shared.properties_facade_service import PropertiesFacadeService

@https_fn.on_request(cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "delete", "put"],
    )
) 
def handle_property_search(request):
    """Handle property search operations."""
    properties_facade = PropertiesFacadeService()
    return properties_facade.search_properties(request)