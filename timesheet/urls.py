"""timesheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from io import IncrementalNewlineDecoder
from unicodedata import name
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.urls import reverse

import timesheets
from timesheets import views
# from timesheets.views import CreateEntry, DeleteEntry, RetriveEntry, UpdateEntry, export_excel, logoutUser


urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^', include('timesheets.urls')),
    # path('user/entries/', CreateEntry.as_view(), name = 'createentry'),
    # path('user/getentry/<int:pk>/', RetriveEntry.as_view, name = 'getentry'),
    # path('user/updateentry/<int:pk>/', UpdateEntry.as_view(), name = 'updateentry'),
    # path('user/delete/<int:pk>/', DeleteEntry.as_view(), name = 'deleteentry'),
    # path('', include('timesheets.urls')),
    path('', views.loginpage, name = 'loginpage'),
    path('login/', views.loginpage, name = 'loginpage'),
    path('register/', views.registerpage, name = 'registerpage'),
    path('loginback/', views.logoutUser, name = 'logoutUser'),
    path('newentry/', views.newentry, name = 'newentry'),
    path('preventry/', views.updatentry, name = 'preventry'),
    path('edit/<int:id>', views.editentry, name = 'editentry'),
    path('delete/<int:id>', views.deletentry, name = 'deletentry'),
    path('addentry/', views.addEntry, name = 'addentry'),
    path('export-excel/', views.export_excel, name = 'export-excel'),
    path('table-view/', views.table_view, name = 'tableview'),
    path('userentry/', views.userentry, name = 'userentry')
    
    # path('viewentry/', views.viewentry, name = 'viewentry')
]
