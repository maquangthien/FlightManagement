from app import admin, db
from flask_admin.contrib.sqla import ModelView
from app.models import *
from flask_admin import Admin, AdminIndexView, expose


class AirportView(ModelView):
    can_export = True
    can_delete = True
    can_view_details = True
    form_columns = ('name',)
    edit_modal = True
    column_searchable_list = ['code', 'name', 'location']
    column_filters = ['code', 'name', 'location']


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', msg="hoàng")

class FlightView(ModelView):
    can_export = True
    can_view_details = True
    column_list = ['name', 'airplane', 'route']
    def __str__(self):
        return self.name
class AirPlaneView(ModelView):
    column_list = ['name', 'airline']
    def __str__(self):
        return self.name

admin = Admin(app=app, name="Flight Managerment",
              template_mode='bootstrap4',
            index_view=MyAdminIndexView())

admin.add_view(AirportView(Airport, db.session))
admin.add_view(AirPlaneView(Airplane, db.session))
admin.add_view(ModelView(Airline, db.session))
admin.add_view((ModelView(Seat, db.session)))
admin.add_view((FlightView(Flight, db.session)))
