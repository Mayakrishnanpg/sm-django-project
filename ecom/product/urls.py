from django.urls import path
from .import views
urlpatterns = [
    path("Addproduct",views.Addproduct,name="Addproduct"),
    path ("ProductViewMerchant",views.ProductViewMerchant,name="ProductViewMerchant"),
    path("DeleteProduct/<int:pk>",views.DeleteProduct,name="DeleteProduct"),
    path("UpdateProduct/<int:pk>",views.UpdateProduct,name="UpdateProduct"),
    path("ProductView/<int:pk>",views.ProductView,name="ProductView"),

 ]