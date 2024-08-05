var agreement_number = null; //Номер договора
/* Обработка клика по кнопке Начисления */
$('#payment-button').click(function() {
        var url = '/deposits/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-deposits').html();
                $('#main-panel-content').html(content);
                $('#title-page').html('Начисления');
                history.pushState(null, null, url);
                var desired_agreement_number = localStorage.getItem('desired_agreement_number');
                agreement_number = desired_agreement_number;
                console.log(agreement_number);
                init_payment_table(agreement_number);
                $("#main-panel-content").hide().fadeIn();
            }
        });
    });
/* ----------------------------------------------------- */

/* Запрос в базу данных по данному договору (о начислениях) */
function init_payment_table(ag_num) {
    $.ajax({
        url: '/get_payment_info/',
        method: 'POST',
        data: {
            'agreement_number': ag_num
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        success: function(data) {
            console.log(data.results.length); //ЭТО ПИШЕТ В КОНСОЛЬ
            if (data.results && data.results.length == 0) {
                $('#paymentTable').css('display', 'none');
                $('#infoAgreement').html('Начисления по договору №<b>' + ag_num + '</b> не найдены');
                $('#card-body-info').hide();
            } else {
                $('#card-body-info').show();
                $('#paymentTable').css('display', 'table');
                $('#infoAgreementTrue').html('Начисления по договору № ' + ag_num);
                fillPaymentTable(data.results);
                init_DataTable_PaymentTable();
            }
        }
    });
}
/* --------------------------------------------------------------------------- */

/* Заполнение таблицы Начисления */
function fillPaymentTable(data){
    var $table_body_payment = $('#paymentBody')
    $table_body_payment.empty();
    var maxRows = data.length;
    for (var i = 0; i < maxRows; i++) {
        var $row = $('<tr>');

        for (var key in data[i]) {
            if (data[i].hasOwnProperty(key)) {
                var $cellElement = $('<td>').text(data[i][key]);
                $row.append($cellElement);
            }
        }
        $table_body_payment.append($row);
    }
}
/* ------------------------------------------------------------------------------ */

function init_DataTable_PaymentTable(){
    $('#paymentTable').DataTable({
        language: {
        url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
                },
        pageLength: 8,
        lengthMenu: [
            [8, 10, 20, -1],
            [8, 10, 20, 50]
        ],
        "bDestroy": true,
        "aoColumnDefs": [{
            "bSortable": false,

        }],
        order: [
            [0, 'desc']
        ]
    });
}

if (window.localStorage && window.location.pathname === '/deposits/') {
    $('#top-panel').css('display', 'flex');
    init_payment_table(sessionStorage.getItem('desired_agreement_number'));
}
