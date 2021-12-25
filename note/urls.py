from django.urls import path
from . import views
urlpatterns = [
    path('all/', views.list_view),
    path('add/', views.add_view),
    path('update/<int:note_id>', views.update_view),
    path('delete/', views.delete_view)
]
