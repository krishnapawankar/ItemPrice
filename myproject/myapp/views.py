import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import DatabaseError
from .models import Item
from .forms import ItemForm

# Configure logging
logger = logging.getLogger(__name__)


def login_view(request):
    """Custom login method."""
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                return redirect('item_list')
        else:
            form = AuthenticationForm()
    except ValidationError as e:
        logger.error(f"Login validation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
    return render(request, 'myapp/login.html', {'form': form})


def signup(request):
    """Custom user signup method."""
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
    except ValidationError as e:
        logger.error(f"Signup validation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during signup: {e}")
    return render(request, 'myapp/signup.html', {'form': form})


@login_required
def custom_logout(request):
    """Custom logout method."""
    try:
        logout(request)
    except Exception as e:
        logger.error(f"Error during logout: {e}")
    return render(request, 'myapp/logout_page.html')


@login_required
def item_list(request):
    """List all items with their price."""
    try:
        items = Item.objects.all()
    except DatabaseError as e:
        logger.error(f"Database error fetching items: {e}")
        return render(request, 'myapp/error.html')
    return render(request, 'myapp/item_list.html', {'items': items})


@login_required
def item_add(request):
    """Add a new item."""
    try:
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('item_list')
        else:
            form = ItemForm()
    except ValidationError as e:
        logger.error(f"Item add validation error: {e}")
    except DatabaseError as e:
        logger.error(f"Database error adding item: {e}")
    return render(request, 'myapp/item_form.html', {'form': form})


@login_required
def item_edit(request, pk):
    """Edit an existing item."""
    try:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('item_list')
        else:
            form = ItemForm(instance=item)
    except ObjectDoesNotExist:
        logger.error(f"Item with pk {pk} not found for editing")
        return redirect('item_list')
    except ValidationError as e:
        logger.error(f"Item edit validation error: {e}")
    except DatabaseError as e:
        logger.error(f"Database error editing item with pk {pk}: {e}")
    return render(request, 'myapp/item_form.html', {'form': form})


@login_required
def item_delete(request, pk):
    """Delete an item."""
    try:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            item.delete()
            return redirect('item_list')
    except ObjectDoesNotExist:
        logger.error(f"Item with pk {pk} not found for deletion")
    except DatabaseError as e:
        logger.error(f"Database error deleting item with pk {pk}: {e}")
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})


@login_required
def item_summary(request):
    """Item summary displays all the items with their total cost."""
    try:
        items = Item.objects.all()
        total_price = sum(item.price for item in items)
    except DatabaseError as e:
        logger.error(f"Database error generating summary: {e}")
        return render(request, 'myapp/error.html')
    return render(request, 'myapp/item_summary.html', {
        'items': items,
        'total_price': total_price
    })
