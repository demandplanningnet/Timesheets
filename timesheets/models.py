from random import choices
from django.db import models
from django.forms import CharField
import django
import datetime
from django.utils.timezone import now

# Create your models here.

# def previous_week_range(date):
#     start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
#     # end_date = date + datetime.timedelta(-date.weekday() - 1)
#     return start_date

###  MODELS CODE BLOCK START HERE
class Users(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.client_name
    
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.project_name


class Category(models.Model):
    category_id = models.AutoField(primary_key = True)
    category_name = models.CharField( max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.category_name
choices = [
    ('yes', 'yes'),
    ('no',"no"),
    # ('choice3',"choice3")
]
from datetime import datetime, timedelta



class Master_db(models.Model):   
    timesheetid = models.AutoField(primary_key=True)
    #client_name = models.CharField(max_length=100)
    #project_name = models.CharField(max_length = 100)
    #category_name = models.CharField(max_length=100)
    billable = models.CharField(max_length = 10, choices = choices)
    date = models.DateField()
    hours = models.FloatField()
    description = models.CharField(max_length = 500)
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, default = 1, on_delete= models.SET_DEFAULT)
    project = models.ForeignKey(Project, default = 1, on_delete= models.SET_DEFAULT)
    category = models.ForeignKey(Category, default = 1, on_delete=models.SET_DEFAULT)
    # week_start_date = models.DateField(default=now, blank=True)
    # week_end_date = models.DateField(default=now, blank=True)
    
    # _week_start = models.DateField( db_column='week_start')
    # week_end = models.DateField()
    # week_start = models.DateTimeField(previous_week_range(date))

    # @property
    # def week_start(self):
        
        
    #     return self._week_start

    # @week_start.setter
    # def week_start(self, value):
    #     self._week_start = self.date - timedelta(days = self.date.weekday() +1)
       
    

    @property
    def week_start(self):
        week_start = self.date - timedelta(days = self.date.weekday() +1)
        # week_end = self.date - timedelta(days=self.date.weekday() - 5)
        return week_start


    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    ##
        self._meta.local_fields = [f for f in self._meta.local_fields if f.name not in ('week_start', 'week_end')]
        super(Master_db, self).save(force_insert, force_update, using, update_fields)


### MODELS CODE BLOCK ENDS HERE

