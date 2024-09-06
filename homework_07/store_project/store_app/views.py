from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from django.views.generic import (
    TemplateView, 
    CreateView, 
    ListView,
    DetailView,
    UpdateView,
)
from store_app.models import Product, Order
from celery.result import AsyncResult 
from .forms import CategoryCreateUpdateForm
from .models import Category, OrderProduct
from .mixins import PageTitleMixin


class ProductsIndexView(TemplateView):
    template_name="store_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            products=(
                Product.objects
                .filter(archived=False)
                .select_related("category")
                .all()
        ),
            )
        return context
    

class OrdersIndexView(TemplateView):
    template_name = "store_app/orders_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            # orders=Order.objects.prefetch_related("products").all(),
            orders=(
                Order.objects
                .select_related("user")
                .prefetch_related("order_products__product")
                .all()
            ),
        )
        return context
    

def task_status(request: HttpRequest) -> HttpResponse:
    context = {}
    task_id = request.GET.get("task_id")
    # result = AsyncResult(id=task_id) 
    # is_ready = result.ready()
    # status = result.status
    # task_result = result.result
    context.update(
        task_id=task_id,
        is_ready="is_ready",
        status="status",
        result="task_result",
    )
    return render(
        request=request,
        template_name="store_app/task_status.html",
        context=context,
    ) 


def create_category(request):
    if request.method == 'POST':
        print('processing')
    
        form = CategoryCreateUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            print('is valid')
            form.save()
            return HttpResponseRedirect('/')
        else:
            print('errors')
    else:
        form = CategoryCreateUpdateForm()            
    context = {
        'create_form': form,
    }
    return render(request, 'store_app/create_category.html', context)


class CreateCategory(PageTitleMixin, CreateView):
    model = Category
    form_class = CategoryCreateUpdateForm
    success_url = '/'
    page_title = 'Category create'
   
    
class ListCategory(PermissionRequiredMixin, PageTitleMixin, ListView):
    model = Category
    page_title = 'List category'
    paginate_by = 10
    permission_required = 'store_app.view_category'
    


class UpdateCategory(PageTitleMixin, UpdateView):
        model = Category
        form_class = CategoryCreateUpdateForm
        page_title = 'Category update'
        success_url = '/'
       


class ReadCategory(PageTitleMixin, DetailView):
        model = Category
        page_title = 'Category update'
                      

class ProductDetailView(DetailView):
    model = Product
    page_title = 'product'
    

    def get_object(self, queryset=None):
        # Используем id из URL для получения объекта
        return get_object_or_404(Product, id=self.kwargs['id'])
    

# КОРЗИНА
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        order, created = Order.objects.get_or_create(user=request.user, comment="Корзина", defaults={'adress': ''})
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product, defaults={'quantity': 0, 'price': product.price})
        
        order_product.quantity += quantity
        order_product.price = product.price
        order_product.save()

        # Подсчет общего количества товаров в корзине
        total_quantity = sum(item.quantity for item in order.order_products.all())

        return JsonResponse({'cart_item_count': total_quantity})

class CartView(LoginRequiredMixin, TemplateView):
    template_name = "store_app/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, user=self.request.user, comment="Корзина")
        context['order'] = order
        
        # Подсчет общего количества товаров в корзине
        total_quantity = sum(item.quantity for item in order.order_products.all())
        context['total_quantity'] = total_quantity
        
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        order = get_object_or_404(Order, user=request.user, comment="Корзина")
        order_product = get_object_or_404(OrderProduct, id=item_id, order=order)
        
        # Удаляем товар из корзины
        order_product.delete()
        
        return redirect('store_app:cart_view')  # Перенаправление на страницу корзины  


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        address = request.POST.get('address')
        
        # Получаем товары из запроса (например, из формы или JSON)
        products = request.POST.getlist('product_ids')  # Список ID продуктов
        quantities = request.POST.getlist('quantities')  # Список количеств

        # Создаем новый заказ
        new_order = Order.objects.create(user=request.user, adress=address, comment="Заказ оформлен")

        # Переносим товары в новый заказ
        for product_id, quantity in zip(products, quantities):
            product = get_object_or_404(Product, id=product_id)
            OrderProduct.objects.create(
                order=new_order,
                product=product,
                quantity=int(quantity),  # Преобразуем в целое число
                price=product.price
            )

        # Удаляем товары из корзины, если они были
        # Убедитесь, что у вас есть логика для удаления товаров из корзины, если это необходимо
        # Например, если у вас есть Order с comment="Корзина", вы можете удалить его
        try:
            order = Order.objects.get(user=request.user, comment="Корзина")
            order.order_products.all().delete()  # Удаляем все товары из корзины
            order.delete()  # Удаляем саму корзину
        except Order.DoesNotExist:
            pass  # Корзина не найдена, ничего не делаем

        # Перенаправление на главную страницу или страницу подтверждения
        return redirect('/')
             