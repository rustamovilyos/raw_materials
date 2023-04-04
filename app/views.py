from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderProduct
from django.views.generic import ListView, DetailView
from django.db import IntegrityError, transaction


# функция обрабатывает GET-запросы на главную страницу сайта и возвращает HTML-страницу index.html.
def index(request):
    return render(request, 'app/index.html')


# запрашивает все объекты (товары) модели Product из базы данных, и передает их в контекст шаблона app/index.html,
# чтобы их можно было отобразить на странице
def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/product_list.html', context)


# Эта функция возвращает список всех заказов и их продуктов на страницу orders_list.html
# с помощью шаблона Django и контекста, содержащего orders_list и order_product_list.
def order_list(request):
    orders_list = Order.objects.all()
    order_product_list = OrderProduct.objects.all()
    return render(request, 'app/orders_list.html',
                  {'orders_list': orders_list, 'order_product_list': order_product_list})


# ProductView является классом-наследником DetailView, который используется для отображения детальной информации
# о конкретном продукте из базы данных на отдельной странице. Шаблон для отображения этой информации
# указан в template_name, а model указывает на соответствующую модель Django.
class ProductView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'


def create_order(request):
    if request.method == 'POST':
        # получить данные формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        products = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        try:
            with transaction.atomic():
                # создать экземпляр заказа
                order = Order.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address
                )

                for i, product_id in enumerate(products):
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantities[i])

                    # проверка, достаточно ли товара на складе
                    print('product.quantity', product.quantity, ' - quantity', product.quantity)
                    if product.quantity < quantity:
                        raise ValueError(f"Not enough {product.name} in stock")

                    # создать экземпляр OrderProduct
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity
                    )

            # перенаправление на страницу подтверждения заказа
            return redirect('app:order_confirmation', order_id=order.id)

        except:
            transaction.rollback()
            message = f"Недостаточно '{product.name}' на складе"
            products = Product.objects.all()
            context = {'products': products, 'message': message}
            return render(request, 'app/create_order.html', context)

    else:
        # получить все продукты
        products = Product.objects.all()

        context = {'products': products}
        return render(request, 'app/create_order.html', context)


# Эта функция возвращает страницу подтверждения заказа соответствующего указанному order_id.
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'app/order_confirmation.html', {'order': order})
