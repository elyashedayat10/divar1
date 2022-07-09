from random import randint

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..models import OtpCode
from ..utils import send_otp
from .serializers import PhoneSerializer, VerifySerializer

user = get_user_model()


class SendOtpApiView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            random_number = randint(111111, 999999)
            otp_code = OtpCode.objects.create(
                phone_number=phone_number, code=random_number
            )
            send_otp(phone_number, random_number)
            contex = {
                "is_done": True,
                "message": "کد برای کاربر ارسال شد",
            }
            return Response(data=contex, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": serializer.errors,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


    
    
class VerifyApiView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]
            otp_obj = OtpCode.objects.get(phone_number=phone_number)
            if otp_obj and otp_obj.code == code:
                try:
                    user_obj = user.objects.get(phone_number=phone_number)
                    token, created = Token.objects.get_or_create(user=user_obj)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفقیت وارد شد",
                        "token": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
                except user.DoesNotExist:
                    user_obj = user.objects.create_user(phone_number=phone_number)
                    token_obj = Token.objects.create(user=user_obj)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفیت ساخته شد",
                        "token": token_obj.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    "is_done": False,
                    "message": "کد ارسال برای کاربر با کد ذزیافتی همخوانی ندارد",
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        context = {
            "is_done": False,
            "message": "خطا در پارامتر ارسالی",
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
    



#
# class LogoutApiView(GenericAPIView):
