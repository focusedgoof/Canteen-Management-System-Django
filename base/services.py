from .models import Employees, Items, Purchases

def handle_purchase(employee_id, item_id, quantity):
    try:
        employee = Employees.objects.get(Id=employee_id)
        item = Items.objects.get(id=item_id)

        amount = item.Amount * quantity

        if item.Quantity < quantity:
            return False, 'Not enough stock for item: ' + item.ItemName

        Purchases.objects.create(employee=employee, item=item, quantity=quantity, amount=amount)
        item.Quantity -= quantity
        item.save()

        employee.Balance = employee.calculate_new_balance(amount)
        employee.save()

        return True, ''
    except Exception as e:
        return False, str(e)
