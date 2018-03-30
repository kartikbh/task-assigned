from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (LoginSerializer, RegistrationSerializer)
from .renderers import UserJSONRenderer

#send email function


def send_email(email):
    from django.core.mail import send_mail
    send_mail(
        'New otp',
        'here is the messsage',
        'kartik.bhatnagar@civilmachines.com',
        [email],
        fail_silently=False,
    )
#forgot email fucntion


def forgot_password(email, otp):
    from django.core.mail import send_mail
    send_mail(
        'New otp',
        otp,
        'kartik.bhatnagar@civilmachines.com',
        [email],
        fail_silently=False,
        )
# we will call forgot_email here so that user can get OTP


class ForgotPasswordAPI(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self):
        return Response('Success', status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        from .serializers import ForgotPasswordSerializers
        sdata = ForgotPasswordSerializers(data=request.data)
        forgot_password('kartikbhatnagar2015@gmail.com', '200')
        return Response(sdata.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self,):
        return Response('Success', status=status.HTTP_200_OK)


    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        send_email('niteshkhanduja19943@gmail.com')
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
