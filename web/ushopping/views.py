import random
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from ushopping.forms import SellerCreateProductForm
from ushopping.models import Product, Category, Cart


class MyListingsProductList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "ushopping/my_listings.html"
    model = Product
    paginate_by = 10
    permission_denied_message = "You must authenticate first!"


    def test_func(self):
        if self.request.user.is_staff:
            return 1  # Accept

        if self.request.user.groups.filter(name='seller').exists():  # If user is part of seller group
            return 1  # Accept

        return self.handle_no_permission()  # Reject others

    def get_context_data(self, **kwargs):
        context = super(MyListingsProductList, self).get_context_data(**kwargs)
        context['myprod'] = self.request.user.products.all()
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super(MyListingsProductList, self).handle_no_permission()


class CreateProduct(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "ushopping/CreateProduct.html"
    model = Product
    form_class = SellerCreateProductForm
    success_url = reverse_lazy('uprofile:profile')

    def test_func(self):
        if self.request.user.is_staff:
            return 1  # Accept

        if self.request.user.groups.filter(name='seller').exists():  # If user is part of seller group
            return 1  # Accept

        return self.handle_no_permission()  # Reject others

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'You successfully submitted your application form.')
        return super().form_valid(form)  # If the form is valid, redirect to the success_url

    permission_denied_message = "Please check your application form!"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class BrowseProducts(ListView):
    template_name = "ushopping/browse.html"
    model = Product
    paginate_by = 8

    def get_queryset(self):
        object_list = super().get_queryset()

        if self.request.GET.get('cfilter'):
            object_list = Product.objects.filter(Q(category__name=self.request.GET.get('cfilter')))

        if self.request.GET.get('as'):

            object_list = Product.objects.filter(
                Q(name__icontains=self.request.GET.get('as')) |
                Q(author__icontains=self.request.GET.get('as')) |
                Q(publisher__icontains=self.request.GET.get('as')) |
                Q(year__icontains=self.request.GET.get('as')) |
                Q(description__icontains=self.request.GET.get('as'))
            )

        return object_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Top 4 Recommended  / BESTSELLERS
        I = Cart.objects.values('item').annotate(total=Count('item')).order_by('-total')

        top4 = list()
        for x in I[:4]:
            top4.append(x['item'])

        top4_list_items = list()

        for x in top4:
            try:
                top4_list_items.append(Product.objects.get(id=x))
            except Exception:
                raise f"[Error]: Can't add item {x} to the top4_list_items. "

        context['top4_list_items'] = top4_list_items

        # User Specific Recommendation System

        if self.request.user.is_authenticated:

            if self.request.user.userto.values('item__category').exists(): # Check if user has any product in his cart

                CategoryOfInterest = self.request.user.userto.values('item__category').first()['item__category']

                if CategoryOfInterest:
                    count = len(list(Product.objects.filter(category_id=CategoryOfInterest).all()))
                    context['UserRecommendation'] = random.sample(list(Product.objects.filter(category_id=CategoryOfInterest).all()), count)

        return context



class ProductDetails(DetailView):
    template_name = "ushopping/product_details.html"
    model = Product

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'add' in self.request.GET:
                try:
                    cart = Cart.objects.get(user=self.request.user, item=self.kwargs['pk'])
                    cart.amount += 1
                    cart.save()
                    messages.success(self.request, f"Your cart has been updated! Current amount = {cart.amount} ")
                except Cart.DoesNotExist:
                    Cart.objects.create(user=self.request.user, amount=1,
                                        item=Product.objects.get(id=self.kwargs['pk']))
                    messages.success(self.request, f"You successfully added  {Product.objects.get(id=self.kwargs['pk']).name}! Check your Cart.")

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Cart
    template_name = 'ushopping/cart_delete.html'
    success_url = reverse_lazy('ushopping:my-cart-view')

    def test_func(self):
        if self.request.user.userto.filter(id=self.kwargs['pk'], user=self.request.user).exists(): # If User has that product
            return 1  # Accept

        return self.handle_no_permission()  # Reject others




class MyCartView(LoginRequiredMixin, ListView):
    template_name = "ushopping/cart.html"
    model = Cart
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mycart'] = self.request.user.userto.all()
        return context


class EditProduct(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "ushopping/EditProduct.html"
    model = Product
    success_url = reverse_lazy('uprofile:profile')

    fields = [
        'name',
        'publisher',
        'year',
        'condition',
        'author',
        'category',
        'short_description',
        'description',
        'product_image',
        'price',
    ]

    def test_func(self):
        if self.request.user.is_staff:
            return 1  # Accept

        if self.request.user.groups.filter(name='seller').exists():  # If user is part of seller group
            if self.request.user.products.filter(id=self.kwargs['pk']).exists(): # If product is related to user
                return 1  # Accept

        return self.handle_no_permission()  # Reject others

    def form_valid(self, form):
        messages.success(self.request, f'You successfully updated {form.instance.name} product information!')
        return super().form_valid(form)  # If the form is valid, redirect to the success_url


    def handle_no_permission(self):
        messages.error(self.request, "No permission!")
        return super().handle_no_permission()




