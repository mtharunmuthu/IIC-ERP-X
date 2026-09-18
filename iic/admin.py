from django.contrib import admin

from .models import (
    Department,
    Student,
    Team,
    TeamMember,
    Project,
    IICMembership,
    Event,
    EventRegistration,
    ExternalVenture,
    ExternalPayment,
    Attendance,
    DailyProgress,
    ExternalEvent,
    StudentAchievement,
)

# ============================================================
# DEPARTMENT
# ============================================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "is_active",
    )


# ============================================================
# STUDENT
# ============================================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "register_number",
        "first_name",
        "last_name",
        "department",
        "year",
        "section",
        "is_active",
    )

    search_fields = (
        "register_number",
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "department",
        "year",
        "section",
        "is_active",
    )


# ============================================================
# TEAM
# ============================================================

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team_leader",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "team_leader__register_number",
        "team_leader__first_name",
        "team_leader__last_name",
    )

    list_filter = (
        "is_active",
    )


# ============================================================
# TEAM MEMBER
# ============================================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "student",
        "role",
        "joined_date",
        "is_active",
    )

    search_fields = (
        "team__name",
        "student__register_number",
        "student__first_name",
        "student__last_name",
    )

    list_filter = (
        "role",
        "is_active",
        "team",
    )


# ============================================================
# PROJECT
# ============================================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "team",
        "category",
        "development_level",
        "current_status",
        "updated_at",
    )

    search_fields = (
        "title",
        "category",
        "team__name",
    )

    list_filter = (
        "development_level",
        "current_status",
        "category",
    )


# ============================================================
# IIC MEMBERSHIP
# ============================================================

@admin.register(IICMembership)
class IICMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "membership_number",
        "student",
        "membership_type",
        "joined_date",
        "status",
    )

    search_fields = (
        "membership_number",
        "student__register_number",
        "student__first_name",
    )

    list_filter = (
        "membership_type",
        "status",
    )


# ============================================================
# EVENT
# ============================================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_type",
        "event_date",
        "venue",
        "registration_required",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "venue",
    )

    list_filter = (
        "event_type",
        "event_date",
        "registration_required",
        "is_active",
    )

    ordering = (
        "-event_date",
    )


# ============================================================
# EVENT REGISTRATION
# ============================================================

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "event",
        "registration_date",
        "status",
        "certificate_eligible",
    )

    search_fields = (
        "student__register_number",
        "student__first_name",
        "student__last_name",
        "event__title",
    )

    list_filter = (
        "status",
        "certificate_eligible",
        "event",
    )


# ============================================================
# EXTERNAL VENTURE
# ============================================================

@admin.register(ExternalVenture)
class ExternalVentureAdmin(admin.ModelAdmin):
    list_display = (
        "venture_id",
        "venture_name",
        "contact_person",
        "email",
        "membership_start",
        "membership_end",
        "membership_fee",
        "status",
        "is_active",
    )

    search_fields = (
        "venture_id",
        "venture_name",
        "contact_person",
        "email",
        "phone",
    )

    list_filter = (
        "status",
        "is_active",
        "industry",
    )


# ============================================================
# EXTERNAL PAYMENT
# ============================================================

@admin.register(ExternalPayment)
class ExternalPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "venture",
        "amount",
        "payment_date",
        "payment_status",
        "transaction_reference",
    )

    search_fields = (
        "venture__venture_name",
        "venture__venture_id",
        "transaction_reference",
    )

    list_filter = (
        "payment_status",
        "payment_date",
    )


# ============================================================
# ATTENDANCE
# ============================================================

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "student",
        "external_venture",
        "date",
        "status",
    )

    search_fields = (
        "event__title",
        "student__register_number",
        "student__first_name",
        "student__last_name",
        "external_venture__venture_name",
    )

    list_filter = (
        "status",
        "event",
        "date",
    )


# ============================================================
# DAILY PROGRESS
# ============================================================

@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "date",
        "activity",
        "progress_percentage",
        "created_at",
    )

    search_fields = (
        "team__name",
        "team__project__title",
        "activity",
        "work_completed",
    )

    list_filter = (
        "date",
        "team",
    )

    ordering = (
        "-date",
    )
# ============================================================
# EXTERNAL EVENT
# ============================================================

@admin.register(ExternalEvent)
class ExternalEventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organizing_college",
        "event_type",
        "event_date",
        "venue",
    )

    search_fields = (
        "title",
        "organizing_college",
        "venue",
        "description",
    )

    list_filter = (
        "event_type",
        "event_date",
    )

    ordering = (
        "-event_date",
    )
# ============================================================
# STUDENT ACHIEVEMENT
# ============================================================

@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "event",
        "result",
        "prize_name",
        "prize_amount",
        "created_at",
    )

    search_fields = (
        "student__register_number",
        "student__first_name",
        "student__last_name",
        "event__title",
        "event__organizing_college",
        "prize_name",
    )

    list_filter = (
        "result",
        "event",
    )

    ordering = (
        "-created_at",
    )