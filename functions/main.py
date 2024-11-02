import sys
from pathlib import Path
import firebase_admin

sys.path.insert(0, Path(__file__).parent.as_posix())

from property_listing.handle_property_crud import *
from property_listing.handle_property_search import *

# Initialize Firebase Admin
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

