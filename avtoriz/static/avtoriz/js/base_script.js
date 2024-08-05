$(document).on('click', '.btn-exit', function(event) {
    event.stopPropagation();
    // Открываем модальное окно после удаления
    $('#basicModal').modal('show');
});
/* ------------------------------------------------------ */
// Получаем все кнопки
const buttons = document.querySelectorAll('.btn');

// Функция для обработки нажатия на кнопку
function handleButtonClick(event) {
    // Удаляем класс "active" у всех кнопок
    buttons.forEach(button => {
        button.classList.remove('active');
    });


    // Добавляем класс "active" к нажатой кнопке
    event.target.classList.add('active');
}

// Добавляем обработчик события для каждой кнопки
buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
});
/* ------------------------------------------------------ */
/* Обработка отображения страницы при клике на блоке с договорами */
var desired_agreement_number;
var selectedBlock = null; // Переменная для хранения выбранного блока
$(document).on('click', '.agreement-block', function() {

    // Убираем подсветку с предыдущего выбранного блока, если такой есть
    if (selectedBlock !== null) {
        $(selectedBlock).css({
            'cursor': 'pointer',
            'background': 'linear-gradient(315deg, #002244,#3457D5)',
            'color': 'white',
            'text-shadow': '0 0 5px #000'
        });
        localStorage.removeItem('desired_agreement_number');
    }

    // Выделяем текущий блок
    $(this).css({
        "background": "blue",
        "color": "white",
        "text-shadow": "none"
    });
    selectedBlock = $(this);
    $('#top-panel').css('display', 'flex');

    var desired_agreement_id = $(this).data('agreement_id'); // Получаем id договора и отправляем во вью
    console.log(desired_agreement_id);
    var desired_agreement_number = $(this).data('agreement_number');
    localStorage.setItem('desired_agreement_number', desired_agreement_number);
    sessionStorage.setItem('desired_agreement_number', desired_agreement_number);
    $.ajax({
        url: '/get_desired_partner/',
        method: 'POST',
        data: {
            'desired_agreement_id': desired_agreement_id
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            $('#main-button').click();
        }
    });
});
/* -------------------------------------------------------------- */
function init_object_table() {
    $('#objectTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        pageLength: 5,
        lengthMenu: [
            [5, 10, 20, -1],
            [5, 10, 20, 50]
        ],
        order: [
            [2, 'desc']
        ],
        "aoColumnDefs": [{
            "bSortable": false,
            "aTargets": [-1] // <-- gets last column and turns off sorting
        }],
        initComplete: function() {
            // Custom filter options
            var customFilterOptions = ['Все', 'Активные', 'Неактивные'];
            var customFilter = $('<select></select>')
                .appendTo($('.dataTables_length'))
                .addClass('custom-filter')
                .attr('id', 'statusFilter')
                .css('margin-left', '50px');
            customFilterOptions.forEach(function(option) {
                var selected = (option === 'Активные') ? 'selected' : ''; // Делаем 'Активные' выбранным по умолчанию
                var value = '';

                if (option === 'Все') {
                    value = '';
                } else if (option === 'Активные') {
                    value = 'true';
                } else if (option === 'Неактивные') {
                    value = 'false';
                }

                customFilter.append('<option value="' + value + '" ' + selected + '>' + option + '</option>');
                $('#objectTable').DataTable().column(2).search('true').draw();
            });
            customFilter.on('change', function() {
                var val = $(this).val();
                if (val === 'true' || val === 'false') {
                    $('#objectTable').DataTable().column(2).search(val).draw();
                } else {
                    $('#objectTable').DataTable().column(2).search('').draw();
                }
            });
        },
        drawCallback: function() {
            // Highlight rows based on a condition
            $('#objectTable tbody tr').each(function() {
                var cells = this.querySelectorAll("td:not(:last-child)");
                if (cells.length >= 2) {
                    var secondToLastCellValue = cells[cells.length - 1].innerText || cells[cells.length - 1].textContent;
                    if (secondToLastCellValue.trim() === "false") {
                        this.style.background = "#ff000020";
                    }
                }
            });
        }
    });
}
/* Обработчики кликов-------------------------------------------- */

// Кнопка Главная //
$(document).ready(function() {
    init_object_table();
    $('#main-button').click(function() {
        var url = '/main/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-main').html();
                $('#main-panel-content').html(content);

                $('#title-page').html('Главная');
                history.pushState(null, null, url);
                init_object_table();
                $("#main-panel-content").hide().fadeIn();
            }
        });
    });
    $('#note-button').click(function() {
        var url = '/note/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-note').html();
                $('#main-panel-content').html(content);
                $('#title-page').html('Уведомления');
                history.pushState(null, null, url);
                $("#main-panel-content").hide().fadeIn();
            }
        });
    });

    $('#appeal-button').click(function() {
        var url = '/appeals/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-appeal').html();
                $('#main-panel-content').html(content);
                $('#title-page').html('Обращения');
                history.pushState(null, null, url);
                sendAppeals();
                $("#main-panel-content").hide().fadeIn();
            }
        });
    });

    $('#document-button').click(function() {
        var url = '/document/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-document').html();
                $('#main-panel-content').html(content);
                $('#title-page').html('Документы');
                history.pushState(null, null, url);
                $("#main-panel-content").hide().fadeIn();
            }
        });
    });

    $('#point-button').click(function() {
        var url = '/meter/';
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var content = $(data).find('#content-meter').html();
                $('#main-panel-content').html(content);
                $('#title-page').html('Точка учета');
                history.pushState(null, null, url);
                init_pointTable(sessionStorage.getItem('objectName'), sessionStorage.getItem('objectAddress'));
                //alert(sessionStorage.getItem('objectName'));
                $("#main-panel-content").hide().fadeIn();
                accordionPassport();
            }
        });
    });

    window.addEventListener('popstate', function(event) {
        location.reload();
    });
});
// ------------------------------------------------------------------------- //
/* -----------------------SIDEBAR-------------------------------- */
//$(document).ready(function() {
//    $('#sidebarCollapse').on('click', function() {
//        $('#sidebar').toggleClass('active');
//    });
//});
var sidebarOpen = true;
function toggleNav() {
    if (sidebarOpen) {
        closeNav(); // Если боковая панель открыта, вызываем функцию закрытия
    } else {
        openNav(); // Если боковая панель закрыта, вызываем функцию открытия
    }
}

function openNav() {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById("sidebar").style.visibility  = "visible";
    document.getElementById("sidebar").style.position  = "relative";
    document.getElementById("main").style.backgroundImage = "linear-gradient(315deg,  #002244, #3457D5)";
    sidebarOpen = true; // Устанавливаем состояние боковой панели как открытое
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("sidebar").style.visibility  = "hidden";
    document.getElementById("sidebar").style.position  = "fixed";
    document.getElementById("main").style.backgroundImage = "none";
    sidebarOpen = false; // Устанавливаем состояние боковой панели как закрытое
}
/* -------------------------------------------------------------- */

/* ----------------------ВЫЗЫВАЕМЫЕ ФУНКЦИИ---------------------- */
function sendAppeals() {
    $("#contact_us_form").on("submit", function(event) {
        event.preventDefault();
        var name = $("#name").val();
        var email = $("#email").val();
        var phone_number = $("#phone_number").val();
        var messageUser = $("#messageUser").val();
        var user_name = document.getElementById('userInfo').textContent;
        // Отправляем данные на сервер с помощью AJAX
        $.ajax({
            url: "/appeal-done/", // Здесь указываем URL-адрес серверного обработчика
            type: "POST",
            data: {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "messageUser": messageUser,
                "user_name": user_name,
            },
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Данные отправлены');
                $('#contact_us_form')[0].reset();
                $('#successModal').modal('show');
                $('#successModalLabel').html('Обращение отправлено');
                $('#modal-body').html('Здравствуйте, ' + name + '\nВаше обращение успешно отправлено, в скором времени вернемся к вам с обратной связью!')
            },
            error: function(error) {
                $('#successModal').show();
                $('#successModalLabel').html('Ошибка');
                $('#modal-body').html('Здравствуйте, ' + name + '\nПроизошла ошибка, просим Вас обратиться за помощью' + '<button class="btn btn-outline-primary">Помощь</button>');
            },
        });
    });
}
/* --------------------------------------------------------------- */
var objectName = null;
var objectAddress = null;
$(document).on('click', '.detailsButton', function() {
    objectName = $(this).closest('tr').find('td:eq(0)').text();
    objectAddress = $(this).closest('tr').find('td:eq(1)').text();
    sessionStorage.setItem('objectName', objectName);
    sessionStorage.setItem('objectAddress', objectAddress);
    $('#point-button').click();
});
//  Инициализация данных по ТУ и ПУ  //
function init_pointTable(name, address) {
    $.ajax({
        url: '/get_point_info/',
        type: 'POST',
        data: {
            'objectName': name,
            'objectAddress': address,
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            if (data.infoPoint != '' && data.infoDevice != '') {
                var mergedData = [
                    data.infoPoint,
                    data.infoDevice
                ];
                $('#infoObject').html(name);
                $('#pointTable').show();
                fillTable(mergedData);
                init_DataTable_pointTable();
                sessionStorage.setItem('name', name)
            } else {
                $('#body-object').html(name + '<h6 style="color: red;">Данные не найдены</h6>');
                $('#pointTable').hide();
            }
        },
        error: function() {
            alert('Ошибка');
        }
    });
}

//  Заполнение таблицы ТУ и ПУ  //
function fillTable(data) {
    var tableBody = document.getElementById('pointTabBody');
    var activeRow = null;
    tableBody.innerHTML = '';
    var maxRows = Math.max(data[0].length, data[1].length);

    for (var i = 0; i < maxRows; i++) {
        var row = tableBody.rows[i] || tableBody.insertRow(i);
        for (var key in data[1][i]) {
            if (data[1][i].hasOwnProperty(key)) {
                var cellElement = row.insertCell();
                cellElement.textContent = data[1][i][key];
            }
        }

        //data[0]
        for (var key in data[0][i]) {
            if (data[0][i].hasOwnProperty(key)) {
                var cellElement = row.insertCell();
                cellElement.textContent = data[0][i][key];
            }
        }

        var detailsCell = row.insertCell();
        var detailsButton = document.createElement('div');
        detailsButton.innerHTML = '<div class="btn-group">' +
            '<button class="btn btn-secondary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown"' +
            'aria-expanded="false" onclick="event.cancelBubble=true;"></button>' + '<ul class="dropdown-menu">' +
            '<li><button class="passportButton dropdown-item" id="passportButton" onclick="showPassport()">Паспорт ТУ</button></li>' +
            '<li><button class="indicateButton dropdown-item" id="indicateButton" onclick="showIndicate()">Показания</button></li>' +
            '</ul></div>';
        detailsButton.className = 'details-button';
        detailsCell.appendChild(detailsButton);
    }
}

function init_DataTable_pointTable() {
    $('#pointTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        pageLength: 5,
        lengthMenu: [
            [5, 10, 20],
            [5, 10, 20]
        ],
        "bDestroy": true,
        "aoColumnDefs": [{
            "bSortable": false,
            "aTargets": [-1] // <-- получает последний столбец и отключает сортировку
        }],
        order: [
            [4, 'desc']
        ],
        initComplete: function() {
            var customFilterOptions = ['Все', 'Активные', 'Неактивные']; // Замените это на свои собственные критерии
            var customFilter = $('<select></select>')
                .appendTo($('.dataTables_length'))
                .addClass('custom-filter')
                .attr('id', 'customFilter') // Присваиваем ID кастомному фильтру
                .css('margin-left', '50px'); // Добавляем стиль для передвижения по центру
            customFilterOptions.forEach(function(option) {
                var selected = (option === 'Активные') ? 'selected' : ''; // Делаем 'Активные' выбранным по умолчанию
                var value = '';

                if (option === 'Все') {
                    value = '';
                } else if (option === 'Активные') {
                    value = 'true';
                } else if (option === 'Неактивные') {
                    value = 'false';
                }

                customFilter.append('<option value="' + value + '" ' + selected + '>' + option + '</option>');
                $('#pointTable').DataTable().column(2).search('^$', true, false).draw();
            });
            customFilter.on('change', function() {
                var val = $(this).val();
                if (val === 'true') {
                    $('#pointTable').DataTable().column(2).search('^$', true, false).draw();
                } else if (val === 'false') {
                    $('#pointTable').DataTable().column(2).search('.+', true, false).draw();
                } else {
                    $('#pointTable').DataTable().column(2).search('').draw();
                }
            });
            var inactiveButton = $('<button></button>')
                .appendTo($('.dataTables_length'))
                .addClass('custom-filter-button')
                .attr('id', 'inactiveButton')
                .text('Начисления по объекту')
                .css({
                    'margin-left': '10px',
                    'background': 'white',
                    'border': '1px solid gray'
                });

            inactiveButton.on('click', function() {
                payment_object();
            });
        },
        drawCallback: function() {
            // Перебираем каждую строку на текущей странице после перерисовки
            $('#pointTable tbody tr').each(function() {
                // Получаем все ячейки (td) текущей строки, кроме последней
                var cells = this.querySelectorAll("td:not(:last-child)");

                // Проверяем, что есть хотя бы две ячейки (предпоследняя и последняя)
                if (cells.length >= 2) {
                    // Получаем значение в предпоследней ячейке (предпоследний td)
                    var secondToLastCellValue = cells[cells.length - 3].innerText || cells[cells.length - 3].textContent;


                    // Проверяем условие: если значение предпоследней ячейки равно "false"
                    if (secondToLastCellValue.trim() != "") {
                        this.style.background = "#ff000020";
                    }
                }
            });
        }
    });
}
//Начисления по объекту - страница
function payment_object() {
    var url = '/payment_obj/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            var content = $(data).find('#content-payment-object').html();
            $('#main-panel-content').html(content);
            $('#title-page').html('Показания');
            history.pushState(null, null, url);
            payment_object_init();
        }
    });
}
//Начисления по объекту - загрузка
function payment_object_init() {
    $.ajax({
        url: '/get_object_payment/',
        method: 'POST',
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        data: {
            'agreement_number': sessionStorage.getItem('desired_agreement_number'),
            'obj_name': sessionStorage.getItem('objectName'),
        },
        cache: false,
        success: function(data) {
            $('#infoPaymentObject').html('<b>Начисления по объекту</b> - ' + sessionStorage.getItem('objectName'));
            $('#indicateError').html();
            $('#objectPayTable').show();
            if (data.results.length) {
                var $table_body_object = $('#object_payBody')
                $table_body_object.empty();
                var maxRows = data.results.length;
                for (var i = 0; i < maxRows; i++) {
                    var $row = $('<tr>');

                    for (var key in data.results[i]) {
                        if (data.results[i].hasOwnProperty(key)) {
                            var $cellElement = $('<td>').text(data.results[i][key]);
                            $row.append($cellElement);
                        }
                    }
                    $table_body_object.append($row);
                }
                init_paymentObject_table();

            } else {
                $('#objectPayTable').hide();
                $('#indicateError').html('<b style="color: red;">Данные не найдены</b>');
            }
        }
    });
}

function back_main() {
    $('#main-button').click();
}

function backMeter() {
    console.log('Лол');
    $('#point-button').click();
}
/* ------------------Настройка переходов между страницами-------------------- */
if (window.localStorage && window.location.pathname === '/meter/') {
    init_pointTable(sessionStorage.getItem('objectName'), sessionStorage.getItem('objectAddress'));
    $('#top-panel').css('display', 'flex');
    accordionPassport();
}
if (window.localStorage && window.location.pathname === '/passport/') {
    initialize_passport_tab(sessionStorage.getItem('rowData'));
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/indicate_info/') {
    initialize_indicate_tab(sessionStorage.getItem('rowDataIndicate'));
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/payment_obj/') {
    payment_object_init();
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/main/') {
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/deposits/') {
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/appeals/') {
    $('#top-panel').css('display', 'flex');
    sendAppeals();
}
if (window.localStorage && window.location.pathname === '/note/') {
    $('#top-panel').css('display', 'flex');
}
if (window.localStorage && window.location.pathname === '/document/') {
    $('#top-panel').css('display', 'flex');
}
/* -------------------------------------------------------------------------------- */
//Показания
function showIndicate() {
    var rowDataIndicate = "";
    $('#pointTable').on('click', '.indicateButton', function() {
        var row = $(this).closest('tr');
        row.find('td').slice(0, 1).each(function() {
            rowDataIndicate += $(this).text();
            sessionStorage.setItem('rowDataIndicate', rowDataIndicate);
        });
    });

    var url = '/indicate_info/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            var content = $(data).find('#content-indicate').html();
            $('#main-panel-content').html(content);
            $('#title-page').html('Показания');
            history.pushState(null, null, url);
            initialize_indicate_tab(rowDataIndicate);
        }
    });
}
//Загрузка показаний
function initialize_indicate_tab(factoryMeter) {
    $.ajax({
        url: '/get_data_info/',
        method: 'POST',
        data: {
            'factoryMeter': factoryMeter,
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            if (data.results.length == 0) {
                $('#indicateError').show();
                $('#indicateError').html("Показания не найдены");

                $('#dataTableInfo').hide();
            } else {
                $('#indicateError').hide();
                $('#dataTableInfo').show();
                var table_body_meter = document.getElementById('bodyMeter');
                table_body_meter.innerHTML = '';
                var maxRows = data.results.length;
                for (var i = 0; i < maxRows; i++) {
                    var row = table_body_meter.rows[i] || table_body_meter.insertRow(i);
                    var cell1 = row.insertCell(0);
                    cell1.textContent = factoryMeter;

                    for (var j = 1; j < Object.keys(data.results[i]).length; j++) {
                        var cellElement = row.insertCell(j);
                        cellElement.textContent = Object.values(data.results[i])[j];
                    }
                }
                init_indicate_table();
            }
        }
    });
}

//Паспорт ТУ
function showPassport() {
    var rowData = "";
    $('#pointTable').on('click', '.passportButton', function() {
        var row = $(this).closest('tr');
        row.find('td').slice(0, 1).each(function() {
            rowData += $(this).text();
            sessionStorage.setItem('rowData', rowData);
        });
    });
    var url = '/passport/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            var content = $(data).find('#content-passport').html();
            $('#main-panel-content').html(content);
            $('#title-page').html('Паспорт ТУ');
            history.pushState(null, null, url);
            //alert(sessionStorage.getItem('desired_agreement_number'));
            initialize_passport_tab(rowData);
        }
    });
}

function initialize_passport_tab(data) {
    $.ajax({
        url: '/get_passport_info/',
        method: 'POST',
        data: {
            'factoryMeter': data,
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            var results_meter = data.meter;
            var results_transform = data.transform;

            results_meter.forEach(function(result) {
                var strDate = result.gos_install_date;
                if (strDate != "" && strDate != null) {
                    strDate = strDate.slice(0, -9);
                }
                $('#modelHeader').html(result.model_id);
                $('#bodytext').html('<p>Заводской номер: <b>' + result.factory_number + '</b></p>' + '<p>Разрядность: <b>' + result.digit + '</b></p>' +
                    '<p>Фазность: <b>' + result.phase + '</b></p>' + '<p>Напряжение: <b>' + result.voltage + '</b></p>' +
                    '<p>Коэффициент трансформации: <b>' + result.tr_k + '</b></p>' +
                    '<p>Интервал поверки: <b>' + result.meter_interval + '</b></p>' +
                    '<p>Дата госпроверки: <b>' + strDate + '</b></p>' +
                    '<p>Дата установки: <b>' + result.production_date + '</b></p>');
            })

            results_transform.forEach(function(result_tr) {
                if (result_tr.Trans != null) {
                    $('#transformHeader').html(result_tr.Trans);
                    $('#transformBodyText').html('<p>Первичная: <b>' + result_tr.TransPrimary + '</b></p>' +
                        '<p>Вторичная: <b>' + result_tr.TransSecondary + '</b></p>' +
                        '<p>Тип трансформатора: <b>' + result_tr.TransType + '</b></p>' +
                        '<p>Точность трансформатора: <b>' + result_tr.TransPrecision + '</b></p>' +
                        '<p>Интервал проверки трансформатора: <b>' + result_tr.TransInterval + '</b></p>');

                } else {
                    $('#nav-profile').html('<br><p style="color:red;">Данные о трансформаторе не найдены</p>');
                }
            })
        }
    });
}

function init_indicate_table() {
    $('#dataTableInfo').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        pageLength: 5,
        lengthMenu: [
            [5, 10, 20, -1],
            [5, 10, 20, 50]
        ],
        order: [
            [1, 'desc']
        ],
        "aoColumnDefs": [{
            "bSortable": false,
            "aTargets": [-1] // <-- gets last column and turns off sorting
        }]
    });
}

function init_paymentObject_table() {
    $('#objectPayTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        pageLength: 5,
        lengthMenu: [
            [5, 10, 20, -1],
            [5, 10, 20, 50]
        ],
        order: [
            [2, 'desc']
        ],
        "aoColumnDefs": [{
            "bSortable": false,
            "aTargets": [-1] // <-- gets last column and turns off sorting
        }]
    });
}
/* -------------------------------------------------------------- */

/* Обработка формы Добавить договор */
$(document).on('submit', '#contractForm', function(e) {
    e.preventDefault();

    var form = $(this);
    // Выполнение AJAX-запроса для отправки данных формы
    $.ajax({
        type: 'POST',
        url: '/add_contract/',
        data: form.serialize(),
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            // Обработка ответа сервера и обновление сообщения об ошибке/успехе
            if (data.error_message) {
                console.log(data.error_message);
                $('#error-message').html(data.error_message);
                $('#error-message').css('color', 'red');
                $('#error-message').css('background-color', '#fc000033');
            } else if (data.info_message) {
                $('#error-message').html(data.info_message);
                $('#error-message').css('color', 'green');
                $('#error-message').css('background-color', '#00fc0833');

            } else {
                alert('Ошибка');
            }
            console.log("addSubmit click handler register")
        },
        error: function(error) {
            console.error('Ошибка');
        }

    });
});

function historyMessage() {
    console.log('ЛОЛ');
    var user_name = document.getElementById('userInfo').textContent;
    $('#nav-profile').html('');
    $.ajax({
        url: "/get_history/",
        type: "POST",
        data: {
            "user_name": user_name
        },
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            console.log('Данные загрузились');
            $('#nav-profile').append('<div class="alert alert-dark" role="alert">Количество обращений - ' + data.length + '</div>');
            for (var i = 0; i < data.length; i++) {
                $('#nav-profile').append('<div class="card mb-3"><div class="card-header">' + data[i].dateTime + '</div>' +
                    '<div class="card-body"><h5 class="card-title">' + data[i].user_name + '</h5>' + '<p class="card-text">' + data[i].message + '</p></div></div>');
            }
        },
        error: function(error) {
            console.log('ОШИБКА');
        },
    });
}

function accordionPassport() {
    $('#pointTabBody').on('click', 'tr', function(event) {
        var firstColumnValue = $(this).find('td:first-child').text();
        var clickedRow = $(this);

        $.ajax({
            url: '/get_accordion_passport/',
            method: 'POST',
            data: {
                'factoryMeter': firstColumnValue
            },
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                var results_passport = data.meter;
                var accordionRow = clickedRow.next('.accordion-row'); // Используем сохраненную ссылку на щелкнутую строку

                if (accordionRow.length) {
                    accordionRow.remove();
                } else {
                    $('.accordion-row').remove();
                    results_passport.forEach(function(result) {
                        clickedRow.after('<tr class="accordion-row"><td colspan="6">' +
                            '<div class="alert alert-primary" style="white-space: nowrap; text-align: justify;">' +
                            '<p style="display: inline;"><strong>Разрядность:</strong> ' + result.digit + '</p>' +
                            '<p style="display: inline;"><strong> Фазность:</strong> ' + result.phase + '</p>' +
                            '<p style="display: inline;"><strong> Напряжение:</strong> ' + result.voltage + '</p>' +
                            '<p style="display: inline;"><strong> Коэффициент трансформации:</strong> ' + result.tr_k + '</p>' +
                            '</div>' +
                            '</td></tr>'); // Используйте сохраненную ссылку на щелкнутую строку
                    });
                }
            }
        });
    });
}