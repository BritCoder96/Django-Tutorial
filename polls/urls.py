from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/<int:user_id>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:user_id>/<int:question_id>/userIndex/', views.UserIndexView.as_view(), name='userIndex'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]