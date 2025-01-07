
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("finance/", include("finance.urls")),
    path("services/",include("service.urls"))
]
