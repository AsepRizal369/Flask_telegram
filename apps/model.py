# model.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from apps import app
from sqlalchemy import text

class Model:
    def __init__(self, _connection=None):
        self._connection = 'default'
        self._table = None
        self._where = None
        self._select = None

        if _connection:
            self._connection = _connection

    def saveGlobal(self, table_name, obj, sequence_name=None):
        try:
            columns = ", ".join(obj.keys())
            placeholders = ", ".join(":" + key for key in obj.keys())
            values = obj

            formatted_sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id")

            # Membuka koneksi
            with Config.engine_pg.connect() as connection:
                # Eksekusi query SQL
                result = connection.execute(formatted_sql, values)
                connection.commit()

                # Mengambil nilai yang baru saja dimasukkan
                inserted_id = result.scalar()


                return {'info': 'success', 'code': 0, 'data': inserted_id}

        except Exception as e:
            # Rollback jika terjadi kesalahan
            raise e
        
    def loadGlobal(self):
        connection = Config.engine_pg.connect()
        formatted_sql = text(f"select * from {self._table} ")
        result = connection.execute(formatted_sql)
        
        json_result=[]
        for row in result:
            row_dict = {
                'ID': row[0],
                'Column1': row[1],
                'Column2': row[2],
                'Column3': row[3],
            }
            json_result.append(row_dict)
        return json_result

        # db.session.add(data)
        # db.session.commit()

    # def getStudentById(self, dataId):
    #     return Student.query.filter_by(id=dataId).first()

# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True)
#     fname = db.Column(db.String(40))
#     lname = db.Column(db.String(40))
#     pet = db.Column(db.String(40))

#     def __init__(self, fname, lname, pet):
#         self.fname = fname
#         self.lname = lname
#         self.pet = pet


    def loadDataReport(self):
        connection = Config.engine_oracle.connect()
        queries1 = []
        queries2 = []

        for table in self._table:
            if table == 'ISURE_HISTORY_INET a LEFT JOIN ISURE_HISTORY_PCRF b ON a.ISUREID = b.ISUREID':
                produk = "INET"
            elif table == 'ISURE_HISTORY_POTS':
                produk = "POTS"
            elif table == 'ISURE_HISTORY_IPTV':
                produk = "IPTV"
            elif table == 'ISURE_HISTORY_ADDONS':
                produk = "ADDONS"

            if produk == 'INET':
                sql1 = f"SELECT '{produk}' as produk,COUNT(*) AS total,COUNT(CASE WHEN b.state = '2' THEN 1 END) AS total_sukses,COUNT(CASE WHEN b.state = '-1' THEN 1 END) AS total_inprogress,COUNT(CASE WHEN b.state != '2' THEN 1 END) AS total_error FROM {table} WHERE a.INSERT_TIME > TO_TIMESTAMP(to_char(SYSDATE - INTERVAL '3' HOUR, 'YYYY-MM-DD HH24'), 'YYYY-MM-DD HH24')AND a.INSERT_TIME < TO_TIMESTAMP(to_char(SYSDATE, 'YYYY-MM-DD HH24'), 'YYYY-MM-DD HH24')AND a.ACTION = '5'"
                subquery = f"SELECT '{produk}' as produk,b.PCRF_INFO AS info_error,count(*) AS jumlah FROM {table} WHERE a.INSERT_TIME > TO_TIMESTAMP(to_char(SYSDATE - INTERVAL '3' HOUR, 'YYYY-MM-DD HH24'), 'YYYY-MM-DD HH24')AND a.INSERT_TIME < TO_TIMESTAMP(to_char(SYSDATE, 'YYYY-MM-DD HH24'), 'YYYY-MM-DD HH24')AND a.ACTION = '5' AND b.state = 4 GROUP BY b.PCRF_INFO"
            else:
                sql1 = f"SELECT '{produk}' as produk,{self._select} FROM {table} WHERE {self._where}  "
                subquery = f"SELECT '{produk}' as produk,CASE WHEN SUBSTR(MESSAGE_BACKEND, 1, INSTR(MESSAGE_BACKEND, ':') - 1)= 'No such user id' THEN 'No such user id : ND' WHEN REGEXP_SUBSTR(MESSAGE_BACKEND, 'org\.codehaus\.jackson\.JsonParseException', 1, 1) ='org.codehaus.jackson.JsonParseException' THEN 'org.codehaus.jackson.JsonParseException' ELSE MESSAGE_BACKEND END AS info_error, count(*) AS jumlah FROM {table} WHERE {self._where} AND state = 4 GROUP BY MESSAGE_BACKEND"
            
            queries1.append(sql1)
            queries2.append(subquery)

        combined_query1 = " UNION ALL ".join(queries1)
        combined_query2 = " UNION ALL ".join(queries2)
        
        mainquery = f"""SELECT
                            produk,
                            INFO_ERROR
                        FROM
                            ({combined_query2})
                        GROUP BY 
                            produk,info_error"""
        
        # Eksekusi query SQL langsung menggunakan Flask SQLAlchemy
        sql1 = connection.execute(text(combined_query1))
        dataDetail = [{'produk': row[0], 'total': row[1], 'total_sukses': row[2], 'total_inprogress': row[3], 'total_error': row[4]} for row in sql1.fetchall()]
        
        sql2 = connection.execute(text(mainquery))
        dataDetailError = dataDetailError = [{'produk': row[0], 'info_error': row[1]} for row in sql2.fetchall()]

        result = []
        for item in dataDetail:
            produk = item['produk']
            total = item['total']
            total_sukses = item['total_sukses']
            total_inprogress = item['total_inprogress']
            total_error = item['total_error']
            errorDetail = []
            for detail_Error in dataDetailError:
                if detail_Error['produk'] == produk:
                    resultdetail = {
                        'info_error': detail_Error['info_error']
                        # 'jumlah'            :detail_Error['jumlah']
                    }
                    errorDetail.append(resultdetail)

            resultDetail = {
                'produk': produk,
                'total': total,
                'total_sukses': total_sukses,
                'total_inprogress': total_inprogress,
                'total_error': total_error,
                'detail_error': errorDetail
            }
            result.append(resultDetail)
        return result
