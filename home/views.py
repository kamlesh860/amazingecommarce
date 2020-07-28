  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q
from .forms import UserUpdateForm
from ecomm.settings import EMAIL_HOST_USER


# def home(request):
#     product=Procuct.objects.all()
#     return render(request,'home.html',{'pro':product})

# def product_about(request):
#     product=Procuct.objects.all()
#     return render(request,'product_about.html',{'pro':product})


class home(ListView):
    model=Item
    template_name='home.html'
    # return render(request,'home.html',{'pro':product})


class product_about(DetailView):
    model=Item
    template_name='product_about.html'

    # product=Procuct.objects.all()
    # return render(request,'product_about.html',{'pro':product})

# def login(request):
#     return render(request,'login.html')

# def checkout(request):
#     return render(request,'checkout.html')

def register1(request):
    if request.method == 'POST':

        first_name1=request.POST['first_name1']
        last_name1 = request.POST['last_name1']
        email1 = request.POST['email1']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user=User.objects.all()
            for u in user:
                if u.email == email1:
                    return render(request,'login.html',context={'Error Message':'Email id is already registered.'})
            x=User.objects.create_user(username=email1,first_name=first_name1,last_name=last_name1,email=email1,password=password1)
            x.save()
            
            return render(request, 'login.html', context={'info_message': "Account created successfully."})
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')
def login(request):
    if request.method == 'POST':
        email2 = request.POST['username1']
        password3 = request.POST['password']
        user=auth.authenticate(username=email2,password=password3)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid email and password')
            return redirect('login')
    else:
        return render(request,'login.html')


class cart(LoginRequiredMixin,View):
    login_url='login'
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context={'object':order}
            return render(self.request, 'cart.html',context)
        except ObjectDoesNotExist:
            order={'get_total_item_price':0,'get_final_price':0}
            return render(self.request, 'cart.html', {'object':order})


def logout(request):
    auth.logout(request)
    return redirect('home')

# def buynow(request,slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_item, created = OrderItem.objects.get_or_create(item=item,
#                                                           user=request.user, ordered=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         print(order)
#         messages.info(request, 'this item was added')
#         order.items.add(order_item, )
#         return redirect('cart')
#     return redirect('checkout')



@login_required(login_url='login')
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,
        user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        print(order)
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,'this item quantity was updated')
            return redirect('cart')

        else:
            messages.info(request,'this item was added')
            order.items.add(order_item,)
            return redirect('cart')

    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'this item was added')
        return redirect('cart')

    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.quantity=1
            order_item.save()
            messages.info(request,'this item was remove')
            return redirect('cart')
        else:
            messages.info(request,'this item was not in your cart')
            return  redirect('cart')
    else:
        messages.info(request, 'you do not active have an order')
        return redirect('cart')
    return redirect('cart')


@login_required(login_url='login')
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,'this item was updated')
            return redirect('cart')
        else:
            messages.info(request,'this item was not in your cart')
            return  redirect('cart')
    else:
        messages.info(request, 'you do not active have an order')
        return redirect('cart')
    return redirect('cart')



class CheckoutView(LoginRequiredMixin,View):
    login_url='login'
    def get(self, *args, **kwargs):
        for order_item in OrderItem.objects.all():
            order_item.ordered=True
            order_item.save()
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            return render(self.request, 'checkout.html', {'object': order})
        except ObjectDoesNotExist:
            messages.error(
                self.request, ' Your Cart Is Empty')
            return redirect('cart')

    def post(self,*args,**kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            
            if self.request.method == 'POST':
                address =self.request.POST['address']
                country =self.request.POST['state']
                city =self.request.POST['city']
                zipcode =self.request.POST['pincode']

                x=UserDetail.objects.create(user_address=address,country=country,city=city,zip=zipcode)
                x.save()

                
                order.ordered = True
                order.save()
                
                
                
                messages.info(self.request, 'Your Order successfull  confermed Check Your Email...')
                return redirect('cart')
            return render(self.request,'checkout.html')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Your Cart is Empty..')
            return redirect('cart')

class myorder(LoginRequiredMixin,DetailView):
    login_url='login'
    def get(self,*args,**kwargs):
        try:
            order=OrderItem.objects.filter(user=self.request.user,ordered=True)
            context={'object':order}
            return render(self.request, 'myorder.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request,'Sorry sir your do not active have any order...')
            return redirect('cart')








def search(request):
    q=request.GET.get("search",None)
    product=Item.objects.filter(Q(title__icontains=q) | Q(tag__icontains=q) | Q(price__icontains=q))
    context={'object':product}
    return render(request,'search.html',context)


def profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
    context = {'u_form': u_form}
    return render(request, 'profile.html',context)








