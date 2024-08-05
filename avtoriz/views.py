import datetime
import time
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from .db_settings import ulgesbdexecute, ulgesdbMeterReadings, ulgesdbAbnSchet, ulgesdbObjectPayment
from .forms import AuthenticationForm, RegistrationForm, ContractForm
from .models import (UserActionLogger, CustomUser,
                     Partner, Agreement, UserAgreement,
                     UserPartner, UserObject, ObjectAccount, ConfirmationData, UserPoint, AccountPoint, DeviceAccount,
                     UserDeviceAccount, TransformDevice, UserTransformator, UserNote, FeedBack)


def base(request):
    """ Главная страница после авторизации """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/base.html')
    else:
        return redirect('index')


def main_button(request):
    """ Кнопка Главная """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/main_panel.html')
    else:
        return redirect('index')


def deposits_button(request):
    """ Кнопка начисления """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/user_deposits.html')
    else:
        return redirect('index')


def note_button(request):
    """ Кнопка уведомления """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/user_note.html')
    else:
        return redirect('index')


def appeals_button(request):
    """ Кнопка обращения """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/user_appeal.html')
    else:
        return redirect('index')


def document_button(request):
    """ Кнопка документы """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/user_document.html')
    else:
        return redirect('index')


def meter_button(request):
    """ Объекты учета """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/meter_point.html')
    else:
        return redirect('index')


def passport_button(request):
    """ Паспорт ТУ """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/passport_point.html')
    else:
        return redirect('index')


def feedback_user(request):
    """ Обработка обращения пользователя """
    dt_now = datetime.datetime.now()
    data = {
        "name": request.POST.get('name'),
        "user_name": str(request.POST.get('user_name')),
        "email": request.POST.get('email'),
        "phone": request.POST.get('phone_number'),
        "messageUser": request.POST.get('messageUser'),
        "dateTime": dt_now
    }
    print(data)
    FeedBack.objects.create(fb_name=data["name"], fb_user_name=data["user_name"], fb_phone_user=data["phone"],
                            fb_email_user=data["email"], fb_message=data["messageUser"], fb_dateTime=dt_now)
    send_mail(
        f'Обращение от пользователя {data["user_name"]} ID - {request.user.id}',
        f'Необходимо ответить на обращение',
        'testTest@ulges.ru',
        ['paklinas@ulges.ru'],  # kirillovag@ulges.ru
        fail_silently=False,
        html_message=render_to_string("email/feedback_admin.html", data)
    )

    return JsonResponse({'results': data})


def hisory_message(request):
    """ Вывод истории обращений для пользователя """
    data_history_upload = []
    user_name = request.POST.get('user_name')

    drop_message = FeedBack.objects.filter(fb_user_name=user_name)
    for drop_history in drop_message:
        data_history = {
            "user_name": drop_history.fb_user_name,
            "message": drop_history.fb_message,
            "dateTime": drop_history.fb_dateTime[:16],
        }
        data_history_upload.append(data_history)
        print(data_history_upload)

    return JsonResponse(data_history_upload, safe=False)


def get_passport_info(request):
    """ Вывод Паспорта ТУ из базы данных по конкретному прибору учета """
    if request.method == 'POST':
        factory_meter = request.POST.get('factoryMeter', None)
        print(factory_meter)
        results_list_meter = []
        result_list_transform = []
        info_meter_account = DeviceAccount.objects.filter(factory_number=factory_meter)
        info_transform_account = TransformDevice.objects.filter(id_device__in=info_meter_account)
        if info_meter_account.exists():
            for info_meters in info_meter_account:
                results_list_meter.append({
                    'id': info_meters.id,  # Id в таблице
                    'model_id': info_meters.model_id,  # марка прибора
                    'factory_number': info_meters.factory_number,  # Заводской номер ПУ
                    'digit': info_meters.digit,  # Разрядность
                    'phase': info_meters.phase,
                    'voltage': info_meters.voltage,
                    'tr_k': info_meters.tr_k,
                    'meter_interval': info_meters.meter_interval,
                    'gos_install_date': info_meters.gos_install_date,
                    'production_date': info_meters.production_date[:-9],
                })
        if info_transform_account.exists():
            for info_transforms in info_transform_account:
                result_list_transform.append({
                    'Trans': info_transforms.Trans,
                    'TransPrimary': info_transforms.TransPrimary,
                    'TransSecondary': info_transforms.TransSecondary,
                    'TransType': info_transforms.TransType,
                    'TransPrecision': info_transforms.TransPrecision,
                    'TransInterval': info_transforms.TransInterval,
                })

        return JsonResponse({'meter': results_list_meter, 'transform': result_list_transform})
    else:
        return JsonResponse({'error': 'Чет не так'})


def passport_accordion(request):
    """ Вывод подробностей прибора учета в раскрывающийся список  """
    if request.method == 'POST':
        factory_meter = request.POST.get('factoryMeter', None)
        list_meter = []
        info_meter_account = DeviceAccount.objects.filter(factory_number=factory_meter)
        if info_meter_account.exists():
            for info_meters in info_meter_account:
                list_meter.append({
                    'model_id': info_meters.model_id,  # марка прибора
                    'factory_number': info_meters.factory_number,  # Заводской номер ПУ
                    'digit': info_meters.digit,  # Разрядность
                    'phase': info_meters.phase,
                    'voltage': info_meters.voltage,
                    'tr_k': info_meters.tr_k,
                    'meter_interval': info_meters.meter_interval,
                    'gos_install_date': info_meters.gos_install_date,
                    'production_date': info_meters.production_date[:-9],
                })
        return JsonResponse({'meter': list_meter})
    else:
        return JsonResponse({'error': 'Чет не так'})


def indicate_button(request):
    """ Страница Показания """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/indicate.html')
    else:
        return redirect('index')


def pay_obj(request):
    """ Страница Начисления по объекту """
    if request.user.is_authenticated:
        return render(request, 'avtoriz/content/payment_object.html')
    else:
        return redirect('index')


def get_object_payment(request):
    """ Начисления по объекту - заполнение """
    data_object_pay = []
    agreement_number = request.POST.get('agreement_number', None)
    name_object = request.POST.get('obj_name', None)
    id_dogovor = Agreement.objects.filter(number_agreement=agreement_number).first()
    print(name_object, id_dogovor.id_Ulges)
    if request.method == 'POST':
        ulges_obj_pay = ulgesdbObjectPayment()
        ulges_obj_pay.object_pay(id_dogovor.id_Ulges, name_object)
        data_object_pay = ulges_obj_pay.get_object_pay()
        print(data_object_pay)

        return JsonResponse({'results': data_object_pay})


def get_data_meter(request):
    """ Вывод показаний из базы данных """
    ulges_meterdb = ulgesdbMeterReadings()
    data_meter_readings = []
    if request.method == 'POST':
        factory_meter = request.POST.get('factoryMeter', None)
        id_point_reg = DeviceAccount.objects.filter(factory_number=factory_meter)
        for id_point_reg_list in id_point_reg:
            ulges_meterdb.meter_readings(id_point_reg_list.id_Ulges)
            data_meter_readings = ulges_meterdb.get_data_meter()

    return JsonResponse({'results': data_meter_readings})


def logout_user(request):
    """ Выход из системы """
    UserActionLogger.objects.create(username=request.user.username, email=request.user.email
                                    , action='Выход из системы')
    logout(request)
    return redirect('index')


def get_desired_partner_id(request):
    """ Возвращаем договор пользователю по нажатию """
    if request.method == 'GET' or request.method == 'POST':
        desired_agreement_id = request.POST.get('desired_agreement_id', request.GET.get('desired_agreement_id'))
        request.session['desired_agreement_id'] = desired_agreement_id
        print(desired_agreement_id)
        return JsonResponse({'success': True})
    else:
        print('Не работает чет')


def get_payment(request):
    """Отображение начислений из базы данных"""
    data_abonent = []
    agreement_number = request.POST.get('agreement_number', None)
    id_dogovor = Agreement.objects.filter(number_agreement=agreement_number).first()
    print(id_dogovor.id_Ulges)
    print(agreement_number)
    if request.method == 'POST':
        ulges_abndb = ulgesdbAbnSchet()
        ulges_abndb.abn_schet(id_dogovor.id_Ulges)
        data_abonent = ulges_abndb.get_data_abn()
    print(data_abonent)

    return JsonResponse({'results': data_abonent})


def index(request):
    """Авторизация"""
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is None:
                try:
                    user = CustomUser.objects.get(email=username)
                    user = authenticate(request, username=user.username, password=password)
                except CustomUser.DoesNotExist:
                    pass
            if user is not None:
                login(request, user)
                UserActionLogger.objects.create(username=request.user.username, email=request.user.email
                                                , action='Вход в систему')
                return redirect('home')
            else:
                error_message = "Пользователь не найден."
    else:
        form = AuthenticationForm()

    return render(request, 'avtoriz/login.html', {'form': form, 'error_message': error_message})


def generate_confirmation_code():
    """ Генерация кода подтверждения """
    return str(uuid.uuid4())


def register(request):
    """ Регистрация """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Генерация ссылки для подтверждения регистрации
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://{get_current_site(request).domain}/activate/{uid}/"
            subject = 'Подтверждение регистрации'
            message = f'Для подтверждения регистрации перейдите по ссылке: {activation_link}'
            from_email = 'testTest@ulges.ru'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'avtoriz/activate_email.html', {'activation_link': activation_link})
        else:
            errors = form.errors
            return render(request, 'avtoriz/register.html', {'form': form, 'errors': errors})
    else:
        form = RegistrationForm()
    return render(request, 'avtoriz/register.html', {'form': form})


def activate(request, uidb64):
    """ Активация на почте """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        user.is_active = True
        user.save()

        # Авторизуем пользователя после активации
        login(request, user)
        UserActionLogger.objects.create(username=request.user.username, email=request.user.email
                                        , action='Успешная активация после регистрации')
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('index')


def add_contract(request):
    """ Добавить договор """
    client_ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    id_abn_ulges = None
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract_number = form.cleaned_data['contract_number']
            inn = form.cleaned_data['inn']
            contract_date = form.cleaned_data['contract_date']
            entity_type = request.POST.get('entityType')
            ulgesdb_instance = ulgesbdexecute()
            try:
                if entity_type == 'individual':
                    ulgesdb_instance.individual(contract_number)
                    data_partner, data_agreement, data_object, data_point = ulgesdb_instance.get_data_ulges()
                    object_ids = []
                    partner_check = Partner.objects.filter(id_Ulges=data_partner['idAbn'],
                                                           name=data_partner['NameAbn']).first()
                    if Agreement.objects.filter(
                            partner_id__id_Ulges=data_partner['idAbn']).exists() and UserPartner.objects.filter(
                        id_customUser=request.user.id, id_partner=partner_check.id).exists():
                        error_message = f"Вы уже активировали данный договор"
                        return JsonResponse({'error_message': error_message})
                    elif Agreement.objects.filter(
                            partner_id__id_Ulges=data_partner['idAbn']).exists() and not UserPartner.objects.filter(
                        id_customUser=request.user.id, id_partner=partner_check.id).exists():
                        print('Кукарача')
                        id_abn_ulges = data_partner['idAbn']
                    else:
                        if data_partner and data_object:
                            partner_create = Partner.objects.create(id_Ulges=data_partner['idAbn'],
                                                                    name=data_partner['NameAbn'],
                                                                    type_partner='Физическое лицо', inn=None,
                                                                    kpp=None,
                                                                    legal_address=None,
                                                                    mail_address=None)
                            partner_create.save()
                            id_abn_ulges = data_partner['idAbn']
                            agreement_create = Agreement.objects.create(id_Ulges=None,
                                                                        partner_id=partner_create,
                                                                        number_agreement=contract_number,
                                                                        conclusion_date=None,
                                                                        terminate_date=None,
                                                                        type_agreement=None)
                            agreement_create.save()
                            for data_objects in data_object:
                                object_create = ObjectAccount.objects.create(agreement_id=agreement_create,
                                                                             id_Ulges=data_objects['idObj'],
                                                                             address=data_objects['ObjectAddress'],
                                                                             object_type=data_objects['NameObject'],
                                                                             is_active=data_objects['is_active'])
                                object_create.save()
                                object_ids.append(object_create)

                            for object_id in object_ids:
                                for data_points in data_point:
                                    if data_points['idObj'] == object_id.id_Ulges:
                                        point_create = AccountPoint.objects.create(id_Ulges=data_points['idPoint'],
                                                                                   id_object_account=object_id,
                                                                                   conclusion_date=data_points[
                                                                                       'PointBegin'],
                                                                                   terminate_date=data_points[
                                                                                       'PointEnd'],
                                                                                   location=data_points['Location'],
                                                                                   name=data_points['NumberPoint'])
                                        point_create.save()

                                        meter_create = DeviceAccount.objects.create(id_object_account=point_create,
                                                                                    id_Ulges=data_points['idPointReg'],
                                                                                    model_id=data_points['MarkMeter'],
                                                                                    factory_number=data_points[
                                                                                        'NumberMeter'],
                                                                                    digit=data_points['Digit'],
                                                                                    phase=data_points['Phase'],
                                                                                    voltage=data_points['Voltage'],
                                                                                    tr_k=data_points['TR_K'],
                                                                                    DateEnd=data_points['DateEnd'],
                                                                                    meter_interval=data_points[
                                                                                        'MeterInterval'],
                                                                                    gos_install_date=data_points[
                                                                                        'DateCheck'],
                                                                                    production_date=data_points[
                                                                                        'DateBegin'])

                                        meter_create.save()

                                        transform_create = TransformDevice.objects.create(id_device=meter_create,
                                                                                          Trans=data_points['Trans'],
                                                                                          TransPrimary=data_points[
                                                                                              'TransPrimary'],
                                                                                          TransSecondary=data_points[
                                                                                              'TransSecondary'],
                                                                                          TransType=data_points[
                                                                                              'TransType'],
                                                                                          TransPrecision=data_points[
                                                                                              'TransPrecision'],
                                                                                          TransInterval=data_points[
                                                                                              'TransInterval'])
                                        transform_create.save()
                        else:
                            error_message = f"Данные не найдены"
                            return JsonResponse({'error_message': error_message})
                elif entity_type == 'legal':
                    ulgesdb_instance.legal(inn, contract_number, contract_date)

                    data_partner, data_agreement, data_object, data_point = ulgesdb_instance.get_data_ulges()
                    object_ids = []
                    partner_check = Partner.objects.filter(id_Ulges=data_partner['idAbn'], name=data_partner['NameAbn'],
                                                           inn=data_partner['INN'])
                    if Agreement.objects.filter(
                            partner_id__id_Ulges=data_partner['idAbn']).exists() and UserPartner.objects.filter(
                        id_customUser=request.user.id, id_partner=partner_check.id).exists():
                        error_message = f"Вы уже активировали данный договор"
                        return JsonResponse({'error_message': error_message})
                    elif Agreement.objects.filter(
                            partner_id__id_Ulges=data_partner['idAbn']).exists() and not UserPartner.objects.filter(
                        id_customUser=request.user.id, id_partner=partner_check.id).exists():
                        print('Кукарача2')
                        id_abn_ulges = data_partner['idAbn']
                    else:
                        if data_partner and data_agreement and data_object:
                            partner_create = Partner.objects.create(id_Ulges=data_partner['idAbn'],
                                                                    name=data_partner['NameAbn'],
                                                                    type_partner='Юридическое лицо',
                                                                    inn=data_partner['INN'],
                                                                    kpp=data_partner['KPP'],
                                                                    legal_address=data_partner['LegalAddress'],
                                                                    mail_address=data_partner['PostAddress'])
                            partner_create.save()
                            agreement_create = Agreement.objects.create(id_Ulges=data_agreement['idDogovor'],
                                                                        partner_id=partner_create,
                                                                        number_agreement=data_agreement['DogNumber'],
                                                                        conclusion_date=data_agreement['DogDate'],
                                                                        terminate_date=data_agreement['DateEnd'],
                                                                        type_agreement=data_agreement['TypeDog'])
                            agreement_create.save()
                            for data_objects in data_object:
                                object_create = ObjectAccount.objects.create(agreement_id=agreement_create,
                                                                             id_Ulges=data_objects['idObj'],
                                                                             address=data_objects['ObjectAddress'],
                                                                             object_type=data_objects['NameObject'],
                                                                             is_active=data_objects['is_active'])
                                object_create.save()
                                object_ids.append(object_create)

                            for object_id in object_ids:
                                for data_points in data_point:
                                    if data_points['idObj'] == object_id.id_Ulges:
                                        point_create = AccountPoint.objects.create(id_Ulges=data_points['idPoint'],
                                                                                   id_object_account=object_id,
                                                                                   conclusion_date=data_points[
                                                                                       'PointBegin'],
                                                                                   terminate_date=data_points[
                                                                                       'PointEnd'],
                                                                                   location=data_points['Location'],
                                                                                   name=data_points['NumberPoint'])
                                        point_create.save()

                                        meter_create = DeviceAccount.objects.create(id_object_account=point_create,
                                                                                    id_Ulges=data_points['idPointReg'],
                                                                                    model_id=data_points['MarkMeter'],
                                                                                    factory_number=data_points[
                                                                                        'NumberMeter'],
                                                                                    digit=data_points['Digit'],
                                                                                    phase=data_points['Phase'],
                                                                                    voltage=data_points['Voltage'],
                                                                                    tr_k=data_points['TR_K'],
                                                                                    DateEnd=data_points['DateEnd'],
                                                                                    meter_interval=data_points[
                                                                                        'MeterInterval'],
                                                                                    gos_install_date=data_points[
                                                                                        'DateCheck'],
                                                                                    production_date=data_points[
                                                                                        'DateBegin'])

                                        meter_create.save()

                                        transform_create = TransformDevice.objects.create(id_device=meter_create,
                                                                                          Trans=data_points['Trans'],
                                                                                          TransPrimary=data_points[
                                                                                              'TransPrimary'],
                                                                                          TransSecondary=data_points[
                                                                                              'TransSecondary'],
                                                                                          TransType=data_points[
                                                                                              'TransType'],
                                                                                          TransPrecision=data_points[
                                                                                              'TransPrecision'],
                                                                                          TransInterval=data_points[
                                                                                              'TransInterval'])
                                        transform_create.save()
                        else:
                            error_message = f"Данные не найдены"
                            return JsonResponse({'error_message': error_message})
            except Exception as e:
                error_message = f"Договор не найден"
                return JsonResponse({'error_message': error_message})

            try:
                print('lol', id_abn_ulges)
                if inn == '':
                    partner = Partner.objects.get(id_Ulges=id_abn_ulges)
                else:
                    print('Сюда тоже заходит')
                    partner = Partner.objects.get(inn=inn)
                print('\nПартнер', partner)
                print(contract_number, contract_date)
                agreement = Agreement.objects.get(number_agreement=contract_number)
                print('\nДоговор', agreement)

                objects = ObjectAccount.objects.filter(agreement_id=agreement)  # Получаем данные Объекта учета
                objects_ids = list(objects.values_list('id', flat=True))

                point = AccountPoint.objects.filter(
                    id_object_account__id__in=objects_ids)  # Получаем данные точки учета
                point_ids = list(point.values_list('id', flat=True))

                device = DeviceAccount.objects.filter(
                    id_object_account__id__in=point_ids)
                device_ids = list(device.values_list('id', flat=True))

                transformator = TransformDevice.objects.filter(id_device__id__in=device_ids)
                transformator_ids = list(transformator.values_list('id', flat=True))

                # Проверяем, существуют ли записи для данного договора
                user_agreement = UserAgreement.objects.filter(id_agreement=agreement.id, id_customUser=request.user.id)
                user_partner = UserPartner.objects.filter(id_partner=partner.id, id_customUser=request.user.id)

                if user_agreement.exists() and user_partner.exists():
                    print('Кукусики')
                else:
                    # Отправляем письмо администратору для подтверждения
                    confirmation_code = generate_confirmation_code()
                    ConfirmationData.objects.create(
                        user_id=request.user.id,
                        partner_id=partner.id,
                        agreement_id=agreement.id,
                        objects_ids=objects_ids,
                        point_ids=point_ids,
                        device_ids=device_ids,
                        transformator_ids=transformator_ids,
                        email=request.user.email,
                        confirmation_code=confirmation_code
                    )
                    context = {
                        'contract_number': contract_number,
                        'inn': inn,
                        'client_ip': client_ip,
                        'user_agent': user_agent,
                        'userName': request.user,
                        'userId': request.user.id,
                        'userEmail': request.user.email,
                        'get_current_site': get_current_site(request),
                        'confirmation_code': confirmation_code,
                    }
                    send_mail(
                        f'Подтверждение данных {contract_number}',
                        f'Подтвердите данные',
                        'testTest@ulges.ru',
                        ['paklinas@ulges.ru'],  # kirillovag@ulges.ru
                        html_message=render_to_string("email/confirmationContract.html", context),
                        fail_silently=False,
                    )

                    info_message = "Данные ожидают подтверждения.\n Вам придет уведомление на почту"
                    UserActionLogger.objects.create(username=request.user.username, email=request.user.email
                                                    , action='Ожидание подтверждения регистрации договора')
                    UserNote.objects.create(user_id=request.user.id,
                                            message=f'Договор №{contract_number} ожидает подтверждения')

                    return JsonResponse({'info_message': info_message})
            except Agreement.DoesNotExist as e:
                error_message = f"Проверьте корректность введенных данных"
                return JsonResponse({'error_message': error_message})
            except Partner.DoesNotExist as e:
                error_message = f"Проверьте корректность введенных данных"
                return JsonResponse({'error_message': error_message})
        else:
            error_message = "Проверьте корректность введенных данных"
            return JsonResponse({'error_message': error_message})
    else:
        print('Не POST')


def confirm_contract(request, confirmation_code):
    """ Подтверждение регистрации договора """
    confirmation_data = get_object_or_404(ConfirmationData, confirmation_code=confirmation_code)
    confirmation_data.save()

    user_agreement = UserAgreement.objects.create(id_agreement=confirmation_data.agreement_id,
                                                  id_customUser=confirmation_data.user_id, is_approved=True)
    user_partner = UserPartner.objects.create(id_customUser=confirmation_data.user_id,
                                              id_partner=confirmation_data.partner_id,
                                              is_approved=True)
    user_agreement.save()
    user_partner.save()

    for counter_object in confirmation_data.objects_ids:
        user_object = UserObject.objects.create(id_customUser=confirmation_data.user_id, id_object=counter_object)
        user_object.save()

    for counter_point in confirmation_data.point_ids:
        user_point = UserPoint.objects.create(id_customUser=confirmation_data.user_id, id_point=counter_point)
        user_point.save()

    for counter_device in confirmation_data.device_ids:
        user_device = UserDeviceAccount.objects.create(id_customUser=confirmation_data.user_id,
                                                       id_device=counter_device)
        user_device.save()

    for counter_transform in confirmation_data.transformator_ids:
        user_transform = UserTransformator.objects.create(id_customUser=confirmation_data.user_id,
                                                          id_transform=counter_transform)
        user_transform.save()

    time.sleep(1)
    send_mail(
        'Информация для пользователя',
        'Успешное подтверждение данных.',
        'testTest@ulges.ru',
        [confirmation_data.email],  # kirillovag@ulges.ru
        html_message=render_to_string("email/confirmationData.html"),
        fail_silently=False,
    )
    UserNote.objects.create(user_id=confirmation_data.user_id,
                            message=f'Договор успешно подтвержден и доступен для Вас')

    return render(request, 'avtoriz/confirmation_success.html')


def get_point(request):
    """ Поиск в бд записей об ТУ и ПУ по объекту """
    if request.method == 'POST':
        obj_name = request.POST.get('objectName', None)
        obj_address = request.POST.get('objectAddress', None)
        print(obj_name, 'ХАХАХА')

        try:
            point_info = AccountPoint.objects.filter(
                id_object_account__address=obj_address,
                id_object_account__object_type=obj_name
            )
            data_point_list = []
            for point in point_info:
                data_point_list.append({
                    'location': point.location,
                    'conclusion_date': point.conclusion_date[:-9],
                })
            data_device_list = []
            for point in point_info:
                device_info = DeviceAccount.objects.filter(
                    id_object_account__id=point.id
                )
                for device in device_info:
                    data_device_list.append({
                        'factory_number': device.factory_number,
                        'model_id': device.model_id,
                        'DateEnd': device.DateEnd,
                    })
                print('Данные Точки\n', data_point_list, 'Данные прибора\n', data_device_list)
            return JsonResponse({'infoPoint': data_point_list, 'infoDevice': data_device_list}, status=200)
        except AccountPoint.DoesNotExist:
            return JsonResponse({'infoPoint': None, 'infoDevice': None}, status=200)
