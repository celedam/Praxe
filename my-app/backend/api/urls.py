from django.urls import path
from .views import TextEditor  # Importujeme třídu TextEditor ze souboru views.py

urlpatterns = [
    path('texteditor/', TextEditor.as_view(), name='text_editor'),  # Připojujeme třídu k URL
]
