from django.urls import path
# import views
from .views import home, post_detail # Import these functions from views.py


urlpatterns = [
    path('', home),
    path('blog/<int:post_id>', post_detail, name="post_detail"), 
]