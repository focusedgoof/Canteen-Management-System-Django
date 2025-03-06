from django.db import models
from django.contrib.auth.models import User


class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee_profile')
    Id = models.PositiveIntegerField(unique=True)  
    FirstName = models.CharField(max_length=200)
    FirstName=models.CharField(max_length=200)
    LastName=models.CharField(max_length=200)
    MailId=models.EmailField()
    Balance = models.PositiveIntegerField( default=0)    
    updated =models.DateTimeField(auto_now =True)
    created=models.DateTimeField(auto_now_add=True)    
    
    class Meta:
        ordering =['-updated','-created']
    
    def __str__(self):
        return str(self.Id)
    
    def calculate_new_balance(self, total_amount):
        current_balance = self.Balance
        new_balance = current_balance - total_amount
        return new_balance
    
   
class Items(models.Model):
    ItemName=models.CharField(max_length=200)
    Quantity=models.PositiveIntegerField()
    Amount=models.PositiveIntegerField()
    updated =models.DateTimeField(auto_now =True)
    created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['-updated','-created']
    
    def __str__(self):
        return str(self.ItemName)
    

class Purchases(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(editable=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.amount = self.item.Amount * self.quantity
        self.item.Quantity -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase by {self.employee} of {self.quantity} {self.item.ItemName}(s) on {self.purchased_at}"

