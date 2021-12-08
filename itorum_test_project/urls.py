"""itorum_test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import OrderView, order_post, order_delete, index_page, export_order_by_json
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('order/', OrderView.as_view(), name='order'),
                  path('order_post/', order_post, name='order_post'),
                  path('delete_order/<int:pk>/', order_delete, name='order_delete'),
                  path('', index_page),
                  path('export/', export_order_by_json),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)