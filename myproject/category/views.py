from django.shortcuts import render
from category import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(__file__).upper()))
# Create your views here.
from account import models as a_model
from Tools import authenticate
from copy import deepcopy

def create_deafault_category(request):
    if request.method == 'POST':
        try:
            models.category.objects.create(user_id=None,
                                        category_name='Salary',
                                        source_type='income',
                                        category_icon_name='IncomeOne')
            models.category.objects.create(user_id=None,
                                        category_name='Financing',
                                        source_type='income',
                                        category_icon_name='financing')
            models.category.objects.create(user_id=None,
                                        category_name='Bonus',
                                        source_type='income',
                                        category_icon_name='financing-one')

            models.category.objects.create(user_id=None,
                                        category_name='Utilities',
                                        source_type='expense',
                                        category_icon_name='WaterRateTwo')
            models.category.objects.create(user_id=None,
                                        category_name='Housing',
                                        source_type='expense',
                                        category_icon_name='Application')
            models.category.objects.create(user_id=None,
                                        category_name='Transportation',
                                        source_type='expense',
                                        category_icon_name='BusTwo')
            models.category.objects.create(user_id=None,
                                        category_name='Medical Expense',
                                        source_type='expense',
                                        category_icon_name='Hospital')
            models.category.objects.create(user_id=None,
                                        category_name='Food',
                                        source_type='expense',
                                        category_icon_name='KnifeFork')
            models.category.objects.create(user_id=None,
                                        category_name='Travel',
                                        source_type='expense',
                                        category_icon_name='Journey')
            models.category.objects.create(user_id=None,
                                        category_name='Entertainment',
                                        source_type='expense',
                                        category_icon_name='Theater')
            models.category.objects.create(user_id=None,
                                        category_name='Telephone',
                                        source_type='expense',
                                        category_icon_name='Intercom')
            return HttpResponse('Successfully Created!')
        except:
            return HttpResponse('Not Successful!')


@csrf_exempt
def add(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        user_id = a_model.User.objects.get(username = cur_username).id
        json_param = json.loads(request.body.decode())

        category_name = json_param['category_name']
        source_type = json_param['source_type']
        category_icon_name = json_param['category_icon_name']

        try:
            models.category.objects.create(
                user_id = user_id,
                category_name = category_name,
                source_type = source_type,
                category_icon_name = category_icon_name)
            res = {'code':200, 'msg':'Successful!', 'data':None}
        except Exception as e:
            # print(e)
            res = {'code':400, 'msg':'Not Successful','data':None}
        finally:
            return HttpResponse(json.dumps(res), status=res['code'])

def fetch_all(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        user_id = a_model.User.objects.get(username = cur_username).id
        try:
            exsited_category = models.category.objects.filter(id__range=[1,12])
            category = {}
            for e in exsited_category:
                category[e.id] = {
                    'category_name':e.category_name,
                    'category_type':e.source_type,
                    'category_icon_name':e.category_icon_name
                }
            users_category = models.category.objects.filter(user_id = user_id)
            for e in users_category:
                category[e.id] = {
                    'category_name':e.category_name,
                    'category_type':e.source_type,
                    'category_icon_name':e.category_icon_name
                }
            res = {'code':200, 'msg':'Successful','data':category}
        except Exception as e:
            print(e)
            res = {'code':400, 'msg':'Not successful','data':None}
        finally:
            return HttpResponse(json.dumps(res), status=res['code'])

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        category_id = json.loads(request.body.decode())['id']
        try:
            fetch = models.category.objects.get(id = category_id)
            fetch.delete()
            res = {'code':200, 'msg':'Successful', 'data':None}
        except Exception as e:
            print(e)
            res = {'code': 406, 'msg':'Failed to delete or the record has been deleted, please try again.', 'data': None}
        finally:
            return HttpResponse(json.dumps(res), status=res['code'])

