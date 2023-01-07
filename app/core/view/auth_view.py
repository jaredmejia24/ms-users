from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.views import APIView, Response

from ..serializer import UserSerializer
from ..models import User

import jwt

import datetime

class RegisterView(APIView):

    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise NotFound("User Not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, '*C7Grs0Q7IiB$UT#U!@jmMoBtBhM13p!yEcDsIsL', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt':token
        }

        return response
    
class LogoutView(APIView):

    def post(self, request):
        
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'sucess logout'
        }

        return response