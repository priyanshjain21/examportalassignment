import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from main.models import User,Question,Choice,StudentChoice,StudentScore
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, str) -> str:
        """ A function to save the password for storing the values """
        return make_password(str)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class StudentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentChoice
        fields = '__all__'

class StudentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScore
        fields = '__all__'

class StudentScoreDataSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    class Meta:
        model = StudentScore
        fields = '__all__'