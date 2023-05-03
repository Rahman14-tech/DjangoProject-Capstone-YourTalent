from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static 
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_place,name="login"),
    path("register",views.register,name="register"),
    path("logout", views.logout_place, name="logout"),
    path("home/<str:username>",views.home,name="home"),
    path("authenticate/<str:username>",views.authentication,name="authenticate"),
    path("authenticate_api/<str:username>",views.authenticateapi,name="authenticateapi"),
    path("viewcontent/<str:category>/<int:id>",views.viewcontent,name="viewcontent"),
    path("mycontents/<str:username>",views.mycontents,name="mycontents"),
    path("interest/<str:username>",views.interest,name="interest"),
    path("API_Interest",views.interest_content,name="interest_content"),
    path("API_Uninterest",views.uninterest_content,name="uninterest_content"),
    path("API_Notif/<int:id>",views.notifapi,name="notifapi"),
    path("API_Delete/<str:category>/<int:id>",views.delete_content,name="delete_content")
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)