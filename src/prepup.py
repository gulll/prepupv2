from bottle import request, response
import requests
import urllib
import json
import datetime
from pre_storage import PreLocal


class PgData(object):
    def __init__(self):
        self.video_url = ""
        self.pre_local = PreLocal()

    def get_categories(self):
         category_list = []
         try:
              _sql = """
                     select cat_id, cat_name from %s
                      """ % 'categories'
              results = self.pre_local.execute_query(_sql, 'select')
              if results is not None:
                  for cat_id, cat_name in results:
                      response_data = {}
                      response_data['cat_id'] = cat_id
                      response_data['cat_name'] = cat_name
                      category_list.append(response_data)
                  return json.dumps(category_list)
         except Exception as e:
                    return json.dumps({'status': str(e)})

