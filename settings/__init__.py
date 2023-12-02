import os
from dotenv import load_dotenv

load_dotenv()

from settings.base import *

if os.environ.get("ENVIRONMENT") == 'production':
	from settings.production import *
else:
	from settings.development import *