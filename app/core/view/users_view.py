from rest_framework.exceptions import AuthenticationFailed
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
        print("before all")
        users = User.objects.all()
        
        print(users)
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)