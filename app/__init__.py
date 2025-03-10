from flask import Flask
import yaml

app = Flask(__name__)

# Load config
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

app.config['DATABASES'] = config['databases']

from app.routes import *