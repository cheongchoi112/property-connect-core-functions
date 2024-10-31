from google.cloud import firestore
from datetime import datetime
from typing import List, Optional
from .models import Property, PropertyCreate, PropertyUpdate
import firebase_admin

class PropertyRepository:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            project_id = firebase_admin.get_app().project_id

            cls._instance.db = firestore.Client(project=project_id)
        return cls._instance
    
    def create_property(self, property_data: PropertyCreate, user_id: str) -> Property:
        doc_ref = self.db.collection('properties').document()
        property_dict = property_data.dict()
        property_dict.update({
            'id': doc_ref.id,
            'owner_user_id': user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        print(property_dict)
        doc_ref.set(property_dict)
        return Property(**property_dict)
    
    def get_property(self, property_id: str) -> Optional[Property]:
        doc = self.db.collection('properties').document(property_id).get()
        
        if doc.exists:
            data = doc.to_dict()
            print(f'Document data: {data}')
        else:
            print(f'Document with {property_id}  does not exist.')

        return Property(**doc.to_dict()) if doc.exists else None
    
    def update_property(self, property_id: str, property_data: PropertyUpdate) -> Optional[Property]:
        doc_ref = self.db.collection('properties').document(property_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
            
        update_dict = property_data.dict()
        update_dict['updated_at'] = datetime.utcnow()
        
        doc_ref.update(update_dict)
        updated_doc = doc_ref.get()
        return Property(**updated_doc.to_dict())
    
    def delete_property(self, property_id: str) -> bool:
        doc_ref = self.db.collection('properties').document(property_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return False
            
        doc_ref.delete()
        return True

    def search_properties(self, query) -> List[Property]:
        properties_ref = self.db.collection('properties')
        return [Property(**doc.to_dict()) for doc in query.stream()]