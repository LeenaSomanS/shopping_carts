from django.shortcuts import render
from carts_app.models import *
from django.http import HttpResponse,JsonResponse
import json
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import hashlib
from datetime import date
from django.db.models import Count,F
from  datetime import datetime,timedelta
from secrets import token_urlsafe
from datetime import datetime
from datetime import datetime as dt
# Create your views here.
########################################################################
#  USER CREATION                                                       #
########################################################################

USER=1

@csrf_exempt
def user_creation(request):
    received_json_data=json.loads(request.body)
    data_dict=json.dumps(received_json_data)
    data=json.loads(data_dict)
    full_name=data["fullName"]
    user_name=data["userName"]
    password=data["password"]
    hashed_pswd=hashlib.sha256(password.encode())
    hashed_pswd=hashed_pswd.hexdigest()
    user_object=User.objects.filter(user_name=user_name)
    if user_object.count()!=0:
        return JsonResponse({"status":409,"message":"User already exist"},safe=False)
    role_obj=Role.objects.get(role_name="User")
    user_data=User(full_name=full_name,user_name=user_name,password=hashed_pswd)

    user_data.save()
    role=RoleMapping(role_id=role_obj,user_id=user_data)
    role.save()
    return JsonResponse({"status":200,"message":"Successfully created the user"},safe=False)
########################################################################
#  USER LOGIN                                                          #
########################################################################
@csrf_exempt
def login(request):
    received_json_data=json.loads(request.body)
    data=json.dumps(received_json_data)
    data=json.loads(data)
    user_name=data["userName"]
    password=data["password"]
    curr_time=datetime.now()
    exp_time=curr_time++ timedelta(days=1)
    session_token = token_urlsafe(64)
    hashed_pswd=hashlib.sha256(password.encode())
    hashed_pswd=hashed_pswd.hexdigest()
    user_obj=User.objects.filter(user_name=user_name,password=hashed_pswd)
    if user_obj.count()!=0:
        for i in user_obj:
            i.session_token=session_token
            i.exp_date=exp_time
            i.save()
        return JsonResponse({"status":200,"message":"Successfully logged in"},safe=False)
    else:
        return JsonResponse({"status":404,"message":"You have entered wrong password"},safe=False)
########################################################################
#  API ADDING ITEMS TO CARTS                                           #
########################################################################
@csrf_exempt
def add_items_to_carts(request):
    received_json_data=json.loads(request.body)
    data=json.dumps(received_json_data)
    data=json.loads(data)
    item_id=data["itemId"]
    user_id=data["userId"]
    session_token=data["sessionToken"]
    user_has_session=session_validation(user_id,session_token)
    if user_has_session:
        item_obj=Item.objects.get(item_id=item_id)
        user_object=User.objects.get(user_id=user_id)
        # print(user_object.count())
        today = date.today()
        carts_object_existence=Cart.objects.filter(item_id=item_obj,user_id=user_object)
        if carts_object_existence.count()!=0:
            return JsonResponse({"status":409,"message":"Data already exists"},safe=False)
        carts_object=Cart(item_id=item_obj,user_id=user_object,cart_date=today)
        carts_object.save()
        return JsonResponse({"status":200,"message":"Successfully added"},safe=False)
    else:
        return JsonResponse({"status":401,"message":"Unauthorised access"},safe=False)
    # return JsonResponse({"status":404,"message":"Invalid user id"},safe=False)
########################################################################
#  API FOR LISTING CART ITEMS                                           #
########################################################################

@csrf_exempt
def date_wise_cart_items(request):
    received_json_data=json.loads(request.body)
    data=json.dumps(received_json_data)
    data=json.loads(data)
    cart_date=data["date"]
    session_token=data["sessionToken"]
    user_id=data["userId"]
    user_has_session=session_validation(user_id,session_token)
    if user_has_session:
        # cart_date=dt.strptime(cart_date,'%Y-%m-%d')
        # start_date=cart_date.strftime('%Y-%m-%d 00:00:00')
        # end_date=cart_date.strftime('%Y-%m-%d 23:59:59')
        cart_list= list(Cart.objects.annotate(cartId=F('cart_id'),itemId=F('item_id'),itemName=F('item_id__item_name'),userId=F('user_id'),userName=F('user_id__full_name'),).values("cartId","itemId","itemName","userId","userName").filter(cart_date__range=(cart_date,cart_date)))
        print(cart_list)
        return JsonResponse({"status":200,"message":"Successfully listed","data":cart_list},safe=False)
    return JsonResponse({"status":401,"message":"Unauthorised access"},safe=False)
########################################################################
#  API FOR ADDING ROLES TO USERS                                         #
########################################################################

@csrf_exempt
def user_role_mapping(request):
    received_json_data=json.loads(request.body)
    data=json.dumps(received_json_data)
    data=json.loads(data)
    role_list=data["roleList"]
    user_id=data["userId"]
    admin_id=data["adminId"]
    session_token=data["sessionToken"]
    user_has_session=session_validation(admin_id,session_token)
    if user_has_session:
        user_object=User.objects.get(user_id=user_id)
        role_object=RoleMapping.objects.filter(user_id=admin_id,role_id=2)
        if role_object.count()==0:
            return JsonResponse({"status":403,"message":"Can't add,only admin can add this roles"},safe=False)
        role_object=RoleMapping.objects.filter(user_id=user_id,role_id__in=role_list)
        if role_object.count()!=0:
            return JsonResponse({"status":409,"message":"Roles already mapped"},safe=False)
        for i in role_list:
            rol_obj=Role.objects.get(role_id=i)
            role=RoleMapping(role_id=rol_obj,user_id=user_object)
            role.save()
        return JsonResponse({"status":200,"message":"Successfully added"},safe=False)
    return JsonResponse({"status":401,"message":"Unauthorised access"},safe=False)

########################################################################
#  API FOR LISTING USERS                                               #
########################################################################

@csrf_exempt
def user_list(request):
    received_json_data=json.loads(request.body)
    data=json.dumps(received_json_data)
    data=json.loads(data)
    admin_id=data["adminId"]
    session_token=data["sessionToken"]
    user_has_session=session_validation(admin_id,session_token)
    if user_has_session:
        role_object=RoleMapping.objects.filter(user_id=admin_id,role_id=2)
        if role_object.count()==0:
            return JsonResponse({"status":403,"message":"You don't have the provision to view the user list"},safe=False)
        user_list= list(RoleMapping.objects.annotate(userId=F('user_id'),roleId=F('role_id'),userName=F('user_id__full_name'),roleName=F('role_id__role_name')).values("userId","roleId","userName","roleName"))
        return JsonResponse({"status":200,"message":"Successfully listed","data":user_list},safe=False)
    return JsonResponse({"status":401,"message":"Unauthorised access"},safe=False)


 
def session_validation(user_id,session_token):
    user_obj=User.objects.filter(user_id=user_id,session_token=session_token,exp_date__gt=datetime.now())
    if user_obj.count()!=0:
        return True
    else:
        return False