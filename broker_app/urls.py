from broker_app.views import index, SurveyCreate, SurveyUpdate, SurveyDelete, RequirementsCreate, RequirementsDelete, \
    RequirementsUpdate, TourBookCreate, TourBookUpdate, TourBookDelete, ExecutiveSummaryCreate, ExecutiveSummaryDelete, \
    ExecutiveSummaryUpdate, tourbook_pdf_view
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('survey/add/', SurveyCreate.as_view(), name='survey-add'),
    path('survey/<int:pk>/', SurveyUpdate.as_view(), name='survey-update'),
    path('survey/<int:pk>/delete/', SurveyDelete.as_view(), name='survey-delete'),
    path('requirement/add/', RequirementsCreate.as_view(), name='requirement-add'),
    path('requirement/<int:pk>/', RequirementsUpdate.as_view(), name='requirement-update'),
    path('requirement/<int:pk>/delete/', RequirementsDelete.as_view(), name='requirement-delete'),
    path('tourbook/add/', TourBookCreate.as_view(), name='tourbook-add'),
    path('tourbook/<int:pk>/', TourBookUpdate.as_view(), name='tourbook-update'),
    path('tourbook/<int:pk>/delete/', TourBookDelete.as_view(), name='tourbook-delete'),
    path('executivesummary/add/', ExecutiveSummaryCreate.as_view(), name='executivesummary-add'),
    path('executivesummary/<int:pk>/', ExecutiveSummaryUpdate.as_view(), name='executivesummary-update'),
    path('executivesummary/<int:pk>/delete/', ExecutiveSummaryDelete.as_view(), name='executivesummary-delete'),
    path('tourbook_pdf/<int:pk>/', tourbook_pdf_view, name='tourbook-pdf')

]
