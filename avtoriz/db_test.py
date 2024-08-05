import pymssql


class ulgesbd:
    def main():
        server = '192.168.1.43'
        user = 'as'
        password = '1'
        conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                               charset='cp1251')
        cursor = conn.cursor(as_dict=True)
        data_objects = []
        data_objects_id = []
        data_points = []
        query = "SELECT * FROM [dbo].[fn_GetAbnObj](%s,%s,%s)"
        cursor.execute(query, ('7325082136', 4044, '20130701'))
        if abs(cursor.rowcount) > 0:
            for row in cursor:
                print("ID=%d,Name=%s Дата=%s АйдиДоговора=%s IDObject=%s" % (
                    row['idAbn'], row['NameAbn'], row['DogDate'], row['idDogovor'], row['idObj']))

                data_partner = {
                    'idAbn': row['idAbn'],
                    'NameAbn': row['NameAbn'],
                    'INN': row['INN'],
                    'KPP': row['KPP'],
                    'PostAddress': row['PostAddress'],
                    'LegalAddress': row['LegalAddress'],
                    'CodeAbonent': row['CodeAbonent']
                }

                data_agreement = {
                    'idDogovor': row['idDogovor'],
                    'DogNumber': row['DogNumber'],
                    'DogDate': row['DogDate'],
                    'DateEnd': row['DateEnd'],
                    'TypeDog': row['TypeDog']
                }

                data_object = {
                    'idObj': row['idObj'],
                    'NameObject': row['NameObject'],
                    'ObjectAddress': row['ObjectAddress'],
                    'isActive': 1 if row['ObjectEnd'] is None else 0
                }

                data_objects.append(data_object)
                data_objects_id.append(row['idObj'])
                print(data_object)

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
                print(
                    "idТочкиУльГЭС=%s,   Вольтаж=%s,   МесторасположенияТУ=%s,   Дата_Нач=%s,   Дата_конец=%s "
                    "Имя_ТУ=%s ,, IDПУ=%s, ЗаводскойНомер=%s, Марка=%s, ДатаУстановки=%s, ДатаПоверки=%s, Транс=%s, "
                    "ТрансПримари=%s" % (
                        row['idPoint'], row['Voltage'], row['Location'], row['PointBegin'], row['PointEnd'],
                        row['NumberPoint'], row['idPointReg'], row['NumberMeter'], row['MarkMeter'], row['DateBegin'],
                        row['DateCheck'], row['Trans'], row['TransPrimary']))
                data_point = {
                    'idPoint': row['idPoint'],
                    'idObj': item,
                    'Voltage': row['Voltage'],
                    'Location': row['Location'],
                    'PointBegin': row['PointBegin'],
                    'PointEnd': row['PointEnd'],
                    'NumberPoint': row['NumberPoint'],
                    # ПриборУчета
                    'idPointReg': row['idPointReg'],
                    'NumberMeter': row['NumberMeter'],
                    'MarkMeter': row['MarkMeter'],
                    'DateBegin': row['DateBegin'],
                    'DateCheck': row['DateCheck'],
                    # Трансформатор
                    'Trans': row['Trans'],
                    'TransPrimary': row['TransPrimary'],
                    'TransSecondary': row['TransSecondary'],
                    'TransType': row['TransType'],
                    'TransPrecision': row['TransPrecision'],
                    'TransInterval': row['TransInterval'],

                }
                data_points.append(data_point)
                # print("\n\n", data_points)

        conn.close()
        conn = pymssql.connect(host=server, user=user, password=password, database="GES", tds_version=r'7.0',
                               charset='cp1251')
        cursor = conn.cursor(as_dict=True)
        query = "select * from [dbo].[fn_GetAbnSchet] (1929,'20231001','20231031')"
        cursor.execute(query)
        for row in cursor:
            print(
                "Дата начисления=%s,id объекта=%s ,номер объекта=%s , Название=%s, Тариф=%s, Количество=%s, Сумма=%s" % (
                    row['dtCalc'], row['idObj'], row['NumberObj'], row['NameObj'], row['Tariff'], row['Quantity'],
                    row['Summa']))

    #
    # def get_data_ulges(self):
    #     return self.data_partner, self.data_agreement, self.data_objects, self.data_point

    if __name__ == "__main__":
        main()
# SELECT * FROM [dbo].[fn_GetAbnObj_Private] (100407300)
# SELECT * FROM [dbo].[fn_GetAbnObj] ('7325082136',4044,'20130701')
# SELECT * FROM [dbo].[fn_GetPointMeter] (1871957)
