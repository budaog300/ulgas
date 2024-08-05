import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

"""--------------------------Хранение данных подтверждения--------------------"""


class ConfirmationData(models.Model):
    """ Таблица Подтверждение данных """
    user_id = models.IntegerField()
    partner_id = models.IntegerField()
    agreement_id = models.IntegerField()
    objects_ids = models.JSONField()
    point_ids = models.JSONField()
    device_ids = models.JSONField()
    transformator_ids = models.JSONField()
    email = models.EmailField()
    confirmation_code = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Данные для подтверждения'
        verbose_name_plural = 'Данные для подтверждения'


""" -------------------------Пользовательские таблицы------------------------- """


class CustomUser(AbstractUser):
    """ Таблица Пользователь """
    first_name = 'None'
    last_name = 'None'
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    confirmation = models.CharField(max_length=255, default=uuid.uuid4)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


class UserPartner(models.Model):
    ''' Таблица КонтрАгент Пользователя '''
    id = models.AutoField(primary_key=True)
    id_customUser = models.IntegerField()
    id_partner = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'КонтрАгент Пользователя'
        verbose_name_plural = 'КонтрАгент Пользователя'


class UserAgreement(models.Model):
    ''' Таблица Договор пользователя '''
    id = models.AutoField(primary_key=True)
    id_customUser = models.IntegerField()
    id_agreement = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Договор Пользователя'
        verbose_name_plural = 'Договор Пользователя'


class UserObject(models.Model):
    ''' Таблица Объект Учета Пользователя '''
    id = models.AutoField(primary_key=True)
    id_customUser = models.JSONField()
    id_object = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Объект пользователя'
        verbose_name_plural = 'Объект пользователя'


class UserPoint(models.Model):
    ''' Таблица Точка Учета Пользователя '''
    id = models.AutoField(primary_key=True)
    id_customUser = models.JSONField()
    id_point = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Точки Учета Пользователя'
        verbose_name_plural = 'Точки Учета Пользователя'


class UserDeviceAccount(models.Model):
    ''' Таблица Прибор Учета Пользователя '''
    id = models.AutoField(primary_key=True)
    id_customUser = models.JSONField()
    id_device = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Прибор Учета Пользователя'
        verbose_name_plural = 'Прибор Учета Пользователя'


class UserTransformator(models.Model):
    '''Таблица Трансформатор Пользователя'''
    id = models.AutoField(primary_key=True)
    id_customUser = models.JSONField()
    id_transform = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Дополнительное оборудование Пользователя'
        verbose_name_plural = 'Дополнительное оборудование Пользователя'


""" -------------------------------------------------------------------------- """


# Логирование данных
class UserActionLogger(models.Model):
    ''' Таблица логирование данных '''
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_timestamp = timezone.localtime(self.timestamp).strftime("%d.%m.%y %H:%M")
        return f'{self.username} - {self.email} - {self.action} - {formatted_timestamp}'

    class Meta:
        verbose_name = 'Журнал действий'
        verbose_name_plural = 'Журнал действий'


""" -------------------------Статические таблицы------------------------- """


class Partner(models.Model):
    """ Таблица КонтрАгент """
    id = models.AutoField(primary_key=True)
    id_Ulges = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    type_partner = models.CharField(max_length=255)
    inn = models.CharField(max_length=255, null=True)
    kpp = models.CharField(max_length=255, null=True)
    legal_address = models.CharField(max_length=255, null=True)
    mail_address = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return (f'{self.id}, {self.id_Ulges} {self.name}, {self.type_partner}, {str(self.inn)}, '
                f'{str(self.kpp)}, {self.legal_address}, {self.mail_address}, {self.email}')

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагент'


class Agreement(models.Model):
    """ Таблица Договор """
    id = models.AutoField(primary_key=True)
    id_Ulges = models.CharField(max_length=255, null=True)
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE)
    number_agreement = models.CharField(max_length=255, null=True)
    idDogovor = models.CharField(max_length=255, null=True)
    conclusion_date = models.CharField(max_length=255, null=True)
    terminate_date = models.CharField(max_length=255, null=True)
    type_agreement = models.CharField(max_length=255, null=True)

    def __str__(self):
        return (f'{self.id}, {self.id_Ulges}, {self.partner_id}, {self.number_agreement},'
                f'{self.conclusion_date},{self.terminate_date}, {self.type_agreement}')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договор'


class ObjectAccount(models.Model):
    ''' Таблица Объект '''
    id = models.AutoField(primary_key=True)
    agreement_id = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    id_Ulges = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    object_type = models.CharField(max_length=255, null=True)
    is_active = models.CharField(max_length=10, null=True)

    def __str__(self):
        return (f'{self.id},{self.agreement_id},'
                f'{self.address},{self.object_type},{self.is_active}')

    class Meta:
        verbose_name = 'Объект Учета'
        verbose_name_plural = 'Объект Учета'


class AccountPoint(models.Model):
    ''' Таблица ТочкаУчета '''
    id = models.AutoField(primary_key=True)
    id_Ulges = models.CharField(max_length=255)
    id_object_account = models.ForeignKey(ObjectAccount, on_delete=models.CASCADE)
    conclusion_date = models.CharField(max_length=255, null=True)
    terminate_date = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)

    def __str__(self):
        return (f'{self.id}, {self.id_object_account}, {self.conclusion_date},'
                f'{self.terminate_date}, {self.comment}, {self.name}, {self.location}')

    class Meta:
        verbose_name = 'Точка Учета'
        verbose_name_plural = 'Точка Учета'


class DeviceAccount(models.Model):
    ''' Таблица Прибор Учета '''
    id = models.AutoField(primary_key=True)
    id_object_account = models.ForeignKey(AccountPoint, on_delete=models.CASCADE)
    id_Ulges = models.CharField(max_length=255)
    model_id = models.CharField(max_length=255, null=True)
    factory_number = models.CharField(max_length=255)
    digit = models.CharField(max_length=30, null=True)  # Разрядность
    phase = models.CharField(max_length=100, null=True)  # Фазность
    voltage = models.CharField(max_length=100, null=True)  # Напряжение
    tr_k = models.CharField(max_length=20, null=True)  # Коэф. трансформации
    meter_interval = models.CharField(max_length=20, null=True)  # Интервал поверки
    gos_install_date = models.CharField(max_length=30, null=True)
    production_date = models.CharField(max_length=255, null=True)
    DateEnd = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (f'{self.id}, {self.id_object_account}, {self.model_id}, '
                f'{self.factory_number}, {self.digit}, '
                f'{self.phase},{self.voltage},{self.tr_k},{self.meter_interval}, {self.gos_install_date}, {self.production_date}')

    class Meta:
        verbose_name = 'Прибор Учета'
        verbose_name_plural = 'Прибор Учета'


class TransformDevice(models.Model):
    '''Таблица Трансформатор'''
    id = models.AutoField(primary_key=True)
    id_device = models.ForeignKey(DeviceAccount, on_delete=models.CASCADE)
    Trans = models.CharField(max_length=50, null=True)
    TransPrimary = models.IntegerField(null=True)
    TransSecondary = models.IntegerField(null=True)
    TransType = models.CharField(max_length=100, null=True)
    TransPrecision = models.FloatField(null=True)
    TransInterval = models.IntegerField(null=True)

    def __str__(self):
        return (
            f'{self.id}, {self.Trans}, {self.TransPrimary}, {self.TransSecondary}, '
            f'{self.TransType}, {self.TransPrecision}, {self.TransInterval}')

    class Meta:
        verbose_name = 'Трансформатор'
        verbose_name_plural = 'Трансформатор'


""" --------------------------------------------------------------------- """


# Журнал#
class MeterReadings(models.Model):
    id_readings = models.AutoField(primary_key=True)
    NumberMeter = models.CharField(max_length=100, null=True),
    DateAct = models.CharField(max_length=100, null=True),
    Zone = models.CharField(max_length=100, null=True),
    CurrValue = models.CharField(max_length=100, null=True),
    DocType = models.CharField(max_length=100, null=True),

    def __str__(self):
        return (
            f'{self.id_readings}, {self.NumberMeter}, {self.DateAct}, {self.Zone}, {self.CurrValue}, {self.DocType}'
        )

    class Meta:
        verbose_name = "Показания"
        verbose_name_plural = "Показания"


# Уведомления#
class UserNote(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    message = models.CharField(max_length=255)

    def __str__(self):
        return (
            f'{self.id}, {self.user_id}, {self.message}'
        )

    class Meta:
        verbose_name = "Уведомления"
        verbose_name_plural = "Уведомления пользователя"


# Обращения#
class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    fb_name = models.CharField(max_length=255)
    fb_user_name = models.CharField(max_length=255)
    fb_phone_user = models.CharField(max_length=255)
    fb_email_user = models.CharField(max_length=255)
    fb_message = models.CharField(max_length=255)
    fb_dateTime = models.CharField(max_length=30)

    def __str__(self):
        return (
            f'{self.id}, {self.fb_name}, {self.fb_user_name}, {self.fb_phone_user}, {self.fb_email_user}, '
            f'{self.fb_message}, {self.fb_dateTime}'
        )

    class Meta:
        verbose_name = "Обращения"
        verbose_name_plural = "Обращения пользователей"


# Документы#
class DocumentUser(models.Model):
    id = models.AutoField(primary_key=True)
    dc_email_admin = models.CharField(max_length=255)
    dc_dateTime = models.CharField(max_length=255)
    dc_username = models.CharField(max_length=255)
    dc_user_agreement = models.CharField(max_length=255)
    dc_filename = models.CharField(max_length=255)
    dc_filepath = models.CharField(max_length=255)

    def __str__(self):
        return (
            f'{self.id}, {self.dc_email_admin}, {self.dc_dateTime},{self.dc_username},{self.dc_user_agreement},'
            f'{self.dc_filename}, {self.dc_filepath}'
        )

    class Meta:
        verbose_name = "Документы"
        verbose_name_plural = "Документы пользователя"
