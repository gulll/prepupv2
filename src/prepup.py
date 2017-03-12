from bottle import request, response
import requests
import urllib
import time
import json
import datetime
from pre_storage import PreLocal
from bottle import request, response
from config import prepup_data
import cgi
from random import shuffle

prepup = prepup_data()


class PgData(object):
    def __init__(self):
        self.video_url = ""
        self.pre_local = PreLocal()
        self.app_ver = prepup.appVersion
        self.app_id_pg = 'prepupProgramming'

    def serialize(self, obj):
    	if isinstance(obj, datetime.datetime):
            return str(obj.strftime("%Y-%m-%d %H:%M:%S"))
   	elif isinstance(obj, datetime.date):
            return str(obj.strftime("%Y-%m-%d"))
        return json.JSONEncoder.default(obj)

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
        response_data['categories'] = category_list
        response.status = 200
        return json.dumps(response_data)

    def get_articles(self):
        response.content_type = 'application/json;charset=utf-8'
        response.status = 400
        params = dict(request.POST)
        pCatId = params.get("catId", None)
        if pCatId is None:
            return json.dumps({"Error": "catId can't be null"})
        pLimit = int(params.get("limit", 20))
        pStartAt = int(params.get("startAt", 0))
        question_list = []
        try:
            _sql = """
                     select * from %s where cat_id = %s limit %d, %d
                      """ % ('articles', pCatId, pStartAt, pLimit)
            results = self.pre_local.execute_query(_sql, 'select')
            if results is not None:
                for article_id, cat_id, article_text, timestamp in results:
                    article_data = {}
                    article_data['questionId'] = article_id
                    article_data['catId'] = cat_id
                    article_data['qnText'] = "ARTICLE DAALTA HOON BAD ME"
                    article_data['ans'] = 0
                    article_data['tags'] = "FUCK"
                    article_data['qnType'] = "ARTICLE"
                    article_data['opts'] = []
                    article_data['explanation'] = cgi.escape(article_text).decode('utf-8',errors='ignore').encode('ascii', 'xmlcharrefreplace')
                    article_data['cDate'] = time.mktime(timestamp.timetuple())*1000
                    article_data['extLink'] = "WWW.PORNHUB.COM"
                    question_list.append(article_data)
        except Exception as e:
            return json.dumps({'status': str(e)})
        response_data = {}
        response_data['version'] = self.app_ver
        response_data['appId'] = self.app_id_pg
        response_data['questions'] = question_list
        response.status = 200
        return json.dumps(response_data, default=self.serialize)

    def get_questions(self):
        response.content_type = 'application/json;charset=utf-8'
        response.status = 400
        params = dict(request.POST)
        pCatId = params.get("catId", None)
        if pCatId is None:
            return json.dumps({"Error": "catId can't be null"})
        pLimit = int(params.get("limit", 10))
        pStartAt = int(params.get("startAt", 0))
        question_list = []
        limitQn = pLimit*3/4
        limitAr = pLimit - limitQn
        startQn = pStartAt*3/4
        startAr = pStartAt - startQn
        try:
            _sql = """
                     select * from %s where cat_id = %s limit %d, %d
                      """ % ('question_mcq', pCatId, startQn, limitQn)
            results = self.pre_local.execute_query(_sql, 'select')
            if results is not None:
                for question_id, cat_id, qn_text, opt1, opt2, opt3, opt4, \
                    opt5, opt6, ans, tags, explanation, extLink, timestamp, qnType in results:
                    question_data = {}
                    question_data['questionId'] = question_id
                    question_data['catId'] = cat_id
                    question_data['qnText'] = qn_text
                    opts = []
                    if opt1 is not None:
                        opts.append(opt1)
                    if opt2 is not None:
                        opts.append(opt2)
                    if opt3 is not None:
                        opts.append(opt3)
                    if opt4 is not None:
                        opts.append(opt4)
                    if opt5 is not None:
                        opts.append(opt5)
                    if opt6 is not None:
                        opts.append(opt6)
                    question_data['opts'] = opts
                    question_data['ans'] = ans
                    question_data['tags'] = tags
                    question_data['explanation'] = explanation
                    question_data['extLink'] = extLink
                    question_data['qnType'] = qnType
                    question_data['cDate'] = time.mktime(timestamp.timetuple())*1000
                    question_list.append(question_data)
        except Exception as e:
            return json.dumps({'status': str(e)})
        try:
            _sql = """
                     select * from %s where cat_id = %s limit %d, %d
                      """ % ('articles', pCatId, startAr, limitAr)
            results = self.pre_local.execute_query(_sql, 'select')
            if results is not None:
                for article_id, cat_id, article_text, timestamp, preview_text in results:
                    article_data = {}
                    article_data['questionId'] = article_id
                    article_data['catId'] = cat_id
                    article_data['qnText'] = "ARTICLE DAALTA HOON BAD ME"
                    article_data['ans'] = 0
                    article_data['tags'] = "FUCK"
                    article_data['qnType'] = "ARTICLE"
                    article_data['opts'] = []
                    article_data['explanation'] = cgi.escape(article_text).decode('utf-8',errors='ignore').encode('ascii', 'xmlcharrefreplace')
                    article_data['cDate'] = time.mktime(timestamp.timetuple())*1000
                    article_data['extLink'] = "WWW.PORNHUB.COM"
                    article_data['previewText'] = preview_text
                    question_list.append(article_data)
        except Exception as e:
            return json.dumps({'status': str(e)})
        shuffle(question_list)
        response_data = {}
        response_data['version'] = self.app_ver
        response_data['appId'] = self.app_id_pg
        response_data['questions'] = question_list
        response.status = 200
        return json.dumps(response_data, default=self.serialize)
