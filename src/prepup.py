from bottle import request, response
import requests
import urllib
import json
import datetime
from pre_storage import PreLocal
from bottle import request, response
from config import prepup_data

prepup = prepup_data()

class PgData(object):
    def __init__(self):
        self.video_url = ""
        self.pre_local = PreLocal()
        self.app_ver = prepup.appVersion
        self.app_id_pg = 'prepupProgramming'

    def get_categories(self):
         response.content_type = 'application/json;charset=utf-8'
         response.status = 400
         category_list = []
         try:
              _sql = """
                     select cat_id, cat_name from %s
                      """ % 'categories'
              results = self.pre_local.execute_query(_sql, 'select')
              if results is not None:
                  for cat_id, cat_name in results:
                      categ_data = {}
                      categ_data['catId'] = cat_id
                      categ_data['catName'] = cat_name
                      category_list.append(categ_data)
         except Exception as e:
                    return json.dumps({'status': str(e)})
         response_data = {}
         response_data['version'] = self.app_ver
         response_data['appId'] = self.app_id_pg
         response_data['categories'] = json.dumps(category_list)
         response.status = 200
         return json.dumps(response_data)

