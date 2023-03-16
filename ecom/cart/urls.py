from django.urls import path
from .import views
urlpatterns = [
    path("CartView",views.CartView,name="CartView"),
    path("AddCart/<int:pk>",views.AddCart,name="AddCart"),
    path("Delete/<int:pk>",views.Delete,name="Delete"),
    path("Placeorder",views.Placeorder,name="Placeorder"),
    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("customerorders",views.customerorders,name="customerorders")
]