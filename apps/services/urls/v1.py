from django.urls import path

app_name = 'v1'

urlpatterns = [
    path('services/', ServiceTypeAPIView.as_view(), name='service-list-create'),
]