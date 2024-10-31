from abc import ABC, abstractmethod
from typing import List
from .models import Property, SearchCriteria
from .property_repository import PropertyRepository
import math

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[Property]:
        pass

class KeywordSearchStrategy(SearchStrategy):
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.keyword:
            # Search in title and description
            query = query.where('title', '>=', criteria.keyword)\
                        .where('title', '<=', criteria.keyword + '\uf8ff')\
                        .order_by('title')
        
        return repo.search_properties(query)

class LocationSearchStrategy(SearchStrategy):
    def search(self, criteria: SearchCriteria) -> List[Property]:
        if not criteria.location:
            return []
            
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        # Get properties and filter by distance
        properties = repo.search_properties(query)
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in kilometers
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
                math.cos(lat1_rad) * math.cos(lat2_rad) * \
                math.sin(delta_lon/2) * math.sin(delta_lon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            return R * c

        return [
            prop for prop in properties
            if calculate_distance(
                criteria.location.latitude,
                criteria.location.longitude,
                float(prop.address.split(',')[0]),  # Assuming address stores "lat,lng"
                float(prop.address.split(',')[1])
            ) <= criteria.location.radius
        ]

class PriceRangeSearchStrategy(SearchStrategy):
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.price_range:
            query = query.where('price', '>=', criteria.price_range.min_price)\
                        .where('price', '<=', criteria.price_range.max_price)
        
        return repo.search_properties(query)

class CompositeSearchStrategy(SearchStrategy):
    def search(self, criteria: SearchCriteria) -> List[Property]:
        # Apply strategies based on provided criteria
        results = set()
        applied_strategies = False
        
        if criteria.keyword:
            keyword_results = set(KeywordSearchStrategy().search(criteria))
            results = keyword_results if not applied_strategies else results.intersection(keyword_results)
            applied_strategies = True
            
        if criteria.location:
            location_results = set(LocationSearchStrategy().search(criteria))
            results = location_results if not applied_strategies else results.intersection(location_results)
            applied_strategies = True
            
        if criteria.price_range:
            price_results = set(PriceRangeSearchStrategy().search(criteria))
            results = price_results if not applied_strategies else results.intersection(price_results)
            applied_strategies = True
            
        if criteria.property_type:
            repo = PropertyRepository()
            type_query = repo.db.collection('properties').where('property_type', '==', criteria.property_type)
            type_results = set(repo.search_properties(type_query))
            results = type_results if not applied_strategies else results.intersection(type_results)
            applied_strategies = True
        
        return list(results)