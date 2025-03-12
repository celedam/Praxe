# my_project/urls.py

from django.contrib import admin
from django.urls import path, include  # include pro vkládání URL z jiných aplikací

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Tady vkládáš api.urls, což je soubor v aplikaci api
]
