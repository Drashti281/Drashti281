from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.HOME, name='home'),
                  path('base/', views.BASE, name='base'),
                  path('products/', views.PRODUCT, name='products'),
                  path('products/<str:id>', views.PRODUCT_DETAIL_PAGE, name='product_detail'),

                  path('search/', views.SEARCH, name='search'),
                  path('contact/', views.Contact_Page, name='contact'),

                  path('register/', views.HandleRegister, name='register'),
                  path('login/', views.HandleLogin, name='login'),
                  path('logout/', views.HandleLogout, name='logout'),

                  # cart
                  path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
                  path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
                  path('cart/item_increment/<int:id>/',
                       views.item_increment, name='item_increment'),
                  path('cart/item_decrement/<int:id>/',
                       views.item_decrement, name='item_decrement'),
                  path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
                  path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
                  path('cart/checkout/', views.Check_out, name='checkout'),

                  path('cart/checkout/placeorder', views.PLACE_ORDER, name='place_order'),
                  path('success/', views.SUCCESS, name='success'),

                  path('Your_Order/', views.Your_Order, name='your_order'),
                  path('about/', views.ABOUT, name='about'),
                  path('blog-grid/', views.Blog_Grid, name='blog-grid'),
                  path('blog-grid-left-sidebar/', views.Blog_Grid_Left_Sidebar, name='blog-grid-left-sidebar'),
                  path('blog-grid-right-sidebar/', views.Blog_Grid_Right_Sidebar, name='blog-grid-right-sidebar'),
                  path('blog-list/', views.Blog_List, name='blog-list'),
                  path('blog-list-left-sidebar/', views.Blog_List_Left_Sidebar, name='blog-list-left-sidebar'),
                  path('blog-list-right-sidebar/', views.Blog_List_Right_Sidebar, name='blog-list-right-sidebar'),
                  path('single-blog/', views.Single_Blog, name='single-blog'),
                  path('single-blog-left-sidebar/', views.Single_Blog_Left_Sidebar, name='single-blog-left-sidebar'),
                  path('single-blog-right-sidebar/', views.Single_Blog_Right_Sidebar, name='single-blog-right-sidebar'),
                  path('shop-3-column/', views.Shop_3_Column, name='shop-3-column'),
                  path('shop-4-column/', views.Shop_4_Column, name='shop-4-column'),
                  path('shop-right-sidebar/', views.Shop_Right_Sidebar, name='shop-right-sidebar'),
                  path('shop-left-sidebar/', views.Shop_Left_Sidebar, name='shop-left-sidebar'),
                  path('shop-list-left-sidebar/', views.Shop_List_Left_Sidebar, name='shop-list-left-sidebar'),
                  path('shop-list-right-sidebar/', views.Shop_List_Right_Sidebar, name='shop-list-right-sidebar'),
                  path('product-group/', views.Product_Group, name='product-group'),
                  path('product-tab-2/', views.Product_Tab_2, name='product-tab-2'),
                  path('product-tab-3/', views.Product_Tab_3, name='product-tab-3'),
                  path('product-slider/', views.Product_Slider, name='product-slider'),
                  path('product-account/', views.Product_Account, name='product-account'),
                  path('empty-product/', views.Empty_Product, name='empty-product'),
                  path('coming-soon-page/',views.Coming_Soon_Page, name='coming-soon-page'),
                  path('home-1/',views.Home_1, name='home-1'),
                  path('whishlist/',views.Whishlist,name='whishlist.html'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
