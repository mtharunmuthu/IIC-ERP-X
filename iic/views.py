from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .models import (
    Student,
    Department,
    Event,
    ExternalEvent,
    StudentAchievement,
    Team,
    TeamMember,
    Project,
)

# ============================================================
# HOME
# ============================================================

def home(request):
    return render(
        request,
        "iic/home.html"
    )


# ============================================================
# STUDENT REGISTRATION
# ============================================================

def student_register(request):

    departments = Department.objects.all()

    if request.method == "POST":

        register_number = request.POST.get(
            "register_number",
            ""
        ).strip()

        date_of_birth = request.POST.get(
            "date_of_birth",
            ""
        ).strip()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        department_id = request.POST.get(
            "department"
        )

        year = request.POST.get(
            "year"
        )

        section = request.POST.get(
            "section",
            ""
        ).strip()

        admission_year = request.POST.get(
            "admission_year"
        )

        graduation_year = request.POST.get(
            "graduation_year"
        )

        # ----------------------------------------------------
        # CHECK DUPLICATE REGISTRATION NUMBER
        # ----------------------------------------------------

        if Student.objects.filter(
            register_number=register_number
        ).exists():

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error": (
                        "This Registration Number is already "
                        "registered. Please use your own "
                        "Registration Number."
                    ),
                },
            )

        try:

            department = Department.objects.get(
                id=department_id
            )

            Student.objects.create(
                register_number=register_number,
                date_of_birth=date_of_birth,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department=department,
                year=year,
                section=section,
                admission_year=admission_year,
                graduation_year=graduation_year,
            )

            return redirect(
                "student_login"
            )

        except Department.DoesNotExist:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error": (
                        "Please select a valid department."
                    ),
                },
            )

    return render(
        request,
        "iic/student_register.html",
        {
            "departments": departments
        },
    )


# ============================================================
# STUDENT LOGIN
# ============================================================

def student_login(request):

    if request.method == "POST":

        register_number = request.POST.get(
            "register_number",
            ""
        ).strip()

        date_of_birth = request.POST.get(
            "date_of_birth",
            ""
        ).strip()

        try:

            student = Student.objects.get(
                register_number=register_number,
                date_of_birth=date_of_birth,
                is_active=True,
            )

            request.session["student_id"] = student.id

            return redirect(
                "student_dashboard"
            )

        except Student.DoesNotExist:

            return render(
                request,
                "iic/student_login.html",
                {
                    "error": (
                        "Invalid Registration Number "
                        "or Date of Birth."
                    )
                },
            )

    return render(
        request,
        "iic/student_login.html"
    )


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard(request):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:

        return redirect(
            "student_login"
        )

    try:

        student = Student.objects.select_related(
            "department"
        ).get(
            id=student_id,
            is_active=True,
        )

    except Student.DoesNotExist:

        request.session.flush()

        return redirect(
            "student_login"
        )

    return render(
        request,
        "iic/student_dashboard.html",
        {
            "student": student
        },
    )


# ============================================================
# STUDENT LOGOUT
# ============================================================

def student_logout(request):

    request.session.flush()

    return redirect(
        "home"
    )


# ============================================================
# IIC ADMIN DASHBOARD
# ============================================================

@staff_member_required
def iic_admin_dashboard(request):

    # --------------------------------------------------------
    # DASHBOARD COUNTS
    # --------------------------------------------------------

    student_count = Student.objects.filter(
        is_active=True
    ).count()

    event_count = Event.objects.filter(
        is_active=True
    ).count()

    external_event_count = ExternalEvent.objects.count()

    achievement_count = StudentAchievement.objects.count()

    team_count = Team.objects.filter(
        is_active=True
    ).count()

    project_count = Project.objects.count()

    # --------------------------------------------------------
    # RECENT ACHIEVEMENTS
    # --------------------------------------------------------

    recent_achievements = (
        StudentAchievement.objects
        .select_related(
            "student",
            "event"
        )
        .order_by(
            "-created_at"
        )[:5]
    )

    # --------------------------------------------------------
    # UPCOMING EXTERNAL EVENTS
    # --------------------------------------------------------

    upcoming_events = (
        ExternalEvent.objects
        .order_by(
            "event_date"
        )[:5]
    )

    # --------------------------------------------------------
    # DASHBOARD CONTEXT
    # --------------------------------------------------------

    context = {

        "student_count": student_count,

        "event_count": event_count,

        "external_event_count": external_event_count,

        "achievement_count": achievement_count,

        "team_count": team_count,

        "project_count": project_count,

        "recent_achievements": recent_achievements,

        "upcoming_events": upcoming_events,

    }

    return render(
        request,
        "iic/iic_admin_dashboard.html",
        context
    )
# ============================================================
# IIC ADMIN - STUDENTS
# ============================================================

@staff_member_required
def iic_admin_students(request):

    students = (
        Student.objects
        .select_related("department")
        .filter(is_active=True)
        .order_by("register_number")
    )

    context = {
        "students": students,
        "student_count": students.count(),
    }

    return render(
        request,
        "iic/iic_admin_students.html",
        context
    )
# ============================================================
# IIC ADMIN - EXTERNAL EVENTS
# ============================================================

@staff_member_required
def iic_admin_external_events(request):

    events = (
        ExternalEvent.objects
        .order_by("-event_date")
    )

    context = {
        "events": events,
        "event_count": events.count(),
    }

    return render(
        request,
        "iic/iic_admin_external_events.html",
        context
    )
# ============================================================
# IIC ADMIN - ACHIEVEMENTS
# ============================================================

@staff_member_required
def iic_admin_achievements(request):

    achievements = (
        StudentAchievement.objects
        .select_related(
            "student",
            "event"
        )
        .order_by("-created_at")
    )

    context = {
        "achievements": achievements,
        "achievement_count": achievements.count(),
    }

    return render(
        request,
        "iic/iic_admin_achievements.html",
        context
    )
# ============================================================
# IIC ADMIN - TEAMS
# ============================================================

@staff_member_required
def iic_admin_teams(request):

    teams = (
        Team.objects
        .select_related(
            "team_leader",
            "project"
        )
        .prefetch_related(
            "members__student"
        )
        .filter(is_active=True)
        .order_by("name")
    )

    context = {
        "teams": teams,
        "team_count": teams.count(),
    }

    return render(
        request,
        "iic/iic_admin_teams.html",
        context
    )
# ============================================================
# STUDENT - PROTOTYPE / PROJECT REGISTRATION
# ============================================================

def prototype_register(request):

    student_id = request.session.get("student_id")

    # Student must be logged in
    if not student_id:
        return redirect("student_login")

    try:
        student = Student.objects.get(
            id=student_id,
            is_active=True
        )
    except Student.DoesNotExist:
        request.session.flush()
        return redirect("student_login")

    # Check whether this student is already a team leader
    existing_team = Team.objects.filter(
        team_leader=student,
        is_active=True
    ).first()

    # Only team leader can access this page
    if existing_team:
        return render(
            request,
            "iic/prototype_register.html",
            {
                "student": student,
                "error": "You have already registered a team."
            }
        )

    if request.method == "POST":

        team_name = request.POST.get(
            "team_name",
            ""
        ).strip()

        project_title = request.POST.get(
            "project_title",
            ""
        ).strip()

        category = request.POST.get(
            "category",
            ""
        ).strip()

        problem_statement = request.POST.get(
            "problem_statement",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        development_level = request.POST.get(
            "development_level",
            "IDEA"
        )

        member_ids = request.POST.getlist(
            "members"
        )

        # --------------------------------------------
        # BASIC VALIDATION
        # --------------------------------------------

        if not team_name or not project_title:

            return render(
                request,
                "iic/prototype_register.html",
                {
                    "student": student,
                    "students": Student.objects.filter(
                        is_active=True
                    ).exclude(
                        id=student.id
                    ),
                    "error": "Team name and project name are required."
                }
            )

        # --------------------------------------------
        # CREATE TEAM
        # --------------------------------------------

        team = Team.objects.create(
            name=team_name,
            description=description,
            team_leader=student,
            is_active=True
        )

        # --------------------------------------------
        # ADD TEAM LEADER
        # --------------------------------------------

        TeamMember.objects.create(
            team=team,
            student=student,
            role="LEADER",
            is_active=True
        )

        # --------------------------------------------
        # ADD TEAM MEMBERS
        # --------------------------------------------

        for member_id in member_ids:

            try:

                member = Student.objects.get(
                    id=member_id,
                    is_active=True
                )

                if member.id != student.id:

                    TeamMember.objects.create(
                        team=team,
                        student=member,
                        role="MEMBER",
                        is_active=True
                    )

            except Student.DoesNotExist:
                continue

        # --------------------------------------------
        # CREATE PROJECT
        # --------------------------------------------

        Project.objects.create(
            team=team,
            title=project_title,
            category=category,
            problem_statement=problem_statement,
            description=description,
            development_level=development_level,
            current_status="NOT_STARTED"
        )

        # --------------------------------------------
        # RETURN TO STUDENT DASHBOARD
        # --------------------------------------------

        return redirect(
            "student_dashboard"
        )

    students = (
        Student.objects
        .filter(is_active=True)
        .exclude(id=student.id)
        .order_by("register_number")
    )

    return render(
        request,
        "iic/prototype_register.html",
        {
            "student": student,
            "students": students,
        }
    )