from django.urls import path
from django.contrib.auth import views as auth_views
from broker_app.views import index, SurveyCreate, SurveyUpdate, SurveyDelete

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('survey/add/', SurveyCreate.as_view(), name='survey-add'),
    path('survey/<int:pk>/', SurveyUpdate.as_view(), name='survey-update'),
    path('survey/<int:pk>/delete/', SurveyDelete.as_view(), name='survey-delete'),
]
