from django.shortcuts import get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('item_list')  # Redirect to desired page after login
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page or home page after signup
            return redirect('login')  # or 'item_list'
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'myapp/logout_page.html')  # Redirects to your custom login view

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'myapp/item_list.html', {'items': items})


@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'myapp/item_form.html', {'form': form})


@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'myapp/item_form.html', {'form': form})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})


@login_required
def item_summary(request):
    items = Item.objects.all()
    total_price = sum(item.price for item in items)
    return render(request, 'myapp/item_summary.html', {
        'items': items,
        'total_price': total_price
    })
