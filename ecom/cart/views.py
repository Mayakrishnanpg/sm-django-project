from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from product.models import ProductDetails
from .models import cart,PurchasedItem
import razorpay 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

razorpay_client = razorpay.Client(auth = (settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))

@login_required(login_url="signin")
def CartView(request):
    product= cart.objects.filter(user=request.user)
    total=0
    for item in product:
        total=total + item.product.Product_Price

        
    context ={
        "products":product,
        "total":total,
    
    }
    return render(request,'cart.html',context)
@login_required(login_url="signin")
def AddCart(request,pk):
    product = ProductDetails.objects.get(Product=pk)
    cartitem = cart.objects.create(product = product,numberofitems = 1,user = request.user)
    cartitem.save()
    return redirect("CartView")
@login_required(login_url="signin")
def Delete(request,pk):
    cartitem= cart.objects.get(id= pk)
    cartitem.delete()
    return redirect("CartView")

def Placeorder(request):
    product=cart.objects.filter(user=request.user)
    for item in product:
        product=item.product
        pitem=PurchasedItem.objects.create(product = product,user = request.user)
        pitem.save()
        item.delete()
    product = PurchasedItem.objects.filter(user = request.user,paymentstatus = False)
    total=0 
    for item in product:
        total = total + item.product.Product_Price
        
    currency ='INR'
    amount = total * 100
    # amount = total
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture=0))
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'paymenthandler/'
           
    context={
        "total":total,
        "razorpay_order_id":razorpay_order_id,
        "razorpay_merchant_key":settings.RAZOR_KEY_ID,
        "razorpay_amount":amount,
        'currency':currency,
        'callback_url':callback_url,
        'slotid':"1"
    }
    return render(request, "payment.html",context)
@csrf_exempt   
def  paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id =request.POST.get('razorpay_payment_id','')
            razorpay_order_id = request.POST.get("razorpay_order_id","")
            signature = request.POST.get('razorpay_signature','')
            params_dict={
                "razorpay_order_id":razorpay_order_id,
                "razorpay_payment_id":payment_id,
                "razorpay_signature":signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 5000
                razorpay_client.payment.capture(payment_id,amount)
                return HttpResponse("Payment Done")
            else:
                return HttpResponse("Done")
        except:
            products=PurchasedItem.objects.filter(user = request.user,paymentstatus =False)
            for item in products:
                item.paymentstatus=True
                item.save()
            return HttpResponse("Not Done")
     
def customerorders(request):
    products=PurchasedItem.objects.all()
    context={
        "products":products
    }
    return render(request,"admin/order.html",context) 


