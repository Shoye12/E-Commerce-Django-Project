from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Cart, Order
from django.contrib.auth.decorators import login_required
from django.db.models import Q

User = get_user_model()


@login_required(login_url='/login/')
def index(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'store/home.html', context)


class ProductDetail(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(
                user=request.user, product=product).exists()

        return render(request, 'store/product_detail.html', {
            'product': product,
            'already_in_cart': already_in_cart
        })

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to add items to your cart.')
            return redirect('login')

        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(
            request, f'{product.name} added to your cart successfully!')
        return redirect('product_detail', product_id=product_id)


class Signup(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'store/signup.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        values = {'name': name, 'phone': phone}

        if len(phone) != 10:
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'store/signup.html', {'values': values})

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, 'This phone number is already registered.')
            return render(request, 'store/signup.html', {'values': values})

        user = User.objects.create_user(
            phone_number=phone,
            password=password,
            first_name=name
        )

        messages.success(
            request, 'Account created successfully! You can now log in.')
        return redirect('login')


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'store/login.html')

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        values = {'phone': phone}

        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Phone Number or Password.')
            return render(request, 'store/login.html', {'values': values})


def logout_user(request):
    logout(request)
    return redirect('index')


class ShowCart(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)

            total_amount = sum(
                item.total_cost for item in cart_items) if cart_items else 0

            return render(request, 'store/cart.html', {
                'cart_items': cart_items,
                'total_amount': total_amount
            })
        else:
            messages.warning(request, "Please log in to view your cart.")
            return redirect('login')


def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        cart_item = Cart.objects.get(product__id=product_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.total_cost for item in cart_items)

        data = {
            'quantity': cart_item.quantity,
            'item_total': cart_item.total_cost,
            'total_amount': total_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        cart_item = Cart.objects.get(product__id=product_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.total_cost for item in cart_items)

        data = {
            'quantity': cart_item.quantity,
            'item_total': cart_item.total_cost,
            'total_amount': total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        cart_item = Cart.objects.get(product__id=product_id, user=request.user)
        cart_item.delete()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.total_cost for item in cart_items)

        return JsonResponse({'total_amount': total_amount})


class Checkout(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to proceed to checkout.")
            return redirect('login')

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items:
            return redirect('show_cart')

        # FIXED: Now correctly using item.total_cost
        total_amount = sum(item.total_cost for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
        }

        return render(request, 'store/checkout.html', context)

    def post(self, request):
        user = request.user
        customer_name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')

        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            Order.objects.create(
                user=user,
                customer_name=customer_name,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                phone=phone,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()
        messages.success(
            request, f"Congratulations {customer_name}! Your order has been placed successfully.")
        return redirect('index')

class Orders(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to view your orders.")
            return redirect('login')

        # Fetch all orders for this user, sorted by newest first!
        user_orders = Order.objects.filter(
            user=request.user).order_by('-order_date')

        return render(request, 'store/orders.html', {'orders': user_orders})

class Search(View):
    def get(self, request):
        query = request.GET.get('query', '')

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            products = Product.objects.none()

        context = {
            'products': products,
            'query': query,
        }

        return render(request, 'store/search.html', context)
