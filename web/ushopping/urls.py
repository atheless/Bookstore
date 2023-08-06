from django.urls import path

from ushopping.views import CreateProduct, MyListingsProductList, BrowseProducts, ProductDetails, MyCartView, \
    EditProduct, CartDeleteView

app_name = 'ushopping'

urlpatterns = [
    path('create_product', CreateProduct.as_view(), name='create-product'),
    path('my_listings', MyListingsProductList.as_view(), name='my-listings-product'),
    path('Browse', BrowseProducts.as_view(), name='browse-products'),
    path('ProductDetails/<int:pk>', ProductDetails.as_view(), name='product-details'),
    path('mycart', MyCartView.as_view(), name='my-cart-view'),
    path('mycart_delete/<int:pk>', CartDeleteView.as_view(), name='cart-delete-view'),
    path('edit_product/<int:pk>', EditProduct.as_view(), name='edit-product'),


]