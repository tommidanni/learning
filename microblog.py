from app import app, db
from app.models import Product, User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product}