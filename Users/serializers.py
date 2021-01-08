# Rest Framework imports
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator


from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email       = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')])
    username    = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')])
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: "9999999999". in 10 digits')
    mobile       = serializers.CharField(max_length=15, validators=[phone_regex], required=True)
    password    = serializers.CharField(max_length=50, min_length=6, write_only=True, style={'input_type': 'password'})
    confirm_password    = serializers.CharField(max_length=50, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        # model = CustomUser
        fields = ['email', 'username', 'mobile', 'password', 'confirm_password']
        

    def validate(self, attrs):
        # get the password from the attrs
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        

        if password != confirm_password:
            raise serializers.ValidationError({"Password": "Password field must match"})

        # errors = dict() 
        # try:
        #     # validate the password and catch the exception
        #     validators.validate_password(password=password, user=CustomUser)

        # # the exception raised here is different than serializers.ValidationError
        # except exceptions.ValidationError as e:
        #     errors['password'] = list(e.messages)

        # if errors:
        #     raise serializers.ValidationError(errors)
        
        return super(RegisterSerializer, self).validate(attrs)


    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
            raise serializers.ValidationError({"Error": "This email already registered"})
        except User.DoesNotExist:
            validated_data.pop('confirm_password')
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
        return user


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']



class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=5, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password']