from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from account import models
import json
import jwt
import time
import os
import sys
sys.path.append(os.path.dirname(__file__).upper())
from Tools import authenticate

# Create your views here.

def index(request):
    return render(request, 'test.html')


# def calc_md5(password):
#     md5_obj = hashlib.md5()
#     md5_obj.update(password.encode('utf-8'))
#     return md5_obj.hexdigest()

# def password_is_valid(password):
#     if len(password)>15 or len(password)<5:
#         return False
#     return password.isalnum()




@csrf_exempt
def signup(request):
    if request.method == 'POST':
        json_param = json.loads(request.body.decode())
        username = json_param.get('username',None)
        password = json_param['password']
        try:
            user = models.User.objects.get(username=username)
            code = 400
            msg = 'The username existed, please try another!'
        except:
            try:
                if len(username) < 8 or len(username) > 15 or password == None:
                    raise NameError
                else:
                    try:
                        if authenticate.password_is_valid(password):
                            slogon = 'To learn and to apply, for the benefit of mankind.'
                            models.User.objects.create(username=username, password=authenticate.calc_md5(password), slogon=slogon)
                            code = 200
                            msg = 'Account created successfully!'
                        else:
                            raise ValueError
                    except:
                        code = 400
                        msg = 'The length of the password should be between 5 and 15. Only uppercase letters, lowercase letters and numbers are accepted.'

            except:
                code = 400
                msg = 'The username length should be more than 8 but less than 15 characters and password cannot be null. '
        un = username

        res = {'code': code, 'message': msg, 'username': un, 'data': None}
    print(res)
    return HttpResponse(json.dumps(res), status=res['code'])


# JWT token generation & verification

# def get_jwt_token(username):
#     payload = {
#         'exp': int(time.time()) + 60 * 180,
#         'iat': int(time.time()),
#         'data': {'username': username}
#     }
#     encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256')
#     return encoded_jwt


# def verify_jwt_token(token):
#     try:
#         _payload = jwt.decode(token, 'secret', algorithms='HS256')
#     except jwt.PyJWTError:
#         print('Not match!')
#         return {'res': False}
#     else:
#         exp = int(_payload.pop('exp'))
#
#         if time.time() > exp:
#             print('Out of time!')
#             return {'res': False}
#         return {'res': True, 'user': _payload['data']['username']}


@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_param = json.loads(request.body.decode())
        username = json_param['username']
        password = json_param['password']
        try:
            user = models.User.objects.get(username=username)
            if user.password == authenticate.calc_md5(password):
                token = authenticate.get_jwt_token(username)
                code = 200
                message = 'Log in successfully!'
            else:
                token = None
                code = 500
                message = 'Wrong password, try again, please.'
            res = {'code': code, 'message': message, 'data': {'token': token}}
        except:
            code = 500
            message = 'Not successful, please try again!'
            res = {'code': code, 'message': message, 'data': {'token': None}}
        finally:
            print(res)
            return HttpResponse(json.dumps(res), status=res['code'])


@csrf_exempt
def modify_password(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not authenticate.authenticate(token):
        return HttpResponse('No Permission, please log in!')
    cur_username = authenticate.authenticate(token)

    if request.method == 'POST':
        json_param = json.loads(request.body.decode())
        oldPass = json_param['oldPassword']
        newPass = json_param['newPassword']
        comfirmPass = json_param['confirmPassword']
        user = models.User.objects.get(username=cur_username)
        try:
            if user.password == authenticate.calc_md5(oldPass):
                try:
                    print(newPass, comfirmPass)
                    if newPass == comfirmPass:
                        user.password = authenticate.calc_md5(newPass)
                        user.save()
                        msg = 'Successfully modified!'
                        code = 200
                    else:
                        raise ValueError
                except:
                    msg = 'New Passwords do not match!'
                    code = 400
            else:
                raise ValueError
        except:
            msg = 'Old Password dose not match!'
            code = 400
        finally:
            res = {'code': code, 'message': msg, 'data': None}
            return HttpResponse(json.dumps(res), status=res['code'])


@csrf_exempt
def modify_userInfo(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not authenticate.authenticate(token):
        return HttpResponse('No Permission, please log in!')
    cur_username = authenticate.authenticate(token)

    if request.method == 'POST':
        json_param = json.loads(request.body.decode("utf-8"))
        slogon = json_param.get('slogon',None)
        avatar = json_param.get('avatar',None)
        user = models.User.objects.get(username=cur_username)
        code = 0
        try:
            user.slogon = slogon
            user.avatar = avatar
            user.save()
            msg = 'Successful!'
            code = 200
        except:
            msg = 'Not successful, please try again.'
            code = 400
            # render 原网页

        res = {'id': user.id, 'slogon': slogon, 'avatar': avatar, 'username': cur_username, 'code': code}
        return HttpResponse(json.dumps(res), status=res['code'])


def get_userinfo(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not authenticate.authenticate(token):
        return HttpResponse('No Permission, please log in!')
    cur_username = authenticate.authenticate(token)

    if request.method == 'GET':
        try:
            user = models.User.objects.get(username=cur_username)
            msg = 'Successful request!'
            res = {'code': 200,'msg':msg,'data':{'id': user.id, 'slogon': user.slogon, 'avatar': user.avatar, 'username': cur_username},}
        except Exception as e:
            print(e)
            msg = "Cant get access to the information"
            res = {'msg': msg, 'code': 400}

        return HttpResponse(json.dumps(res), status=res['code'])
