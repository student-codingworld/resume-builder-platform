from django.urls import path
from .views import CreateResume, DownloadResume, ResumeList, ResumeDetail

urlpatterns = [
    path('create/', CreateResume.as_view()),
    path('list/', ResumeList.as_view()),
    path('view/<int:pk>/', ResumeDetail.as_view()),
    path('download/<int:pk>/', DownloadResume.as_view()),
]