import pymssql


class ulgesdbObjectPayment:
    '''
    Начисления по конкретному объекту
    '''
    def __init__(self):
        self.data_obj_payment = []

    def object_pay(self, id_dog, name_obj):
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        try:
            conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                   charset='cp1251')
            cursor = conn.cursor(as_dict=True)
            query = "select * from [dbo].[fn_GetAbnSchet] (%s,'20201001','20231031') WHERE NameObj = %s"
            cursor.execute(query, (id_dog.encode("cp1251"), name_obj.encode("cp1251")))
            for row in cursor:
                data_obj_p = {
                    'dtCalc': str(row['dtCalc'])[:-9],
                    'Tariff': row['Tariff'],
                    'Quantity': row['Quantity'],
                    'Summa': str(row['Summa'])[:-2]
                }

                self.data_obj_payment.append(data_obj_p)

            conn.close()
            print(self.data_obj_payment)
        except Exception as e:
            print('Ошибка запроса', e)

    def get_object_pay(self):
        return self.data_obj_payment


class ulgesdbAbnSchet:
    '''
    Счета начисления по котрагенту (общее)
    '''
    def __init__(self):
        self.data_abnschet = []

    def abn_schet(self, id_dogovor):
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        try:
            conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                   charset='cp1251')
            cursor = conn.cursor(as_dict=True)
            query = "select * from [dbo].[fn_GetAbnSchet] (%s,'20200101','20231231')"
            cursor.execute(query, id_dogovor)
            for row in cursor:
                data_abn = {
                    'dtCalc': str(row['dtCalc'])[:-9],
                    'NameObj': row['NameObj'],
                    'Tariff': row['Tariff'],
                    'Quantity': row['Quantity'],
                    'Summa': str(row['Summa'])[:-2]
                }

                self.data_abnschet.append(data_abn)

            conn.close()
        except Exception as e:
            print('Ошибка запроса', e)

    def get_data_abn(self):
        return self.data_abnschet


class ulgesdbMeterReadings:
    '''
    Показания приборов учета
    '''
    def __init__(self):
        self.data_meter_readings = []

    def meter_readings(self, meter_number):
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        try:
            conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                   charset='cp1251')
            cursor = conn.cursor(as_dict=True)
            print('Заводской номер - ', meter_number)
            query = "select * from [dbo].[fn_GetMeterReadings] (%s,'20200101', '20231231')"
            cursor.execute(query, meter_number)
            for row in cursor:
                data_meter = {
                    'NumberMeter': meter_number,
                    'DateAct': str(row['DateAct'])[:-9],
                    'Zone': row['Zone'],
                    'CurrValue': str(row['CurrValue'])[:-7],
                    'SizeKWT': row['SizeKWT'],
                    'DocType': row['DocType'],
                }

                self.data_meter_readings.append(data_meter)

            conn.close()
        except Exception as e:
            print('Ошибка запроса', e)

    def get_data_meter(self):
        return self.data_meter_readings


class ulgesbdexecute:
    '''
    работа с данными юриков и физиков???

    '''
    def __init__(self):
        self.data_agreement = None
        self.data_partner = None
        self.data_objects = []
        self.data_points = []

    def legal(self, innUser, numberDogUser, dataDogUser):
        flag = False
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        try:
            conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                   charset='cp1251')
            cursor = conn.cursor(as_dict=True)
            query = "SELECT * FROM [dbo].[fn_GetAbnObj] (%s,%s,%s)"
            cursor.execute(query, (innUser, numberDogUser, dataDogUser))
            if abs(cursor.rowcount) > 0:
                flag = True
                data_objects_id = []
                if abs(cursor.rowcount) > 0:
                    for row in cursor:
                        print("ID=%d,Name=%s Дата=%s АйдиДоговора=%s IDObject=%s" % (
                            row['idAbn'], row['NameAbn'], row['DogDate'], row['idDogovor'], row['idObj']))

                        self.data_partner = {
                            'idAbn': row['idAbn'],
                            'NameAbn': row['NameAbn'],
                            'INN': row['INN'],
                            'KPP': row['KPP'],
                            'PostAddress': row['PostAddress'],
                            'LegalAddress': row['LegalAddress'],
                            'CodeAbonent': row['CodeAbonent']
                        }

                        self.data_agreement = {
                            'idDogovor': row['idDogovor'],
                            'DogNumber': row['DogNumber'],
                            'DogDate': row['DogDate'],
                            'DateEnd': row['DateEnd'],
                            'TypeDog': row['TypeDog'],
                        }

                        data_object = {
                            'idObj': row['idObj'],
                            'NameObject': row['NameObject'],
                            'ObjectAddress': row['ObjectAddress'],
                            'is_active': 1 if row['ObjectEnd'] is None else 0
                        }

                        self.data_objects.append(data_object)
                        data_objects_id.append(row['idObj'])
                else:
                    print("Ошибка")
                conn.close()
                conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                       charset='cp1251')
                cursor = conn.cursor(as_dict=True)
                query = "SELECT * FROM [dbo].[fn_GetPointMeter] (%s)"
                for item in data_objects_id:
                    cursor.execute(query, (item,))
                    result = cursor.fetchall()

                    for row in result:
                        data_point = {
                            'idPoint': row['idPoint'],
                            'idObj': item,
                            'Location': row['Location'],
                            'PointBegin': row['PointBegin'],
                            'PointEnd': row['PointEnd'],
                            'NumberPoint': row['NumberPoint'],
                            'idPointReg': row['idPointReg'],
                            'NumberMeter': row['NumberMeter'],
                            'MarkMeter': row['MarkMeter'],
                            'Digit': row['Digit'],
                            'Phase': row['Phase'],
                            'Voltage': row['Voltage'],
                            'TR_K': row['TR_K'],
                            'DateEnd': row['DateEnd'],
                            'MeterInterval': row['MeterInterval'],
                            'DateBegin': row['DateBegin'],
                            'DateCheck': row['DateCheck'],
                            'Trans': row['Trans'],
                            'TransPrimary': row['TransPrimary'],
                            'TransSecondary': row['TransSecondary'],
                            'TransType': row['TransType'],
                            'TransPrecision': row['TransPrecision'],
                            'TransInterval': row['TransInterval'],
                        }

                        self.data_points.append(data_point)
            else:
                print("Ошибка - неверные параметры", cursor.rowcount)
                print("SQL: ", query)
        except Exception as e:
            print(f"Ошибка: {e}")
        return flag

    def individual(self, numberDogUser):
        flag = False
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        try:
            conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                   charset='cp1251')
            cursor = conn.cursor(as_dict=True)
            query = "SELECT * FROM [dbo].[fn_GetAbnObj_Private] (%s)"
            cursor.execute(query, numberDogUser)
            if abs(cursor.rowcount) > 0:
                flag = True
                data_objects_id = []
                if abs(cursor.rowcount) > 0:
                    for row in cursor:
                        print("ID=%d,Name=%s IDObject=%s" % (
                            row['idAbn'], row['NameAbn'], row['idObj']))

                        self.data_partner = {
                            'idAbn': row['idAbn'],
                            'NameAbn': row['NameAbn'],
                            'CodeAbonent': row['CodeAbonent']
                        }

                        data_object = {
                            'idObj': row['idObj'],
                            'NameObject': row['NameObject'],
                            'ObjectAddress': row['ObjectAddress'],
                            'is_active': row['isActive'],
                        }

                        self.data_objects.append(data_object)
                        data_objects_id.append(row['idObj'])
                else:
                    print("Ошибка")
                conn.close()
                conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                                       charset='cp1251')
                cursor = conn.cursor(as_dict=True)
                query = "SELECT * FROM [dbo].[fn_GetPointMeter] (%s)"
                for item in data_objects_id:
                    cursor.execute(query, (item,))
                    result = cursor.fetchall()

                    for row in result:
                        data_point = {
                            'idPoint': row['idPoint'],
                            'idObj': item,
                            'Location': row['Location'],
                            'PointBegin': row['PointBegin'],
                            'PointEnd': row['PointEnd'],
                            'NumberPoint': row['NumberPoint'],
                            'idPointReg': row['idPointReg'],
                            'NumberMeter': row['NumberMeter'],
                            'MarkMeter': row['MarkMeter'],
                            'Digit': row['Digit'],
                            'Phase': row['Phase'],
                            'Voltage': row['Voltage'],
                            'TR_K': row['TR_K'],
                            'DateEnd': row['DateEnd'],
                            'MeterInterval': row['MeterInterval'],
                            'DateBegin': row['DateBegin'],
                            'DateCheck': row['DateCheck'],
                            'Trans': row['Trans'],
                            'TransPrimary': row['TransPrimary'],
                            'TransSecondary': row['TransSecondary'],
                            'TransType': row['TransType'],
                            'TransPrecision': row['TransPrecision'],
                            'TransInterval': row['TransInterval'],
                        }

                        self.data_points.append(data_point)
                        print(self.data_points)
            else:
                print("Ошибка - неверные параметры", cursor.rowcount)
                print("SQL: ", query)
                conn.close()
        except Exception as e:
            print(f"Ошибка: {e}")
        return flag

    def get_data_ulges(self):
        return self.data_partner, self.data_agreement, self.data_objects, self.data_points
