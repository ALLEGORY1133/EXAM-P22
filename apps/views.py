
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from apps.forms import UserRegisterModelForm
from apps.models import Product, Category
from apps.tasks import send_to_email


class ProductListView(ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class RegisterCreateView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = UserRegisterModelForm
    success_url = reverse_lazy('product_list_page')

    def form_valid(self, form):
        form.save()
        # send_to_email('Your account has been created!', form.data['email'])
        send_to_email.delay('Your account has been created!', form.data['email'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SettingsUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = 'first_name', 'last_name'
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


# class CustomLoginView(LoginView):
#     template_name = 'apps/auth/login.html'
#     redirect_authenticated_user = True
#     next_page = reverse_lazy('product_list_page')


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('product_list_page')


class CustomLoginView(LoginView):
    template_name = 'apps/auth/login.html'
    next_page = reverse_lazy('product_list_page')
    redirect_authenticated_user = True


class CustomLogoutView(View):
    template_name = 'apps/auth/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('product_list_page')


class CustomRegister(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = UserRegisterModelForm
    success_url = reverse_lazy('product_list_page')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        send_to_email.delay('Your account has been created!', form.cleaned_data['email'])
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CustomSettings(LoginRequiredMixin,UpdateView):
    queryset = User.objects.all()
    fields = 'first_name', 'last_name'
    template_name = 'apps/auth/settings.html'
    success_url = reverse_lazy('settings_page')

    def get_object(self, queryset=None):
        return self.request.user
