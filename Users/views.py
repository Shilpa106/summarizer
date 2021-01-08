from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django import template
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model


from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import jwt

from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer
from .services.generate_user import generate_data, generate_user_data
from .services.emailTemplate import verification_template
from utils.messages import message
from utils.emails.mailer import send_email


User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        '''
        Method to register as a user
        : Permission : 'Anyone can Register'
        : Mehod : `POST`
        : Params : `Email, Username, Mobile, Password and Confirm Password`

        '''

        
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = generate_data(request, serializer)

        try:
            db_temp = verification_template
            send_temp = template.Template(db_temp)
            context_msg = template.Context({'user':user_data['data']['email'], 'absurl':user_data['absurl']})
            html_content = send_temp.render(context_msg)
            text_content = strip_tags(html_content)

            data = {'email_body': text_content, 'to_email': user_data['data']['email'], 'email_subject': 'Verify Your Email', 'attach': html_content }
            send_email(data) # uses delay to send email via celery 
        except Exception as e:
            # print("error",e)
            return Response({'Wrong': message.messages['User']['Wrong']}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(user_data, status=status.HTTP_201_CREATED)



# Verify Email View with verification link
class VerifyEmail(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        '''
        Method to verify an email and user during Registration
        : Mehod : `GET`
        : Params : `Token sent via email`
        : Process : `After veryfiyng, User will automatically login and Welcome email will be sent for first time`

        '''

        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)  # encode the received token
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

                # code to send welcome email to after verification
                data = {}
    
                text_content = '<p>Welcome to the <strong>Community</strong>.</p>'
                data = {'email_body': text_content, 'to_email': user.email, 'email_subject': 'Welcome', 'attach': text_content }
                send_email(data) # uses delay to send email via celery
                

            if not request.session.get('detail'):
                login(request, user)
            else:
                return Response({"Message": message.messages['User']['AlreadyVerifiedLoggedIn']})

            user_data = generate_user_data(request, user) #Generate data using function call
            user_data['Success'] = message.messages['User']['EmailVerified']

            return Response(user_data, status=status.HTTP_200_OK )

        except jwt.ExpiredSignatureError as e:
            return Response({'Error': 'Signature Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as e:
            return Response({'Error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

     


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        '''
        Method to Login a User
        : Mehod : `POST`
        : Permission : 'Anyone can Login with credentials'
        : Params : `Email, Password`
        : Response : `Return user data as email, and token`

        '''

        email = request.data.get('email')
        password = request.data.get('password')
        
        if not request.session.get('detail'):
            if email is None or password is None:
                return Response({'Error': message.messages['User']['FieldBlank']}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(password) < 6:
                return Response({'Error': message.messages['User']['LenPassword']}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = authenticate(email=email, password=password)
            except Exception as e:
                return Response({'Error': message.messages['User']['InvalidCredentials']}, status=status.HTTP_400_BAD_REQUEST)
                
            if user is None:
                return Response({'Error': message.messages['User']['UserNone']}, status=status.HTTP_404_NOT_FOUND)

            if user.is_active == True and user.is_verified == True:
                login(request, user)
                user_data = generate_user_data(request, user) #Generate data using function call
                return Response(user_data, status=status.HTTP_200_OK)
                # return Response({"Success": True, "Message": "Successfully Logged in"}, status=status.HTTP_200_OK)
            else:
                return Response({"Failed": "You are not verified"})
        else:
            return Response({'Info': message.messages['User']['LoginInfo']})




class LogoutView(APIView):
    '''
    Logout a Looged in user
    '''

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        '''
        Authenticated user with token can access
        '''

        try:
            logout(request)
        except KeyError:
            pass

        return Response({'Success': message.messages['User']['LogoutSuccess']}, status=status.HTTP_200_OK)
       