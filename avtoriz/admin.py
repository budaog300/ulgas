from django.contrib import admin

from avtoriz.models import (UserActionLogger,
                            Partner, Agreement, ObjectAccount, DeviceAccount, AccountPoint, TransformDevice, CustomUser,
                            UserPartner,
                            UserAgreement, UserObject, ConfirmationData, UserPoint, UserDeviceAccount,
                            UserTransformator, MeterReadings, UserNote, FeedBack, DocumentUser)


# Данные для подтверждения
class CustomConfirmationData(admin.ModelAdmin):
    list_display = (
        'user_id', 'partner_id', 'agreement_id', 'objects_ids', 'point_ids', 'transformator_ids', 'email',
        'confirmation_code')


# Кастомный Юзер
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'confirmation', 'status',
                    'deleted', 'is_active', 'is_staff')


# КонтрАгентПользователя
class UserPartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_partner', 'is_approved', 'status', 'deleted')


# ДоговорПользователя
class UserAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_agreement', 'is_approved', 'status', 'deleted')


# Объект Пользователя
class UserObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_object', 'status', 'deleted')


# Точка учета пользователя
class UserPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_point', 'status', 'deleted')


# Прибор Учета пользователя
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_device', 'status', 'deleted')


# Доп. Оборудование Юзера
class UserDopTransform(admin.ModelAdmin):
    list_display = ('id', 'id_customUser', 'id_transform', 'status', 'deleted')


# КонтрАгент
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_Ulges', 'name', 'type_partner', 'inn',
                    'kpp', 'legal_address', 'mail_address', 'email')


# Договор
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_Ulges', 'partner_id', 'number_agreement', 'conclusion_date',
                    'terminate_date', 'type_agreement', 'idDogovor')


# Объект Учета
class ObjectAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'agreement_id', 'address', 'object_type', 'is_active')


# Точка Учета
class AccountPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_object_account', 'conclusion_date',
                    'terminate_date', 'comment', 'name', 'location')


# ПриборУчета
class DeviceAccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'id_object_account', 'model_id', 'factory_number',
        'digit', 'phase', 'voltage', 'tr_k', 'meter_interval', 'gos_install_date', 'production_date', 'DateEnd')


# ДопОборудование
class TransFormAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'id_device', 'Trans', 'TransPrimary', 'TransSecondary', 'TransType', 'TransPrecision', 'TransInterval')


class MeterReadingsAdmin(admin.ModelAdmin):
    list_display = ('id_readings', 'NumberMeter', 'DateAct', 'Zone', 'CurrValue', 'DocType')


class NoteUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'message')


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'fb_name', 'fb_user_name', 'fb_phone_user', 'fb_email_user', 'fb_message', 'fb_dateTime')


class DocumentUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'dc_email_admin', 'dc_dateTime', 'dc_username', 'dc_user_agreement', 'dc_filename', 'dc_filepath')


# Регистрация моделей
admin.site.register(UserActionLogger)  # Логирование
admin.site.register(UserNote, NoteUserAdmin)  # Уведомления
admin.site.register(FeedBack, FeedBackAdmin)  # Обращения
admin.site.register(DocumentUser, DocumentUserAdmin)  # Документы

admin.site.register(Partner, PartnerAdmin)  # КонтрАгент
admin.site.register(Agreement, AgreementAdmin)  # Договор
admin.site.register(ObjectAccount, ObjectAccountAdmin)  # Объект учета
admin.site.register(AccountPoint, AccountPointAdmin)  # Точка учета
admin.site.register(DeviceAccount, DeviceAccountAdmin)  # Прибора учета
admin.site.register(TransformDevice, TransFormAdmin)  # Трансофрматор

admin.site.register(MeterReadings, MeterReadingsAdmin)  # Журнал показаний

admin.site.register(CustomUser, CustomUserAdmin)  # Пользователь

admin.site.register(UserPartner, UserPartnerAdmin)  # КонтрАгент Пользователя
admin.site.register(UserAgreement, UserAgreementAdmin)  # Договор Пользователя
admin.site.register(UserObject, UserObjectAdmin)  # Объект Пользователя
admin.site.register(UserPoint, UserPointAdmin)  # Точки учета Пользователя
admin.site.register(UserDeviceAccount, UserDeviceAdmin)  # Прибор Учета Пользователя
admin.site.register(UserTransformator, UserDopTransform)  # Доп. оборудование пользователя

admin.site.register(ConfirmationData,
                    CustomConfirmationData)  # Промежуточная таблица для хранения данных для подтверждения
