from django.forms import ModelForm
from .models import ProductDetails

class ProductAddForm(ModelForm):
    class Meta:
        model = ProductDetails
        fields = ["Product_Name","Product_Brand","Product_Discription","Product_Price","Product_Category","Product_Stock","Product_Image"]