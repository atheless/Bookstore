from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from uprofile.forms import SellerApplyForm, UserEditForm, UProfileEditForm, form_validation_error
from uprofile.models import Seller, UProfile
from ushopping.models import Category


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class SellersApplicationFormsListView(StaffRequiredMixin, ListView):
    model = Seller
    template_name = 'uprofile/sellers_applications.html'
    context_object_name = "af_list"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        object_list = super().get_queryset()
        query = self.request.GET.get("search")
        if query:  # Is a query
            return Seller.objects.filter(
            Q(created_by__username=query) | Q(seller_name__icontains=query) | Q(country__icontains=query) | Q(seller_email__icontains=query) | Q(contact_phone__icontains=query)
        )
        return object_list


    def get_context_data(self, **kwargs):
        context = super(SellersApplicationFormsListView, self).get_context_data(**kwargs)
        context['count0'] = self.get_queryset().filter(status='0').count()
        context['count1'] = self.get_queryset().filter(status='1').count()
        context['count2'] = self.get_queryset().filter(status='2').count()
        context['count3'] = self.get_queryset().filter(status='3').count()
        context['count4'] = self.get_queryset().filter(status='4').count()
        return context


class SellersApplicationFormsDetailView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Seller
    template_name = 'uprofile/sellers_app_details.html'
    success_url = reverse_lazy('uprofile:sellers-app-forms')

    fields = [
        'seller_name',
        'legal_seller_address',
        'country',
        'contact_phone',
        'seller_email',
        'description',
        'status',
    ]

    def form_valid(self, form):
        # 'created_by' refers to user in User Django model.
        if form.instance.status == '0':  # If in form selected normal
            Group.objects.get_or_create(name='normal')
            form.instance.created_by.groups.set(Group.objects.filter(name='normal'))

        if form.instance.status == '1':  # If in form selected approved then add change user group to seller
            Group.objects.get_or_create(name='seller')
            form.instance.created_by.groups.set(Group.objects.filter(name='seller'))

        if form.instance.status == '2':  # If in form selected rejected
            Group.objects.get_or_create(name='normal')
            form.instance.created_by.groups.set(Group.objects.filter(name='normal'))

        if form.instance.status == '3':  # If in form selected undefined
            Group.objects.get_or_create(name='normal')
            form.instance.created_by.groups.set(Group.objects.filter(name='normal'))

        form.instance.approved_by = self.request.user
        return super().form_valid(form)

    permission_denied_message = "You must authenticate first!"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "uprofile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["obj"] = get_object_or_404(User, id=self.request.user.id)

        if Group.objects.filter(user=self.request.user).exists():
            # User did use MyUserCreationForm or is in a group
            context["group"] = Group.objects.filter(user=self.request.user).first().name.capitalize()
        else:
            # User didn't use MyUserCreationForm
            if self.request.user.is_staff:
                context["group"] = 'Staff'
            else:
                context["group"] = 'Undefined'

        # Check if user has UProfile
        if UProfile.objects.filter(user=self.request.user.id).exists():
            context["uprofile"] = get_object_or_404(UProfile, user=self.request.user)
        else:
            context["uprofile"] = False

        if Seller.objects.filter(created_by=self.request.user.id).exists():
            # User has applied to become a seller or already approved seller. I can obtain an object for a template.
            context["seller"] = get_object_or_404(Seller, created_by=self.request.user)
        else:
            # User is normal and did not apply yet to become a seller.
            context["seller"] = False

        return context


class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('uprofile:profile')
    template_name = 'uprofile/update_password.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'uprofile/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('uprofile:profile')

    def get(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        second_form = UProfileEditForm(request.POST, request.FILES, instance=request.user.uprofile)
        return render(request, self.template_name, {'user_form': form, 'profile_form': second_form})

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        second_form = UProfileEditForm(request.POST, request.FILES, instance=request.user.uprofile)
        if form.is_valid() and second_form.is_valid():
            form.save()
            second_form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, form_validation_error(form))
            messages.error(request, form_validation_error(second_form))
        return render(request, self.template_name, {'user_form': form, 'profile_form': second_form})

    permission_denied_message = "You must authenticate first!"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class SellerApplyView(LoginRequiredMixin, CreateView):
    template_name = "uprofile/seller_apply.html"
    model = Seller
    form_class = SellerApplyForm
    success_url = reverse_lazy('uprofile:profile')
    permission_denied_message = "You must authenticate first!"
    seller = None

    def form_valid(self, form):
        self.seller = form.save(commit=False)
        self.seller.created_by = self.request.user
        messages.success(self.request, 'You successfully submitted your application form.')
        return super().form_valid(form)  # If the form is valid, redirect to the success_url

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(SellerApplyView, self).handle_no_permission()


class SearchSellerView(ListView):
    model = Seller
    template_name = "uprofile/search_sellers.html"
    paginate_by = 10

    def get_queryset(self):
        object_list = Seller.objects.filter(status=1)
        query = self.request.GET.get("q")
        if query:  # Is a query
            return Seller.objects.filter(
            Q(seller_name__icontains=query) | Q(country__icontains=query) | Q(seller_email__icontains=query) | Q(contact_phone__icontains=query) ,
            Q(status__exact='1')
        )
        return object_list



class SellerDetailView(DetailView):
    model = Seller
    template_name = "uprofile/seller_details.html"

class CreateNewCategoryProduct(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "ushopping/CreateProduct.html"
    model = Category
    success_url = reverse_lazy('uprofile:profile')

    fields = [
        'name',
    ]

    def form_valid(self, form):
        messages.success(self.request, 'You successfully created new category for products.')
        return super().form_valid(form)  # If the form is valid, redirect to the success_url

    permission_denied_message = "No permissions!"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()