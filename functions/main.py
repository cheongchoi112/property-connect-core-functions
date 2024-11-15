import sys
from pathlib import Path
import firebase_admin
from firebase_admin import credentials


sys.path.insert(0, Path(__file__).parent.as_posix())

from presentation.handle_property_crud import *
from presentation.handle_property_search import *

# Initialize Firebase Admin
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

