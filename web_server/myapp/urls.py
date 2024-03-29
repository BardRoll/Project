from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    # path('user_management', views.user_management),
    path('add_user', views.add_user),
    path('edit_user/<student_id>', views.edit_user),
    path('delete_user/<student_id>', views.delete_user),
    path('sign-in', views.sign_in),
    path('sign-out', views.sign_out, name="sign-out"),
    path('upload_csv', views.upload_csv),
    path('test_control/<student_id>', views.custom_test_control),
    path('test_result/<student_id>', views.test_result),
    path('test_result_all', views.test_result_all),
    path('download_csv', views.download_csv),
    path('example_test_control', views.example_test_control),
]