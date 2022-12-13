from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.views import APIView, Response

from .serializer import UserSerializer
from .models import User

import jwt

import datetime

import pandas


class RegisterView(APIView):
    
    def post(self, request):
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1-Wx3MunuVlDT96K_fz18P1HgBUYaxSBjUu16_KyNjDU/gviz/tq?tqx=out:csv"
        file = pandas.read_csv(SHEET_URL)
        users = []
        count = 1
        for user in file.iterrows():
            user_data = {}
            
            first_name= user[1]['first_name']
            last_name = user[1]['last_name']
            user_data["name"] = f"{first_name} {last_name}"
            
            first_name = first_name.split()[0].lower()
            last_names= last_name.split()
            last_name = last_names[len(last_names)-1].lower()
            user_data["email"] = f"{first_name}{last_name}{count}@gmail.com"
 
            user_data['password'] = "pass1234"
            
            users.append(user_data)
            serializer = UserSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            count += 1
            
        return Response({"status": "success", "users": users})

class SignUpView(APIView):

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
    
class UserView(APIView):

    def get(self, request):
        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token,'*C7Grs0Q7IiB$UT#U!@jmMoBtBhM13p!yEcDsIsL', algorithms='HS256')
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
    
        return Response(serializer.data)
    
class LogoutView(APIView):

    def post(self, request):
        
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'sucess logout'
        }

        return response