from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Student
    path(
        "student/register/",
        views.student_register,
        name="student_register"
    ),
    path(
        "student/login/",
        views.student_login,
        name="student_login"
    ),
    path(
        "student/dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),
    path(
        "student/logout/",
        views.student_logout,
        name="student_logout"
    ),
    path(
        "student/prototype/register/",
        views.prototype_register,
        name="prototype_register"
    ),

    # IIC Admin
    path(
        "iic-admin/",
        views.iic_admin_dashboard,
        name="iic_admin_dashboard"
    ),
    path(
        "iic-admin/students/",
        views.iic_admin_students,
        name="iic_admin_students"
    ),
    path(
        "iic-admin/external-events/",
        views.iic_admin_external_events,
        name="iic_admin_external_events"
    ),
    path(
        "iic-admin/achievements/",
        views.iic_admin_achievements,
        name="iic_admin_achievements"
    ),
    path(
        "iic-admin/teams/",
        views.iic_admin_teams,
        name="iic_admin_teams"
    ),
]