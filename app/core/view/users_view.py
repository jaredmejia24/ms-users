from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.views import APIView, Response

from ..serializer import UserSerializer
from ..models import User

import jwt

class SelfUserView(APIView):

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
    
class UserViewSet(APIView):
    
    def get(self, request):
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)

class UserByPkView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        pk = kwargs['pk']
        
        user = User.objects.filter(id=pk).first()
        
        if(not user):
            raise NotFound("User Not Found")
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)