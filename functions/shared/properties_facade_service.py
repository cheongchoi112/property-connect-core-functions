# properties_facade_service.py
from .search_strategies import SearchStrategyEngine
from .property_repository import PropertyRepository
from .models import PropertyCreate, PropertyUpdate, Property, SearchCriteria
from typing import List, Optional

class PropertiesFacadeService:
    def create_properties(self, repo, request, user_email, user_id):
        try:
            print('---------request.get_json()----------', request.get_json())
            data = request.get_json()
            if isinstance(data, list):
                properties_data = [PropertyCreate(**item) for item in data]
                properties = repo.create_properties(properties_data, user_id, user_email)
                return {'data': [prop.dict() for prop in properties]}, 201
            else:
                property_data = PropertyCreate(**data)
                property_obj = repo.create_property(property_data, user_id, user_email)
                return {'data': property_obj.dict()}, 201
        except ValueError as e:
            return {'error': 'Invalid property data: ' + str(e)}, 400

    def get_properties(self, repo: PropertyRepository, path):
        property_id = path.split('/')[-1]  # Consider using a more robust path parsing method
        property_obj = repo.get_property(property_id)
        if not property_obj:
            return {'error': 'Property not found'}, 404
        return {'data': property_obj.dict()}, 200

    def get_user_properties(self, repo : PropertyRepository, user_id):
        properties = repo.get_properties_by_user(user_id)
        return {'data': [property_obj.dict() for property_obj in properties]}, 200
    
    def update_property(path, repo, request, user_id):
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
    
    def delete_property(self, repo, path, user_id):
        property_id = path.split('/')[-1]
        property_obj = repo.get_property(property_id)
        if not property_obj:
            return {'error': 'Property not found'}, 404
        if property_obj.owner_user_id != user_id:
            return {'error': 'Unauthorized'}, 403
        success = repo.delete_property(property_id)
        return {'success': success}, 200 if success else 404
    
    def search_properties(self, request):
        try:
            if request.method != 'POST':
                return {'error': 'Method not allowed'}, 405

            search_data = request.get_json()
            print('search_data', search_data)
            criteria = SearchCriteria(**search_data)

            search_strategy = SearchStrategyEngine()
            results = search_strategy.search(criteria)

            return {
                'data': [property.dict() for property in results],
                'count': len(results)
            }, 200

        except Exception as e:
            return {'error': str(e)}, 500