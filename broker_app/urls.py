from broker_app.views import index, signup, LandlordReponseCreate, LandlordResponseUpdate, LandlordResponseDelete, \
    RequirementsCreate, RequirementsDelete, \
    RequirementsUpdate, TourBookCreate, TourBookUpdate, TourBookDelete, ExecutiveSummaryCreate, ExecutiveSummaryDelete, \
    ExecutiveSummaryUpdate, MediaFileCreateView, tourbook_ppt_view, MediaFileDeleteView, \
    email_requirement, BuildingCreate, BuildingUpdate, BuildingDelete
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('building/add/', BuildingCreate.as_view(), name='building-add'),
    path('building/<int:pk>/', BuildingUpdate.as_view(), name='building-update'),
    path('building/<int:pk>/delete/', BuildingDelete.as_view(), name='building-delete'),
    path('landlordresponse/add/', LandlordReponseCreate.as_view(), name='landlordresponse-add'),
    path('landlordresponse/<int:pk>/', LandlordResponseUpdate.as_view(), name='landlordresponse-update'),
    path('landlordresponse/<int:pk>/delete/', LandlordResponseDelete.as_view(), name='landlordresponse-delete'),
    path('requirement/add/', RequirementsCreate.as_view(), name='requirement-add'),
    path('requirement/<int:pk>/', RequirementsUpdate.as_view(), name='requirement-update'),
    path('requirement/<int:pk>/delete/', RequirementsDelete.as_view(), name='requirement-delete'),
    path('tourbook/add/', TourBookCreate.as_view(), name='tourbook-add'),
    path('tourbook/<int:pk>/', TourBookUpdate.as_view(), name='tourbook-update'),
    path('tourbook/<int:pk>/delete/', TourBookDelete.as_view(), name='tourbook-delete'),
    path('executivesummary/add/', ExecutiveSummaryCreate.as_view(), name='executivesummary-add'),
    path('executivesummary/<int:pk>/', ExecutiveSummaryUpdate.as_view(), name='executivesummary-update'),
    path('executivesummary/<int:pk>/delete/', ExecutiveSummaryDelete.as_view(), name='executivesummary-delete'),
    path('tourbook_ppt/<int:pk>/', tourbook_ppt_view, name='tourbook-ppt'),
    path('media_upload/<int:landlordresponse_pk>/', MediaFileCreateView.as_view(), name='media-upload'),
    path('media_delete/<int:pk>/delete/', MediaFileDeleteView.as_view(), name='media-delete'),
    path('email_requirement/<int:pk>', email_requirement, name='email_requirement'),

]
