from django.urls import path
from . import views

urlpatterns=[
     path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='registerPage'),
    
    path('',views.home, name='home'),
    path('items/',views.items, name='items'),
    path('employee-detail/',views.employeeData, name='employeeData'),
    path('purchases/', views.allPurchaseHistory, name='allPurchaseHistory'), 
 
    path('employee-info/<int:pk>/',views.employeeInfo, name='employeeInfo'),
    path('item-info/<int:pk>/',views.itemInfo, name='itemInfo'),
    
    path('add-item/',views.createItem,name='createItem'),
    path('add-employee/',views.createUser,name='createUser'),
    
    path('update-item/<int:pk>',views.updateItem,name='updateItem'),
    path('update-employee/<int:pk>',views.updateUser,name='updateUser'),
    
    path('delete-item/<int:pk>',views.deleteItem,name='deleteItem'),
    path('delete-employee/<int:pk>',views.deleteUser,name='deleteUser'),
    
    path('make-purchase/<str:pk>/', views.makePurchase, name='makePurchase'),
   path('purchase-history/<int:pk>/', views.employeePurchaseHistory, name='employeePurchaseHistory'),
    
]