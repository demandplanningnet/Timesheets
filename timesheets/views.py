import datetime
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models.functions import Now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from timesheets.forms import Masterdb, CreateUserForm
from timesheets.models import Master_db
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import generic
import xlwt
from timesheets.models import Admin, Client, Project, Master_db, Users
from .forms import Masterdb
# Create your views here.

### CODE BLOCK FOR FORM VIEW
def addEntry(request):
    name = request.user
    results = Master_db.objects.filter(name = name).order_by('-timesheetid')[:5]
    
    if request.method =="POST":
        form = Masterdb(request.POST)
        if form.is_valid():
            masterdb_item = form.save(commit = False)
            masterdb_item.save()
            form = Masterdb()
            messages.success(request, 'Entry Saved Successfully')
    else:
        form  = Masterdb()
    
    return render (request, 'timesheet.html', {'form': form,'addEntry':results})

### CODE BLOCK FOR FORM VIEW ENDS

### CODE BLOCK FOR AUTHENTICATION
def registerpage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render (request, 'register.html', context)

from django.contrib import messages
def loginpage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('userentry')
        else:
            messages.success(request, 'Incorrect Username or Password')
            return render(request,'login.html')

    context = {}
    return render (request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginpage')

### CODE BLOCK FOR AUTHENTICATION ENDS

### CODE BLOCK FOR PULLING IN DATA

def newentry(request):
    return render(request, 'home.html')

from django.utils import timezone
from datetime import date, timedelta, datetime
@login_required


def updatentry(request): 
       
            #results = Master_db.objects.all()
        time_threshold = datetime.now() - timedelta(days=14)
        now = timezone.now()
        results = Master_db.objects.filter(date__gt = time_threshold).order_by("-timesheetid")
        return render(request, "previous.html",{'updatentry':results})


def editentry(request,id):

    entries = Master_db.objects.get(timesheetid = id)
    form = Masterdb(instance=entries)

    if request.method =="POST":
        form = Masterdb(request.POST, instance=entries)
        if form.is_valid():
            form.save()
            return redirect('preventry')
    context = {'form':form }
    return render(request, 'edit.html', context)


def deletentry(request, id):
    entries = Master_db.objects.get(timesheetid = id)
    entries.delete()
    return render(request, 'delete.html')

def userentry(request): 
       
        #results = Master_db.objects.all()
        time_threshold = datetime.now() - timedelta(days=14)
        now = timezone.now()
        name = request.user
        results = Master_db.objects.filter(date__gt = time_threshold, name = name).order_by("-timesheetid")
        # results = Master_db.objects.aggregate(
        #     last_14_days = models.Count('timesheetid',filter=models.Q(date=(now - timedelta(days=14)).date())),
        # )
        # status_filter = UserFilter(request.GET, queryset=results)
        return render(request, "userentry.html",{'userentry':results})

### CODE BLOCK FOR PULLING IN DATA ENDS

### CODE BLOCK FOR EXCEL EXPORT

def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Master_db'+ \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Master_db')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['billable','date','hours','description','name', 'client_name','project', 'category']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Master_db.objects.values_list(
        'billable','date','hours','description','name', 'client' ,'project', 'category')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]), font_style)
    wb.save(response)
    return response

### CODE BLOCK FOR EXCEL ENDS


### CODE BLOCK FOR TABLE VIEW
from django.shortcuts import render

# importing formset_factory
from django.forms import formset_factory
@login_required
def table_view(request):
    name = request.user
    results = Master_db.objects.filter(name = name).order_by('-timesheetid')[:5]
    extra_forms = 1
   
    AddnewFormset = formset_factory(Masterdb, extra=extra_forms)
    formset = AddnewFormset()
    if request.method == 'POST':
        if 'additems' in request.POST and request.POST['additems']  == "true":
            
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = int(formset_dictionary_copy['form-TOTAL_FORMS']) + extra_forms
            print(formset_dictionary_copy)
            formset = AddnewFormset( formset_dictionary_copy)
        elif 'additems1' in request.POST and request.POST['additems1']  == "true":
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = int(formset_dictionary_copy['form-TOTAL_FORMS']) - extra_forms
            print(formset_dictionary_copy)
            formset = AddnewFormset( formset_dictionary_copy)
        
        else:
            formset = AddnewFormset(request.POST)
          
            if formset.is_valid():
                    for form in formset:
                        if form.cleaned_data:
                            entry = form.save(commit=False)
                            entry.save()
                            messages.success(request, 'Entries Saved Successfully')
                    return redirect('tableview')
    return render(request, 'table-view.html', {'formset': formset,'addEntry':results})

### CODE BLOCK FOR TABLE VIEW ENDS