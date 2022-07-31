from django.urls import path
from myapp import views


# 현재 app에서 사용할 Routing
# path('경로', views.함수명)
urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read),  # 가변값은 < > 안에 / views.py에서 파라미터로 받아 처리해
    path('delete/', views.delete),
    path('update/<id>/', views.update)
]
