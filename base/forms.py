from django.forms import ModelForm
from .models import Items, Employees, Purchases

class ItemForm(ModelForm):
    class Meta:
        model =Items
        fields = '__all__'
        
class EmployeeForm(ModelForm):
    class Meta:
        model =Employees
        fields = '__all__'
        
class PurchaseForm(ModelForm):
    class Meta:
        model =Purchases
        fields = '__all__'
        
        
        

