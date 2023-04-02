from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderProduct
from django.views.generic import ListView, DetailView
from django.db import IntegrityError, transaction


def index(request):
    products = Product.objects.all()
    return render(request, 'app/index.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_list.html', context)


def order_list(request):
    orders_list = Order.objects.all()
    order_product_list = OrderProduct.objects.all()
    return render(request, 'app/orders_list.html',
                  {'orders_list': orders_list, 'order_product_list': order_product_list})


class ProductView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'


def create_order(request):
    if request.method == 'POST':
        # get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        products = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        try:
            with transaction.atomic():
                # create Order instance
                order = Order.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address
                )

                for i, product_id in enumerate(products):
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantities[i])

                    # check if there is enough product in stock
                    print('product.quantity', product.quantity, ' - quantity', product.quantity)
                    if product.quantity < quantity:
                        raise ValueError(f"Not enough {product.name} in stock")

                    # create OrderProduct instance
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity
                    )

            # redirect to order confirmation page
            return redirect('app:order_confirmation', order_id=order.id)

        except:
            transaction.rollback()
            message = f"Недостаточно '{product.name}' на складе"
            products = Product.objects.all()
            context = {'products': products, 'message': message}
            return render(request, 'app/create_order.html', context)

    else:
        # get all products
        products = Product.objects.all()

        context = {'products': products}
        return render(request, 'app/create_order.html', context)


def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'app/order_confirmation.html', {'order': order})
