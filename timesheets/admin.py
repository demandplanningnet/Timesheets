from dataclasses import Field, fields
from http import client
from importlib import resources
from multiprocessing.connection import Client
from django.contrib import admin
from .models import Admin, Master_db, Client, Project, Category
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import resources
from import_export.fields import Field
from django.db.models import Count
from django.db.models import Sum
from django.contrib.admin import SimpleListFilter


admin.site.site_header = "Timesheets Admin"
admin.site.site_title = "Timesheets Admin"
admin.site.index_title = "Timesheets Admin"
list_per_page = 1

from import_export import widgets,fields,resources
from timesheets.models import Master_db,Client, Category, Project
from import_export import fields
from import_export.fields import Field

class CharRequiredWidget(widgets.CharWidget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            return val
        else:
            raise ValueError('this field is required')


class ForeignkeyRequiredWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            print(self.field, value)
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value})
        else:
            raise ValueError(self.field+ " required")
     
class MasterdbResource(resources.ModelResource):
    client = fields.Field(column_name='client', attribute='client', widget=ForeignkeyRequiredWidget(Client, 'client_name'),
                        saves_null_values=False)
    category = fields.Field(column_name='category', attribute='category', widget=ForeignkeyRequiredWidget(Category, 'category_name'),
                        saves_null_values=False)
    project = fields.Field(column_name='project', attribute='project', widget=ForeignkeyRequiredWidget(Project, 'project_name'),
                        saves_null_values=False)
    week_start = fields.Field(column_name='week_start', attribute='week_start', widget=CharRequiredWidget(),
                        saves_null_values=False)
    # week_end = fields.Field(column_name='week_end', attribute='week_end', widget=CharRequiredWidget(),
    #                     saves_null_values=False)

    class Meta:
        model = Master_db
        fields = ('name','client','project','category','description','billable','hours','date','week_start',)
        clean_model_instances = True

class ClientAdmin(ImportExportModelAdmin):
  
    list_display = ('name','client','project','category','description','date','hours','week_start',)
    list_filter = ( 'name','client', )
    date_hierarchy = 'date'
    resource_class = MasterdbResource

admin.site.register(Master_db, ClientAdmin, )
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Category)
