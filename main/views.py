from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from main.models import User
from main.serializers import UserSerializer
#To structure the API response according to UI.
def responsedata(status, message, data=None):
    if status:
        return {"status":status,"message":message,"data":data}
    else:
        return {"status":status,"message":message,}

class RegisterUser(APIView):


    def post(self, request):
        #to check if user is already registered with the provided email ID
        if request.data.get('email'):
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response(responsedata(False, "User already present"), status=status.HTTP_400_BAD_REQUEST)
        
        #if password and confirm password does not matches
        if request.data.get("confirm_password") != request.data.get("password"):
            return Response(responsedata(False, "Password Does Not Match!!"), status=status.HTTP_400_BAD_REQUEST)
        if request.data:
            data = request.data
            del data['confirm_password']
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            user_data = serializer.data
            return Response(responsedata(True, "User registered",user_data), status=status.HTTP_200_OK)
        return Response(responsedata(False, "No Data provided"), status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    """To login user using email and password"""

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        #validation for password is required
        if not request.data.get("password"):
            return Response(responsedata(False, "Password is required"), status=status.HTTP_400_BAD_REQUEST)
        #validation if user with given email id does not exists
        if not User.objects.filter(email=request.data.get('email')).exists():
            return Response(responsedata(False, "No user found"), status=status.HTTP_400_BAD_REQUEST)
        #validation to check password
        if not User.objects.get(email=request.data.get('email')).check_password(request.data.get("password")):
            return Response(responsedata(False, "Incorrect Password"), status=status.HTTP_400_BAD_REQUEST)
        #to login user
        if request.data.get('email'):
            user = User.objects.get(email=request.data.get('email'))
            request.data['uuid'] = user.uuid
            user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
            login(request,user)
            #to get user data
            request.data['user'] = User.objects.filter(uuid=request.data.get('uuid')).values()
            return Response(responsedata(True, "Sign in Successful", request.data), status=status.HTTP_200_OK)
        return Response(responsedata(False, "Something went wrong"), status=status.HTTP_400_BAD_REQUEST)
