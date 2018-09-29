# -*- coding: utf-8 -*-


import re
from flask import request
from flask_restful import Resource
from bulldog.models import find_jobs


class JobInfo(Resource):

    def get(self):
        data = {"c": -1, "datas": [], "msg": "Error"}
        condition = request.args.get('query-condition', '')
        if not condition:
            return data

        condition = condition.replace(' ', '')
        # 解析查询条件
        relation = "$and"
        if '-' in condition:
            conditions = condition.split('-')
        elif '|' in condition:
            conditions = condition.split('|')
            relation = "$or"
        else:
            print('fuck')
            return data

        try:
            query = dict(c.split(':') for c in conditions)
        except Exception as e:
            print(e)
            return data

        mongo_condition = self.struct_mongo_query(relation, query)
        data['c'] = 0
        for j in find_jobs(mongo_condition).limit(50):
            data['datas'].append({
                "city": j['city'],
                "position": j['positionName'],
                "company": j['companyFullName'],
                "logo": 'https://www.lagou.com/{}'.format(j['companyLogo']),
                "url": 'https://www.lagou.com/jobs/{}.html'.format(j['positionId']),
            })

        return data

    def struct_mongo_query(self, relation, query_dict):
        mongo_condition = {}
        if 'city' in query_dict:
            mongo_condition['city'] = query_dict.pop('city', 'guangzhou')

        mongo_condition[relation] = []
        for k, v in query_dict.items():
            if k in {"position", "company", "addr"}:
                re_value = re.compile('.*{}.*'.format(v), re.IGNORECASE)
                mongo_condition[relation].append({
                    self.change_db_key(k): re_value
                })
            else:
                mongo_condition[relation].append({
                    self.change_db_key(k): v
                })

        return mongo_condition

    def change_db_key(self, name):
        name_2_Mongo_key = {
            "addr": "address",
            "district": "district",
            "company": "companyFullName",
            "position": "positionName",
        }
        return name_2_Mongo_key.get(name, '')
