from firebase_functions import https_fn, options

from application.properties_facade_service import PropertiesFacadeService

@https_fn.on_request(cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "delete", "put"],
    )
)
def handle_property_search(request):
    """
    Presentation Layer: Handles property search operations.

    Relationships:
    - Uses properties_facade_service from the application layer for property search operations.
    - Indirectly depends on search_strategies through properties_facade_service in the application layer for different search algorithms.
    - Indirectly depends on property_repository through properties_facade_service in the infrastructure layer for data access.
    """
    properties_facade = PropertiesFacadeService()
    return properties_facade.search_properties(request)