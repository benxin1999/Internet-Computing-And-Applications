from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bill import models as b_model
from account import  models as a_model
from category import  models as c_model
from django.views.decorators.csrf import csrf_exempt
import time
import json
from copy import deepcopy
from collections import defaultdict


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__).upper()))
from Tools import records
from Tools import authenticate
# Create your views here.

@csrf_exempt
def add(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        json_param = json.loads(request.body.decode())
        source_type = json_param['source_type']
        bill_amount = json_param.get('bill_amount', 0)
        category_id = json_param['category_id']
        category_name = c_model.category.objects.get(id = category_id).category_name
        bill_remark = json_param.get('bill_remark',None)
        bill_date = json_param['bill_date']
        category_icon_name = c_model.category.objects.get(id = category_id).category_icon_name

        user_id = a_model.User.objects.get(username = cur_username).id
        try:

            b_model.Bill.objects.create(user_id = user_id ,
                                        source_type = source_type,
                                        bill_amount = bill_amount,
                                        category_id = category_id,
                                        category_name = category_name,
                                        bill_remark = bill_remark,
                                        bill_date = bill_date,
                                        category_icon_name = category_icon_name )

            msg = 'Successfully created!'
            res = {'code':200, 'msg':msg, 'data':None}
        except Exception as e:
            print(e)
            msg = 'Falied to create, please try again!'
            res = {'code': 200, 'msg': msg, 'data': None}
        finally:
            return HttpResponse(json.dumps(res), status=res['code'])

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        json_param = json.loads(request.body.decode())
        bill_id = json_param['id']


        try:
            delete = b_model.Bill.objects.get(id=bill_id)
            delete.delete()
            msg = 'Successfully deleted!'
            code = 200
        except:
            msg = 'Failed to delete or the record has been deleted, please try again.'
            code = 406
        finally:
            res = {'code':code, 'msg':msg, 'data':None}
            return HttpResponse(json.dumps(res), status=res['code'])


def fetch_one(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        bill_id = request.GET.get('id',None)
        try:
            fetch = b_model.Bill.objects.get(id=bill_id)
            user_id = a_model.User.objects.get(username = cur_username).id
            data = records.extract_bill(fetch)
            data.pop('category_icon_name')
            data['user_id'] = user_id
            msg = 'Successful!'
            code = 200
        except Exception as e:
            print(e)
            msg = 'Cannot find the bill.'
            code = 406
            data = None
        finally:
            res = {'msg':msg, 'data':data, 'code':code,}
            return HttpResponse(json.dumps(res), status=res['code'])


@csrf_exempt
def get_bill_lists(request):
    if request.method == 'GET':
        #authenication
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        try:
            user_id = a_model.User.objects.get(username=cur_username).id
            time = request.GET.get('filterBillDate') #timestamp
            # category_id = request.GET.get('category_id') #int

            s, e = records.time_period(time)
            ans = b_model.Bill.objects.filter(user_id=user_id, bill_date__range=[s, e]).order_by('bill_date')
            # if category_id == 'all':
            #     ans = b_model.Bill.objects.filter(user_id = user_id,bill_date__range = [s, e]).order_by('bill_date')
            # else:
            #     ans = b_model.Bill.objects.filter(user_id=user_id, bill_date__range=[s, e], category_id=category_id).order_by('bill_date')
            today = {'date':'', 'income':[],'expense':[]}
            bill_lists = []
            for e in ans:
                if today['date'] != records.date(e.bill_date):
                    bill_lists += [deepcopy(today)]
                    today.clear()

                    today['date'] = records.date(e.bill_date)
                    today['expense'], today['income'] = [], []
                    info  = records.extract_bill(e)
                    if info['source_type'] == 'income':
                        today['income'].append(info)
                    else:
                        today['expense'].append(info)
                else:
                    info = records.extract_bill(e)
                    if info['source_type'] == 'income':
                        today['income'].append(info)
                    else:
                        today['expense'].append(info)
            bill_lists.append(deepcopy(today))
            if len(bill_lists)!=0:
                bill_lists.pop(0)
            #calculate total
            income, expense = records.details(ans)
            data ={'totalExpense':expense,'totalIncome':income, 'dataMap':bill_lists}
            res = {'code':200, 'msg':'Successful!','data':data}
            return HttpResponse(json.dumps(res), status=res['code'])
        except Exception as e :
            print(e)
            res ={'code':400, 'msg':' Not Successful!'}
            return HttpResponse(json.dumps(res),status=res['code'])

@csrf_exempt
def update(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)

        json_param = json.loads(request.body.decode())
        bill_id = json_param['id']
        source_type = json_param['source_type']
        bill_amount = json_param['bill_amount']
        category_id = json_param['category_id']
        category_name = c_model.category.objects.get(id = category_id).category_name
        bill_date = json_param['bill_date']
        user_id = json_param['user_id']
        bill_remark = json_param['bill_remark']

        try:
            update = b_model.Bill.objects.get(id = bill_id)
            update.source_type = source_type
            update.bill_amount = bill_amount
            update.category_id = category_id
            update.category_type = category_name
            update.bill_date = bill_date
            update.bill_remark = bill_remark
            update.category_icon_name = c_model.category.objects.get(id = category_id).category_icon_name
            update.save()
            res = {'code':200, 'msg':'Successful!'}
            return HttpResponse(json.dumps(res), status=res['code'])
        except Exception as e:
            print(e)
            res = {'code': 400, 'msg': 'Not Successful!'}
            return HttpResponse(json.dumps(res), status=res['code'])


def create_category(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not authenticate.authenticate(token):
            return HttpResponse('No Permission, please log in!')
        cur_username = authenticate.authenticate(token)






