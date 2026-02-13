
from django.shortcuts import render,redirect

from cart.cart import Cart
from .models import Product,Category, Profile
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated")
				login(request, current_user)
				return redirect('store:')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('store:update_password') #
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('store:home')
        

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)            
            messages.success(request, "Profile updated successfully")
            return redirect('store:home')
        return render(request, "update_user.html", {'user_form': user_form })
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect('store:login')
        




def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(Product=key, Quantity=value)


                request.session['session_key'] = eval(saved_cart)

            messages.success(request, ("You have been logged in"))
            return redirect('store:home')
        else:
            messages.success(request, ("There has been some error"))
            return redirect('store:login')
    return render(request, 'login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out succesfully"))
    return redirect('store:home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have been registered"))
            return redirect('store:home')
        else:
            messages.success(request,("Unsuccessful registration. Invalid information."))

    else:
        return render(request ,'register.html',{'form':form}) 


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, category_name):       
   category_name = category_name.replace('-',' ')
   try:
       category = Category.objects.get(name__iexact=category_name)
       products = Product.objects.filter(category=category)
       return render(request, 'category.html', {'products':products, 'category':category})
   except Category.DoesNotExist:
         messages.error(request,("No products found in this category"))
         return redirect('store:home')
   

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile info has been updated successfully")
            return redirect('store:home')
        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect('store:login')

def search(request):
     if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        return render(request, 'search.html', {'searched': searched, 'products': products})
        if not searched:
            messages.info(request, "No search term entered.")
            return redirect('store:search')
        else:
             return render(request, 'search.html', {'searched': searched, 'products': products})
     else:
        return render(request, 'search.html')
