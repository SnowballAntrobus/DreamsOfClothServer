from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from server import views

urlpatterns = [
    path('print-message/', views.PrintMessageView.as_view(), name='print-message'),
    path('image-upload/', views.GetObjectMaskView.as_view(), name='image-upload/'),
    path('test-json-nest/', views.TestNestedJSONView.as_view()),
    path('test-complex/', views.TestComplexView.as_view()),
]