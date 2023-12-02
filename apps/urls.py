# urls.py
from flask_restful import Api
from apps.resources import FormSubmission, loadReportTele

api = Api()

# Tambahkan sumber daya ke API

api.add_resource(FormSubmission, '/listData', endpoint='ListData'),
api.add_resource(FormSubmission, '/test/submit', endpoint='formsubmit_submit'),
api.add_resource(loadReportTele, '/loadReportTele', endpoint='loadReportTele')
