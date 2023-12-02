# resources.py
from flask import request, Response, jsonify
from flask_restful import Resource
from apps.model import  Model
from helper import send_message,getSysdateHour
import settings

class FormSubmission(Resource):
    def get(self):
        model_instance = Model()
        model_instance._table  = 'students'
        model_instance._select = 'fname,lname,pets,cprod'
        model_instance._where  = f"id ={44}"

        result = model_instance.loadGlobal()
        return result

    def post(self):
        model_instance = Model()

        data = {}
        data['fname']   = request.form['fname']
        data['lname']   = request.form['lname']
        data['pet']     = request.form['pets'] 
        
        result = model_instance.saveGlobal('students',data)
        return jsonify (result)
    
class loadReportTele(Resource):
    def get(self):
        tanggal = request.args.get('tanggal')
        jam = request.args.get('jam')
        storage = Model()
        storage._table  = 'ISURE_HISTORY_INET a LEFT JOIN ISURE_HISTORY_PCRF b ON a.ISUREID = b.ISUREID', 'ISURE_HISTORY_POTS','ISURE_HISTORY_IPTV','ISURE_HISTORY_ADDONS'
        storage._select = "COUNT(*) AS total,COUNT(CASE WHEN state = '2' THEN 1 END) AS total_sukses,COUNT(CASE WHEN state = '-1' THEN 1 END) AS total_inprogress,COUNT(CASE WHEN state != '2' THEN 1 END) AS total_error "
        if tanggal and jam:
            intervaljam = int(jam) - 3
            if intervaljam < 0:
                intervaljam = getSysdateHour(intervaltanggal=tanggal, jam=intervaljam)
            else:
                intervaljam = f'{tanggal} {intervaljam}'
            storage._where = f""" INSERT_TIME > TO_TIMESTAMP('{intervaljam[0]}:00:00', 'YYYY-MM-DD HH24:MI:SS')
                                AND INSERT_TIME < TO_TIMESTAMP('{tanggal} {jam}:00:00', 'YYYY-MM-DD HH24:MI:SS')
                                AND ACTION = '5' """
        else:
            jamSekarang = getSysdateHour()
            intervaljam = getSysdateHour(interval=3)
            storage._where = """ INSERT_TIME > TO_TIMESTAMP(to_char(SYSDATE - INTERVAL '3' HOUR,'YYYY-MM-DD HH24'),'YYYY-MM-DD HH24')
                                AND INSERT_TIME < TO_TIMESTAMP(to_char(SYSDATE,'YYYY-MM-DD HH24'),'YYYY-MM-DD HH24')
                                AND ACTION = '5' """

        
        data = storage.loadDataReport()

        if tanggal and jam:
            message_text = f"<b><u>Report Pengawalan Buka Isolir</u></b>\nPiloting Project I-SURE TREG-3\n\nPosisi pukul {intervaljam[0]}:00 - {jam}:00 :\n\n"
        else:
            jamSekarang = getSysdateHour()
            intervaljam = getSysdateHour(interval=3)
            message_text = f"<b><u>Report Pengawalan Buka Isolir</u></b>\nPiloting Project I-SURE TREG-3\n\nPosisi Hari ini pukul {intervaljam[0]}:00 - {jamSekarang[0]}:00 :\n\n"

        for result in data:
            produk = result["produk"]
            total_sukses = result["total_sukses"]
            total_inprogress = result["total_inprogress"]
            total_error = result["total_error"]

            success_icon = "✅"
            inprogress_icon = "🔄"
            failed_icon = "❌"
            detail_failed_icon = "🚫"  

            message_text += f"\n<b>{produk}</b>\n{success_icon} Success: {total_sukses}\n{inprogress_icon} On-Progress: {total_inprogress}\n{failed_icon} Failed: {total_error}"

            if total_error > 0:
                message_text += f"\n{detail_failed_icon} Detail Failed:\n"
                number = 1
                for detail in result['detail_error']:
                    if detail['info_error'] is not None:
                        info_error = detail['info_error']
                        message_text += f"         {number}. {info_error}\n"
                        number += 1
            else:
                message_text += "\n"

        # return jsonify(message_text)
        group_id = settings.GROUP_ID_TELEGRAM
        # group_id =-1001994152178

        result = send_message(text=message_text, chat_id=group_id, parse_mode='html') 
        if result.status_code == 200:
            return ({"message": "Sukses", "results": "T"}), 200
        else:
            return ({"message": "Error", "results": "F"}), 404
    
