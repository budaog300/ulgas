from .models import UserAgreement, UserPartner, UserObject, Partner, Agreement, ObjectAccount
from django.core.paginator import Paginator


def user_data(request):
    if request.user.is_authenticated:
        user_agreement_ids = UserAgreement.objects.filter(id_customUser=request.user.id, is_approved=True).values_list(
            'id_agreement', flat=True)
        user_partner_ids = UserPartner.objects.filter(id_customUser=request.user.id, is_approved=True).values_list(
            'id_partner', flat=True)

        if user_agreement_ids and user_partner_ids:
            # Получаем Объекты
            objects_ids = UserObject.objects.filter(id_customUser=request.user.id).values_list('id_object',
                                                                                               flat=True)
            # Получаем данные из статики (что заполнено по пользователю, фильтрация выборка данных)
            partners = Partner.objects.filter(id__in=user_partner_ids)
            agreements = Agreement.objects.filter(id__in=user_agreement_ids)
            objectpoint = ObjectAccount.objects.filter(id__in=objects_ids)
            paginator = Paginator(partners, 3)  # 3 партнера на страницу
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            data = {
                'partners': partners,  # Контрагент
                'agreements': agreements,  # Договор
                'objectpoint': objectpoint,  # Объект учета (точка на карте)
                'user_agreement_ids': user_agreement_ids,
                'user_partner_ids': user_partner_ids,
                'page_obj': page_obj,
            }
        else:
            data = {
                'partners': [],  # Контрагент
                'agreements': [],  # Договор
                'objectpoint': [],  # Объект учета
                'user_agreement_ids': [],
                'user_partner_ids': [],
                'page_obj': [],
            }
        return data
    else:
        return {}
