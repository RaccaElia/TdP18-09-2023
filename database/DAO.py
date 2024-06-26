from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year(gds.Date)) as anno
                    from go_sales.go_daily_sales gds """

        cursor.execute(query, )

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(gr.Country)
                from go_sales.go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append((row["Country"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_sales.go_retailers gr 
                where gr.Country = %s"""

        cursor.execute(query, (nazione, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArco(anno, ret1, ret2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct(gds.Product_number)) as num, gds2.Retailer_code as ret2, gds.Retailer_code as ret
                from go_sales.go_daily_sales gds, go_sales.go_daily_sales gds2
                where year(gds2.Date)=%s and year(gds.Date)=%s and gds2.Product_number = gds.Product_number
                and gds.Retailer_code = %s and gds2.Retailer_code = %s
                group by gds.Retailer_code, gds2.Retailer_code """

        cursor.execute(query, (anno, anno, ret1, ret2))

        for row in cursor:
            result = [row["num"], (row["ret"], row["ret2"])]

        cursor.close()
        conn.close()
        return result