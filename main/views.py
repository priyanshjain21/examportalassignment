from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from main.models import User,Question,Choice,StudentChoice,StudentScore
from main.serializers import UserSerializer,QuestionSerializer,ChoiceSerializer,StudentScoreDataSerializer,StudentChoiceSerializer,StudentScoreSerializer
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


class AddQuestion(APIView):

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            response_data = {
                "status": True,
                'message': 'Question Added',
                'data': serializer.data
            }
            return Response(data=response_data)
        response_data = {
            'status': False,
            'message': 'error adding question',
            'data': serializer.errors
        }
        return Response(data=response_data, status=400)

class DeleteQuestion(APIView):

     def delete(self, request, pk, format=None):
        import pdb; pdb.set_trace()
        try:
            if StudentChoice.objects.filter(choice__question=pk,choice__is_correct=True).exists():
                studentchoice_objects = StudentChoice.objects.filter(choice__question=pk,choice__is_correct=True)
                for studentchoice_object in studentchoice_objects:
                    studentscore_object = StudentScore.objects.get(student=studentchoice_object.student)
                    studentscore_object.score -=1
                    studentscore_object.save()
            obj = Question.objects.get(uuid=pk)
            obj.delete()
            return Response(data={
                "status": True,
                "message": "Question deleted sucessfully",
                "data": {}
            },
                            status=status.HTTP_200_OK)
        except:
            return Response(data={
            "status": False,
            "message": "Question deletion failed",},
                        status=status.HTTP_400_BAD_REQUEST)

class QuestionsList(APIView):

    def get(self,request):
        obj = Question.objects.all()
        serializer = QuestionSerializer(obj,many=True)
        return Response(responsedata(True, "Questions List", serializer.data), status=status.HTTP_200_OK)


class ChoiceForQuestion(APIView):
    def get(self,request,question_id):
        choices = Choice.objects.filter(question=question_id)
        serializer = ChoiceSerializer(choices,many=True)
        return Response(responsedata(True, "Choice List", serializer.data), status=status.HTTP_200_OK)

class AddChoice(APIView):
     def post(self, request):

        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            response_data = {
                "status": True,
                'message': 'Choice Added',
                'data': serializer.data
            }
            return Response(data=response_data)
        
        response_data = {
            'status': False,
            'message': 'error adding choice',
            'data': serializer.errors
        }
        return Response(data=response_data, status=400)

class DeleteChoice(APIView):
     def delete(self, request, pk, format=None):
        try:
            obj = Choice.objects.get(uuid=pk)
            obj.delete()
            return Response(data={
                "status": True,
                "message": "Choice deleted sucessfully",
                "data": {}
            },
                            status=status.HTTP_200_OK)
        except:
            return Response(data={
            "status": False,
            "message": "Choice deletion failed",},
                        status=status.HTTP_400_BAD_REQUEST)

class StudentChoiceSelection(APIView):
    def post(self, request):
        import pdb;pdb.set_trace()
        
        choice_object = Choice.objects.get(uuid=request.data['choice'])

        if StudentChoice.objects.filter(choice__question=choice_object.question,student=request.data['student']).exists():
            return Response(responsedata(False, "User already added choice for this question"), status=status.HTTP_400_BAD_REQUEST)
        if choice_object.is_correct:
            if StudentScore.objects.filter(student=request.data['student']).exists():
                studentscore_object = StudentScore.objects.get(student=request.data['student'])
                studentscore_object.score +=1
                studentscore_object.save()
            else:
                studentscore_data = { "student": request.data['student'], "score": 1}
                studentscore_serializer = StudentScoreSerializer(data=studentscore_data)
                if studentscore_serializer.is_valid(raise_exception=True):
                    studentscore_serializer.save()

        serializer = StudentChoiceSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            response_data = {
                "status": True,
                'message': 'Choice Added',
                'data': serializer.data
            }
            return Response(data=response_data)
        response_data = {
            'status': False,
            'message': 'error adding choice',
            'data': serializer.errors
        }
        return Response(data=response_data, status=400)

class StudentScoreResult(APIView):

    def get(self,request):
        studentscore_objects = StudentScore.objects.all()
        serializer = StudentScoreDataSerializer(studentscore_objects,many=True)
        return Response(responsedata(True, "Questions List", serializer.data), status=status.HTTP_200_OK)
