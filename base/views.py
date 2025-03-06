from django.shortcuts import render, redirect, get_object_or_404
from .services import handle_purchase
from .models import Employees, Items, Purchases
from .forms import ItemForm, EmployeeForm, PurchaseForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


#for the login and logout
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')
        
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
            
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')        
        else:
            messages.error(request,'Username or password does not exist')
            
    
    context={'page':page}
    return render(request,'base/login_registration.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method =='POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('createUser')
        else:
            messages.error(request,'An error occured during registration')
    
    return render(request,'base/login_registration.html',{'form':form})


 #for the home page with an opeinig message 


def home(request):
    employeeData=Employees.objects.all()
    context={'employeeData':employeeData}
    return render(request,'base/home.html',context)


#for the items portal in admin
def items(request):    
    i=request.GET.get('i') if request.GET.get('i') !=None else ''
    items= Items.objects.filter(ItemName__icontains=i)
    context={'items':items}
    return render(request,'base/admin/items/items.html',context)

def employeeData(request):    
    #search
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    employeeData= Employees.objects.filter(
        Q(Id__contains=q)|
        Q(FirstName__icontains=q)
    )    
    context={'employeeData':employeeData}
    return render(request,'base/admin/employees_detail.html',context)

def allPurchaseHistory(request):
    purchases = Purchases.objects.all().order_by('-purchased_at')
    context = {'purchases': purchases}
    return render(request, 'base/purchase/purchase_history.html', context)


#for the employees and items portal
def itemInfo(request,pk):
    itemInfo= Items.objects.get(id=pk)
    context={'itemInfo':itemInfo}            
    return render(request,'base/admin/items/items_info.html',context)

def employeeInfo(request,pk):
    employeeInfo= Employees.objects.get(Id=pk)
    context={'employeeInfo':employeeInfo}            
    return render(request,'base/employee/employee_info.html',context)


#add Item and User
def createItem(request):
    form= ItemForm()
    
    if request.method =="POST":
        form=ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    
    context={'form':form}
    return render(request,'base/admin/items/item_form.html',context)

def createUser(request):
    form= EmployeeForm()
    
    if request.method =="POST":
        form=EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request,'base/admin/employee/employee_form.html',context)


#update Item and employee data
def updateItem(request, pk):
    item = get_object_or_404(Items, id=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm(instance=item)
    
    context = {'form': form}
    return render(request, 'base/admin/items/item_form.html', context)

def updateUser(request, pk):
    employee = get_object_or_404(Employees, Id=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employeeData')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {'form': form}
    return render(request, 'base/admin/employee/employee_form.html', context)


#delete Item and employee data
def deleteItem(request,pk):
    item=Items.objects.get(id=pk)
    if request.method =='POST':
        item.delete()
        return redirect('items')
    return render(request,'base/admin/delete.html',{'obj':item})

def deleteUser(request,pk):    
    user=Employees.objects.get(id=pk)
    if request.method =='POST':
        user.delete()
        return redirect('items')
    return render(request,'base/admin/delete.html',{'obj':user})


def makePurchase(request, pk):
    employee = Employees.objects.get(Id=pk)
    items = Items.objects.all()
    form = PurchaseForm()

    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        quantities = request.POST.getlist('quantity')

        if len(item_ids) != len(quantities):
            return render(request, 'base/purchase/make_purchase.html', {
                'employee': employee,
                'items': items,
                'form': form,
                'error': 'Mismatch between items and quantities'
            })

        total_amount = 0
        for item_id, quantity in zip(item_ids, quantities):
            quantity = int(quantity)
            item = Items.objects.get(id=item_id)
            total_amount += item.Amount * quantity

        if employee.Balance < total_amount:
            return render(request, 'base/purchase/make_purchase.html', {
                'employee': employee,
                'items': items,
                'form': form,
                'error': 'Insufficient balance'
            })

        for item_id, quantity in zip(item_ids, quantities):
            quantity = int(quantity)
            success, error_message = handle_purchase(employee.Id, item_id, quantity)
            if not success:
                return render(request, 'base/purchase/make_purchase.html', {
                    'employee': employee,
                    'items': items,
                    'form': form,
                    'error': error_message
                })

        if 'admin' in request.user.username.lower():
            return redirect('allPurchaseHistory')
        else:
            return redirect('employeePurchaseHistory', pk=employee.Id)

    context = {
        'employee': employee,
        'items': items,
        'form': form,
    }
    return render(request, 'base/purchase/make_purchase.html', context)

def employeePurchaseHistory(request, pk):
    employee_profile = get_object_or_404(Employees, Id=pk)    
    purchases = Purchases.objects.filter(employee=employee_profile).order_by('-purchased_at')
    
    context = {
        'employee': employee_profile,
        'purchases': purchases
    }
    return render(request, 'base/employee/employee_purchase_history.html', context)



#logout
# def logout