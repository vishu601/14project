from django.contrib import admin
from django.urls import path
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('StudentReg/', StudentReg, name='StudentReg'),
    path('showstudent/', showstudent, name='showstudent'),
    path('updatestudent/<int:id>/', updatestudent, name='updatestudent'),
    path('deletestudent/<int:id>/', deletestudent, name='deletestudent'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
