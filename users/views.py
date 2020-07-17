from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.permissions import IsAuthenticated
from .models import Customer, User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


@api_view(['GET'])
def users_list(request):
    users_queryset = Customer.objects.all()  # retrieve a list of users from the database

    users_json = serialize('json', users_queryset)  # serialize the query set to a json list of objects

    return HttpResponse(users_json, content_type='application/json')  # send users_json list as a http response.


@csrf_exempt
def register(request):
    register_request = request_body(
        request.body)  # load the request object body and json serialize it, assign it to register_request variable

    user = User.objects.create_user(
        email=register_request['email'],
        password=register_request['password']
    )

    customer = Customer.objects.create(
        user=user,
        first_name=register_request['first_name'],
        last_name=register_request['last_name'],
        telephone=register_request['telephone'],
        location=register_request['location']
    )  # creating an instance of the customer class and assigning values to the object

    if customer is not None:
        success_message = {
            "success": "Registration successful"
        }  # a success message to be returned after a successfull registration

        return JsonResponse(success_message, safe=False)
    else:
        error_message = {
            "error": "An error occurred during registration"
        }  # an error message returned if registration fails
        return JsonResponse(error_message, safe=False).status_code(304)


@csrf_exempt
def login(request):
    # retrieve request body as a json string
    login_request = json.loads(request.body)

    # assign email and password values from the request body
    email = login_request['email']
    password = login_request['password']

    # attempt to authenticate the details presented
    user_to_login = authenticate(email=email, password=password)

    # if authentication fails, throw an error 404 for not finding the user
    if user_to_login is None:
        error_message = {
            "message": "Invalid login credentials"
        }
        return JsonResponse(status=404,data=error_message, safe=False)

    try:
        payload = JWT_PAYLOAD_HANDLER(user_to_login)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user_to_login)

    except User.DoesNotExist:
        return JsonResponse('User does not exist', safe=False)

    auth_response = {
        "email": email,
        "token": jwt_token
    }

    return JsonResponse(auth_response, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    member = Customer.objects.get(user=user)

    some_data = member.__dict__
    user_obj = {
        'first_name': some_data['first_name'],
        'last_name': some_data['last_name'],
        'telephone': some_data['telephone'],
        'location': some_data['location'],
        'is_vip': some_data['is_vip'],
        'referrals': some_data['referrals']
    }
    return JsonResponse(user_obj, safe=False)


# a helper function that converts the request body object to a json string.
# could be used in a number of areas in this view
def request_body(params):
    return json.loads(params)
