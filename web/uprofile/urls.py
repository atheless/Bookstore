from django.urls import path

from uprofile.views import ProfileView, SellerApplyView, ProfileEditView, SellersApplicationFormsListView, \
    SellersApplicationFormsDetailView, UpdatePassword, SearchSellerView, SellerDetailView, CreateNewCategoryProduct

app_name = 'uprofile'

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/new_seller', SellerApplyView.as_view(), name='seller-apply'),
    path('edit_profile', ProfileEditView.as_view(), name='profile-edit'),
    path('update_password', UpdatePassword.as_view(), name='update-password'),
    path('sellers_application_forms/', SellersApplicationFormsListView.as_view(), name='sellers-app-forms'),
    path('sellers_app_details/<int:pk>', SellersApplicationFormsDetailView.as_view(), name='sellers-app-details'),
    path('search_seller/', SearchSellerView.as_view(), name='search_seller'),
    path('seller_details/<int:pk>', SellerDetailView.as_view(), name='seller-details'),
    path('CreateNewCategory', CreateNewCategoryProduct.as_view(), name='create-new-category'),

]