from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns=[
    path('',views.home.as_view(),name='home'),
    path('product_about/<slug>/',views.product_about.as_view(),name='product_about'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name="logout"),
    path('register/',views.register1,name='register1'),
    path('cart/', views.cart.as_view(), name='cart'),
    path('myorder/', views.myorder.as_view(), name='myorder'),
    # path('buynow/<slug>/', views.buynow, name='buynow'),

    path('checkout/', views.CheckoutView.as_view(), name='CheckoutView'),

    path('add_to_cart/<slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),

  

    path('search/',views.search,name='search'),
    path('profile/',views.profile,name='profile'),

        # -------------------Forgot Password--------------------------------------

        path(
                'change-password/',
                auth_views.PasswordChangeView.as_view(
                    template_name='password-reset/change-password.html',
                    success_url = '/'
                ),
                name='change_password'
            ),


    # -------------------Forgot Password--------------------------------------
    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset/password_reset.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)