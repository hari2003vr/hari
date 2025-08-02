"""
URL configuration for bag project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from material import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hi',views.show),
    path('home',views.index),
    path('jewellery',views.jewellery),
    path('fashion',views.fashion),
    path('electronic',views.electronic),
    path('register',views.reg),
    path('log',views.log),
    path('admin',views.admin),
    path('user_log',views.user_login),
    path('logout',views.log_out),
    path('add_product',views.add_product),
    path('manage_product',views.manage_product),
    path('dele/<int:c>',views.dele),
    path('update/<int:x>',views.update1),
    path('user_prooduct',views.user_prooduct),
    path('addcart/<int:d>',views.addcart),
    path('cartview',views.cartview),
    path('increment/<int:d>',views.increment),
    path('decrement/<int:d>',views.decrement),
    path('rem/<int:d>',views.rem),
    path('wish/<int:d>',views.addwish),
    path('wishview',views.wishview),
    path('reme/<int:d>',views.reme),
    path('payment/<int:id>',views.payment),
    path('success',views.order),
    path('myorder', views.myorder),
    path('adorder',views.adorder),
    path('alert', views.alert),
    path('forgot',views.forgot_password),
    path('reset_password/<token>',views.reset_password),
    path('booking_details',views.booking_details),
    path('about',views.about),
    path('display_details',views.display_details),
    path('update_status/<int:pk>',views.update_status)


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)