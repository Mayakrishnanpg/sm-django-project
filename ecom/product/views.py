from django.shortcuts import render,redirect
from .forms import ProductAddForm
from django.contrib import messages
from .models import ProductDetails
from django.contrib.auth.decorators import login_required

@login_required(login_url="SignIn")
def Addproduct(request):
    form = ProductAddForm()
    if request.method == "POST":
        form= ProductAddForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save()
            product.Merchant = request.user
            product.save()
            messages.info(request,"product added To list")
            return redirect("Addproduct")
    return render(request,"admin/addproduct.html",{"forms":form})

def ProductViewMerchant(request):
    product = ProductDetails.objects.all()
    context = {
        "product":product
    }
    return render(request,"admin/productlist.html",context)
@login_required(login_url="SignIn")
def DeleteProduct(request,pk):
    product = ProductDetails.objects.get(Product = pk)
    product.delete()
    messages.info(request,"Product deleted")
    return redirect("ProductViewMerchant")
@login_required(login_url="SignIn")
def UpdateProduct(request,pk):
    Product=ProductDetails.objects.filter(Product=pk)
    if request.method == "POST":
        
        pname =request.POST['pname']
        pbrand=request.POST['pbrand']
        pdisc=request.POST['pdisc']
        pstock=request.POST['pstock']
        price=request.POST['price']
        pcat=request.POST['pcat']
        image=request.FILES["image"]
        
        item=ProductDetails.objects.get(Product=pk)
        
        item.Product_Name=pname
        item.Product_Brand=pbrand
        item.Product_Discription=pdisc
        item.Product_Stock=pstock
        item.Product_Price=price
        item.Product_Category=pcat
        item.Product_Image.delete()
        item.Product_Image=image
        item.save()
        messages.info(request,"items Updated")
        return redirect("UpdateProduct",pk=pk)
    
    
    context={
        "product":Product
    }
    return render(request,"admin/updateproduct.html",context)
@login_required(login_url="signin")
def ProductView(request,pk):
     Product=ProductDetails.objects.filter(Product=pk)
     item=ProductDetails.objects.get(Product=pk)
     context={
         "product":Product
     }
     return render(request,"productview.html",context)



