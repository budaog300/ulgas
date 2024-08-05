from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from . import views
from .forms import CustomPasswordRestForm

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('home/', views.base, name='home'),  # Главная страница после авторизации
    path('main/', views.main_button, name='main_button'),  # Кнопка Главная
    path('deposits/', views.deposits_button, name='deposits_button'),  # Кнопка начисления
    path('note/', views.note_button, name='note_button'),  # Кнопка уведомления
    path('appeals/', views.appeals_button, name='appeals_button'),  # Кнопка обращения
    path('document/', views.document_button, name='document_button'),  # Кнопка документы
    path('meter/', views.meter_button, name='meter_button'),  # Кнопка точки учета
    path('passport/', views.passport_button, name='passport_button'),  # Кнопка Паспорт ТУ
    path('logout/', views.logout_user, name='logout'),  # Выход из системы
    path('indicate_info/', views.indicate_button, name='indicate'),  # Показания
    path('payment_obj/', views.pay_obj, name='pay_obj'),  # Начисления по объекту
    path('activate/<uidb64>/', views.activate, name='activate'),  # Активация при регистрации

    path('get_desired_partner/', views.get_desired_partner_id, name='get_desired'),  # Блок с договорами в SideBar
    path('get_payment_info/', views.get_payment, name='get_payment'),  # Заполнение таблицы начисления
    path('get_point_info/', views.get_point, name='get_point'),  # Поиск ТУ и ПУ по объекту
    path('get_passport_info/', views.get_passport_info, name="passport_info"),  # Прогружаем информацию о Паспорте ТУ
    path('get_data_info/', views.get_data_meter, name='get_data_info'),  # Показания прогрузка
    path('get_object_payment/', views.get_object_payment, name='get_obj_pay'),  # Начисления по объекту
    path('add_contract/', views.add_contract, name='addcontract'),  # Добавить договор
    path('confirm/<str:confirmation_code>/', views.confirm_contract, name='confirm_contract'),
    # Информация для подтверждения
    path('appeal-done/', views.feedback_user, name='feedback'),  # Обращение форма
    path('get_history/', views.hisory_message, name='history_message'),  # История обращений
    path('get_accordion_passport/', views.passport_accordion, name='passport_accordion'),  # Подробности паспорт

    # Сброс пароля
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="avtoriz/password_reset_form.html",
             email_template_name="avtoriz/password_reset_email.html",
             success_url=reverse_lazy("password_reset_done"),
             form_class=CustomPasswordRestForm
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="avtoriz/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="avtoriz/password_reset_confirm.html",
             success_url=reverse_lazy("password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="avtoriz/password_reset_complete.html"),
         name='password_reset_complete'),
]
