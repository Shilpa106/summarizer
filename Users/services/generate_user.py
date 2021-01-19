from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken


from utils.messages import message


User = get_user_model()


def generate_user_data(request, user):

    '''
        Generate Token and Session Data to use inside email verification and login
        param :HTTPRequest: `request` - It will take the HTTPRequest
        param :User: `user` - And User Data
        
        ** context **
        :token: - Token will get or create by passing users
        :return: - Return the user_data dict
    '''

    try:
        token, created = Token.objects.get_or_create(user=user)
    except Exception as e:
        return Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)


    user_data = {}
    user_data['token'] = token.key
    user_data['id'] = user.id
    user_data['email'] = user.email
    request.session['detail'] = user_data

    return user_data



def generate_data(request, serializer):
    '''
        Generate User data during registration
        param :HTTPRequest: `request` - It will take the HTTPRequest
        param :serializer: `serializer` 
        
        ** context **
        :token: - RefreshToken will generate for email verification with 1 day expiry.
        :return: - Return the user_data dict with email and verification link
    '''
    
    user_data = {}
    user_data['data'] = serializer.data
    user_data['message'] = 'Successfully Registered'
    
    # try:
    #     user = User.objects.get(email=user_data['data']['email'])
    #     token = RefreshToken.for_user(user).access_token
    # except Exception as e:
    #     return Response({'Error': 'Invalid Email'})

    # current_site = str(get_current_site(request))
    # relative_link = reverse('verify-email')

    # absurl = f"http://{current_site}{relative_link}?token={str(token)}"
    
    # https://trupinion-survey.herokuapp.com/api/v1/users/verify-email/?token={str(token)}
    # absurl = f"https://trupinion-react.netlify.app/#/login-by-token/{str(token)}"
    # user_data['absurl'] = absurl
    return user_data