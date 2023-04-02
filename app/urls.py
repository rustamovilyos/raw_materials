from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from app.views import ProductView
app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.product_list, name='product_list'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('orders_list', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
