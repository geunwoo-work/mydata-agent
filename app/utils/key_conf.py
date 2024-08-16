import os
from dotenv import load_dotenv
import importlib

load_dotenv()
settings = os.getenv('settings')
KEY_CONF = importlib.import_module("settings." + settings + ".KEY_CONF")
os.environ['OPENAI_API_KEY'] = KEY_CONF.OPENAI_API_KEY
