from django.contrib import admin
from django.apps import apps


# --------------------------------------------------
# IIC ADMIN CONFIGURATION
# --------------------------------------------------

admin.site.site_header = "IIC ERP"
admin.site.site_title = "IIC ERP"
admin.site.index_title = "IIC Administration"

# After successful login, show the custom IIC dashboard
admin.site.index_template = "admin/iic_index.html"


# --------------------------------------------------
# Register IIC models in Django Admin
# --------------------------------------------------

iic_app = apps.get_app_config("iic")

for model in iic_app.get_models():
    if not admin.site.is_registered(model):
        admin.site.register(model)


# --------------------------------------------------
# IIC Dashboard Data
# --------------------------------------------------

def iic_dashboard_context(request):
    """
    Supplies IIC dashboard information to Django Admin.
    """

    from .models import (
        Student,
        Event,
        ExternalEvent,
        StudentAchievement,
        Team,
        Project,
    )

    active_students = Student.objects.filter(
        is_active=True
    ).count()

    events_count = Event.objects.count()

    external_events_count = ExternalEvent.objects.count()

    achievements_count = StudentAchievement.objects.count()

    teams_count = Team.objects.filter(
        is_active=True
    ).count()

    projects_count = Project.objects.count()

    recent_achievements = (
        StudentAchievement.objects
        .all()
        .order_by("-id")[:5]
    )

    recent_external_events = (
        ExternalEvent.objects
        .all()
        .order_by("-id")[:5]
    )

    return {
        "iic_active_students": active_students,
        "iic_events_count": events_count,
        "iic_external_events_count": external_events_count,
        "iic_achievements_count": achievements_count,
        "iic_teams_count": teams_count,
        "iic_projects_count": projects_count,
        "iic_recent_achievements": recent_achievements,
        "iic_recent_external_events": recent_external_events,
    }