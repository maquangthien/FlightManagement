from app import admin, db
from flask_admin.contrib.sqla import ModelView
from app.models import Airport

admin.add_view(ModelView(Airport,db.session))
