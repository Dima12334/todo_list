from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .models import Todo
from .forms import TodoForm, AuthUserForm, RegisterUserForm


def show_calendar(request):      #<img src='{% static "todo_app/img/calendar.png"%}' width = "25px" height="25">
    return render(request, 'todo_app/calendar.html')


class HomeListView(ListView):   #<img src='{% static "todo_app/img/main.png"%}' width = "25px" height="25">
    model = Todo
    template_name = 'todo_app/all_days.html'
    context_object_name = 'todo'


class DetailPageView(DetailView):
    model = Todo
    template_name = 'todo_app/one_day.html'
    context_object_name = 'example'


class CustomSuccessMessageMixin:

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class TodoCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Todo
    template_name = 'todo_app/edit_page.html'
    form_class = TodoForm
    success_url = reverse_lazy('edit-page')
    success_msg = 'Заметка создана'

    def get_context_data(self, **kwargs):
        kwargs['example'] = Todo.objects.all().order_by('id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Todo
    template_name = 'todo_app/edit_page.html'
    form_class = TodoForm
    success_url = reverse_lazy('edit-page')
    success_msg = 'Заметка обновлена'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class MyprojectLoginView(LoginView):
    template_name = 'todo_app/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit-page')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = Todo
    template_name = 'todo_app/register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('edit-page')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class MyprojectLogOut(LogoutView):
    next_page = reverse_lazy('edit-page')


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo_app/edit_page.html'
    success_url = reverse_lazy('edit-page')
    success_msg = 'Заметка удалена'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):  #не працює
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
