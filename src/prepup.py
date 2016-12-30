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

    def get_questions(self):
        response.content_type = 'application/json;charset=utf-8'
        response.status = 400
        params = dict(request.POST)
        p_cat_id = params.get("cat_id", None)
        if p_cat_id is None:
            return json.dumps({"Error": "cat_id can't be null"})
        question_list = []
        try:
            _sql = """
                     select * from %s wher cat_id = %s
                      """ % 'question_mcq',p_cat_id
            results = self.pre_local.execute_query(_sql, 'select')
            if results is not None:
                for question_id, cat_id, qn_text, opt1, opt2, opt3, opt4, \
                    opt5, opt6, ans, tags, explanation in results:
                    question_data = {}
                    question_data['question_id'] = question_id
                    question_data['catId'] = cat_id
                    question_data['qn_text'] = qn_text
                    question_data['opt1'] = opt1
                    question_data['opt2'] = opt2
                    question_data['opt3'] = opt3
                    question_data['opt4'] = opt4
                    question_data['opt5'] = opt5
                    question_data['opt6'] = opt6
                    question_data['ans'] = ans
                    question_data['tags'] = tags
                    question_data['explanation'] = explanation
                    question_list.append(question_data)
        except Exception as e:
            return json.dumps({'status': str(e)})
        response_data = {}
        response_data['version'] = self.app_ver
        response_data['appId'] = self.app_id_pg
        response_data['questions'] = json.dumps(question_list)
        response.status = 200
        return json.dumps(response_data)
