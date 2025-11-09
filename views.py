from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import RegisterForm, ProductForm
import csv
from django.http import HttpResponse

def home(request):
    search = request.GET.get('search','')
    products = Product.objects.filter(is_deleted=False, name__icontains=search)
    return render(request, 'shop/home.html', {'products': products, 'search': search})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Added to cart')
    return redirect('cart')

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        subtotal = product.price * qty
        total += subtotal
        items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        total = 0
        order = Order.objects.create(user=request.user, total_price=0)
        for pid, qty in cart.items():
            product = get_object_or_404(Product, id=pid)
            total += product.price * qty
            OrderItem.objects.create(order=order, product=product, qty=qty, price=product.price)
        order.total_price = total
        order.save()
        request.session['cart'] = {}
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')
    return render(request, 'shop/checkout.html')

def order_success(request):
    return render(request, 'shop/order_success.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def admin_check(user):
    return user.is_staff

@user_passes_test(admin_check)
def admin_dashboard(request):
    return render(request, 'shop/admin/dashboard.html', {
        'orders': Order.objects.count(),
        'products': Product.objects.count(),
    })

@user_passes_test(admin_check)
def admin_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm()
    products = Product.objects.all()
    return render(request, 'shop/admin/products.html', {'products': products, 'form': form})

@user_passes_test(admin_check)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    if request.method == 'POST' and 'export' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'
        writer = csv.writer(response)
        writer.writerow(['ID','User','Total','Status','Date'])
        for o in orders:
            writer.writerow([o.id, o.user.username, o.total_price, o.status, o.created_at])
        return response
    return render(request, 'shop/admin/orders.html', {'orders': orders})

@user_passes_test(admin_check)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    status = request.POST.get('status')
    if status:
        order.status = status
        order.save()
    return redirect('admin_orders')
from django.shortcuts import render

# Create your views here.
