from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Product
from store.models.orders import Order
from store.models.customer import Customer

class CheckOut(View):

    # Метод GET — для редиректа на корзину при прямом переходе
    def get(self, request):
        return redirect('cart')  # перенаправляем на корзину

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Получаем ID пользователя из сессии
        customer = request.session.get('customer')
        if not customer:
            # Если пользователь не залогинен, редирект на login с возвратом на checkout
            return redirect('/login?return_url=/check-out')

        # Получаем товары из корзины
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        # Создаём заказ для каждого товара
        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()

        # Очищаем корзину
        request.session['cart'] = {}
        return redirect('cart')