from django.urls import path

from . import views

urlpatterns = [
    path('registeruser', views.RegisterUser.as_view()),
    path('loginuser', views.LoginUser.as_view()),
    path('addquestion', views.AddQuestion.as_view()),
    path('addchoice',views.AddChoice.as_view()),
    path('questionslist', views.QuestionsList.as_view()),
    path('choicesforquestion/<question_id>',views.ChoiceForQuestion.as_view()),
    path('deletequestion/<pk>',views.DeleteQuestion.as_view()),
    path('deletechoice/<pk>',views.DeleteChoice.as_view()),
    path('studentchoiceselection',views.StudentChoiceSelection.as_view()),
    path('studentscore',views.StudentScoreResult.as_view())


]