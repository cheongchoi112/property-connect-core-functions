from abc import ABC, abstractmethod
from typing import List, Set
from google.cloud.firestore_v1 import FieldFilter  # Import FieldFilter

from domain.models import Property, SearchCriteria
from infrastructure.property_repository import PropertyRepository

import logging

class SearchStrategy(ABC):
    """
    Application Layer: Abstract base class for search strategies.

    This class uses the Strategy design pattern to define a family of search strategies,
    encapsulate each one, and make them interchangeable. This allows the algorithm to vary independently
    from the clients that use it.
    """
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[Property]:
        pass

class CitySearchStrategy(SearchStrategy):
    """
    Application Layer: Search strategy for filtering properties by city.
    """
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.city:
            # Use FieldFilter with filter keyword argument
            query = query.where(filter=FieldFilter('city', '==', criteria.city))
        
        return repo.search_properties(query)

class PriceRangeSearchStrategy(SearchStrategy):
    """
    Application Layer: Search strategy for filtering properties by price range. This srearch strategy is not implemented in the frontend.
    """
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.price_range:
            query = query.where(filter=FieldFilter('price', '>=', criteria.price_range.min_price))\
                         .where(filter=FieldFilter('price', '<=', criteria.price_range.max_price))
        
        return repo.search_properties(query)

class PropertyTypeSearchStrategy(SearchStrategy):
    """
    Application Layer: Search strategy for filtering properties by property type.
    """
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.property_type:
            query = query.where(filter=FieldFilter('property_type', '==', criteria.property_type))
        
        return repo.search_properties(query)

class ListingTypeSearchStrategy(SearchStrategy):
    """
    Application Layer: Search strategy for filtering properties by listing type.
    """
    def search(self, criteria: SearchCriteria) -> List[Property]:
        repo = PropertyRepository()
        query = repo.db.collection('properties')
        
        if criteria.listing_type:
            query = query.where(filter=FieldFilter('listing_type', '==', criteria.listing_type))
        
        return repo.search_properties(query)

class SearchStrategyEngine(SearchStrategy):
    """
    Application Layer: Engine for applying multiple search strategies.
    """
    def search(self, criteria: SearchCriteria) -> List[Property]:
        results: Set[Property] = set()
        applied_strategies = False
        
        if criteria.city:
            address_results = set(CitySearchStrategy().search(criteria))
            results = address_results if not applied_strategies else results.intersection(address_results)
            applied_strategies = True
            
        if criteria.price_range:
            price_results = set(PriceRangeSearchStrategy().search(criteria))
            results = price_results if not applied_strategies else results.intersection(price_results)
            applied_strategies = True
            
        if criteria.property_type:
            property_type_results = set(PropertyTypeSearchStrategy().search(criteria))
            results = property_type_results if not applied_strategies else results.intersection(property_type_results)
            applied_strategies = True
        
        if criteria.listing_type:
            listing_type_results = set(ListingTypeSearchStrategy().search(criteria))
            results = listing_type_results if not applied_strategies else results.intersection(listing_type_results)
            applied_strategies = True
        
        if not applied_strategies:
            logging.warning("No search criteria provided.")
        
        return list(results)