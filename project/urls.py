"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from project_app import views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/update_profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('courses/', views.ViewCourses.as_view(), name='view_courses'),
    path('courses/create/', views.CreateCourse.as_view(), name='create_course'),
    path('courses/<int:course_id>/', views.ViewCourse.as_view(), name='view_course'),
    path('courses/<int:course_id>/edit/', views.EditCourse.as_view(), name='edit_course'),
    path('courses/<int:course_id>/delete/', views.DeleteCourse.as_view(), name='delete_course'),
    # path('courses/<int:course_id>/assign', , name='assign_course_ta'),
    # path('courses/<int:course_id>/remove', , name='remove_course_ta'),
    path('courses/<int:course_id>/sections/create/', views.CreateSection.as_view(), name='create_section'),
    path('courses/<int:course_id>/sections/<int:section_id>/edit', views.EditSection.as_view() , name='edit_section'),
    path('courses/<int:course_id>/sections/<int:section_id>/delete/', views.DeleteSection.as_view(), name='delete_section'),
    # path('courses/<int:course_id>/sections/<int:section_id>/assign', , name='assign_section_ta')
    # path('courses/<int:course_id>/sections/<int:section_id>/remove', , name='remove_section_ta')
    path('users/', views.ViewUsers.as_view(), name='view_users'),
    path('users/create/', views.CreateUser.as_view(), name='create_user'),
    path('users/<int:user_id>/', views.ViewUser.as_view(), name='view_user'),
    path('users/<int:user_id>/edit/', views.EditUser.as_view(), name='edit_user'),
    path('users/<int:user_id>/delete/', views.DeleteUser.as_view(), name='delete_user'),
    # path('notifications/', view.Notifications.as_view(), name='view_notifications')
    # path('notifications/send/', views.SentNotification.as_view(), name='send_notification')
    # path('notifications/<int:notification_id>, views.Notfication.as_view(), name='view_notification')
    # path('notifications/<int:notification_id>/delete/', views.DeleteNotification.as_view(), name='delete_notification')
]
