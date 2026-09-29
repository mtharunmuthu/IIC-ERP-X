from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from .models import (
    Student,
    Department,
    Event,
    ExternalEvent,
    StudentAchievement,
    Team,
    TeamMember,
    Project,
    DailyProgress,
    DailyAttendance,
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
# ERP LOGIN
# ============================================================

def erp_login(request):

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
                is_active=True
            )

            request.session["student_id"] = student.id

            return redirect(
                "student_dashboard"
            )

        except Student.DoesNotExist:

            return render(
                request,
                "iic/erp_login.html",
                {
                    "error":
                        "Invalid Registration Number or Date of Birth."
                }
            )

    return render(
        request,
        "iic/erp_login.html"
    )


# ============================================================
# STUDENT REGISTRATION
# ============================================================

def student_register(request):

    departments = (
        Department.objects
        .filter(is_active=True)
        .order_by("name")
    )

    if request.method == "POST":

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
        # VALIDATION
        # ----------------------------------------------------

        if not date_of_birth:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your Date of Birth."
                }
            )

        if not first_name:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your First Name."
                }
            )

        if not email:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your Email."
                }
            )

        if not phone:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your Phone Number."
                }
            )

        if not department_id:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please select your Department."
                }
            )

        if not year:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please select your Year."
                }
            )

        if not admission_year:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your Admission Year."
                }
            )

        if not graduation_year:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please enter your Graduation Year."
                }
            )

        # ----------------------------------------------------
        # CHECK DUPLICATE EMAIL
        # ----------------------------------------------------

        if Student.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "This email address is already registered."
                }
            )

        # ----------------------------------------------------
        # GET DEPARTMENT
        # ----------------------------------------------------

        try:

            department = Department.objects.get(
                id=department_id,
                is_active=True
            )

        except Department.DoesNotExist:

            return render(
                request,
                "iic/student_register.html",
                {
                    "departments": departments,
                    "error":
                        "Please select a valid department."
                }
            )

        # ====================================================
        # AUTO GENERATE REGISTRATION NUMBER
        # ====================================================

        prefix = f"IIC{admission_year}"

        existing_numbers = (
            Student.objects
            .filter(
                register_number__startswith=prefix
            )
            .values_list(
                "register_number",
                flat=True
            )
        )

        highest_number = 0

        for number in existing_numbers:

            try:

                sequence = int(
                    number[len(prefix):]
                )

                if sequence > highest_number:
                    highest_number = sequence

            except (
                ValueError,
                TypeError
            ):

                continue

        next_number = highest_number + 1

        register_number = (
            f"{prefix}{next_number:04d}"
        )

        # ====================================================
        # CREATE STUDENT
        # ====================================================

        student = Student.objects.create(

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

        # ====================================================
        # SHOW GENERATED NUMBER
        # ====================================================

        return render(
            request,
            "iic/student_register.html",
            {
                "departments": departments,
                "success": True,
                "generated_register_number":
                    register_number,
                "student": student,
            }
        )

    return render(
        request,
        "iic/student_register.html",
        {
            "departments": departments
        }
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
                is_active=True
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
                    "error":
                        "Invalid Registration Number or Date of Birth."
                }
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

        student = (
            Student.objects
            .select_related("department")
            .get(
                id=student_id,
                is_active=True
            )
        )

    except Student.DoesNotExist:

        request.session.flush()

        return redirect(
            "student_login"
        )

    today = timezone.localdate()

    today_attendance = (
        DailyAttendance.objects
        .filter(
            student=student,
            date=today
        )
        .first()
    )

    return render(
        request,
        "iic/student_dashboard.html",
        {
            "student":
                student,

            "today_attendance":
                today_attendance,
        }
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

    student_count = (
        Student.objects
        .filter(is_active=True)
        .count()
    )

    event_count = (
        Event.objects
        .filter(is_active=True)
        .count()
    )

    external_event_count = (
        ExternalEvent.objects.count()
    )

    achievement_count = (
        StudentAchievement.objects.count()
    )

    team_count = (
        Team.objects
        .filter(is_active=True)
        .count()
    )

    project_count = (
        Project.objects.count()
    )

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

    upcoming_events = (
        ExternalEvent.objects
        .order_by(
            "event_date"
        )[:5]
    )

    context = {

        "student_count":
            student_count,

        "event_count":
            event_count,

        "external_event_count":
            external_event_count,

        "achievement_count":
            achievement_count,

        "team_count":
            team_count,

        "project_count":
            project_count,

        "recent_achievements":
            recent_achievements,

        "upcoming_events":
            upcoming_events,
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
        .filter(
            is_active=True
        )
        .order_by(
            "register_number"
        )
    )

    context = {

        "students":
            students,

        "student_count":
            students.count(),
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
        .order_by(
            "-event_date"
        )
    )

    context = {

        "events":
            events,

        "event_count":
            events.count(),
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
        .order_by(
            "-created_at"
        )
    )

    context = {

        "achievements":
            achievements,

        "achievement_count":
            achievements.count(),
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
        .filter(
            is_active=True
        )
        .order_by(
            "name"
        )
    )

    context = {

        "teams":
            teams,

        "team_count":
            teams.count(),
    }

    return render(
        request,
        "iic/iic_admin_teams.html",
        context
    )


# ============================================================
# IIC ADMIN - TEAM DETAILS
# ============================================================

@staff_member_required
def iic_admin_team_details(
    request,
    team_id
):

    team = get_object_or_404(

        Team.objects
        .select_related(
            "team_leader",
            "team_leader__department",
            "project"
        )
        .prefetch_related(
            "members__student__department"
        ),

        id=team_id,

        is_active=True
    )

    members = (
        team.members
        .filter(
            is_active=True
        )
        .select_related(
            "student",
            "student__department"
        )
        .order_by(
            "role",
            "student__register_number"
        )
    )

    project = getattr(
        team,
        "project",
        None
    )

    context = {

        "team":
            team,

        "members":
            members,

        "project":
            project,
    }

    return render(
        request,
        "iic/iic_admin_team_details.html",
        context
    )


# ============================================================
# STUDENT - PROTOTYPE / PROJECT REGISTRATION
# ============================================================

def prototype_register(request):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:

        return redirect(
            "student_login"
        )

    # --------------------------------------------------------
    # GET CURRENT STUDENT
    # --------------------------------------------------------

    try:

        student = (
            Student.objects
            .select_related("department")
            .get(
                id=student_id,
                is_active=True
            )
        )

    except Student.DoesNotExist:

        request.session.flush()

        return redirect(
            "student_login"
        )

    # --------------------------------------------------------
    # CHECK WHETHER STUDENT IS ALREADY IN AN ACTIVE TEAM
    # --------------------------------------------------------

    existing_membership = (
        TeamMember.objects
        .filter(
            student=student,
            is_active=True,
            team__is_active=True
        )
        .select_related(
            "team"
        )
        .first()
    )

    if existing_membership:

        return render(
            request,
            "iic/prototype_register.html",
            {
                "student":
                    student,

                "existing_team":
                    existing_membership.team,

                "error":
                    "You are already registered in an active team."
            }
        )

    # --------------------------------------------------------
    # FUNCTION TO GET AVAILABLE STUDENTS
    # --------------------------------------------------------

    def get_available_students():

        students_already_in_team = (
            TeamMember.objects
            .filter(
                is_active=True,
                team__is_active=True
            )
            .values_list(
                "student_id",
                flat=True
            )
        )

        return (
            Student.objects
            .filter(
                is_active=True
            )
            .exclude(
                id=student.id
            )
            .exclude(
                id__in=students_already_in_team
            )
            .select_related(
                "department"
            )
            .order_by(
                "register_number"
            )
        )

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    if request.method == "POST":

        team_type = request.POST.get(
            "team_type",
            ""
        ).strip().upper()

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
        ).strip()

        member_ids = request.POST.getlist(
            "members"
        )

        # ====================================================
        # VALIDATE SOLO / TEAM
        # ====================================================

        if team_type not in [
            "SOLO",
            "TEAM"
        ]:

            return render(
                request,
                "iic/prototype_register.html",
                {
                    "student":
                        student,

                    "students":
                        get_available_students(),

                    "error":
                        "Please select whether your project is Solo or Team."
                }
            )

        # ====================================================
        # VALIDATE TEAM NAME
        # ====================================================

        if not team_name:

            return render(
                request,
                "iic/prototype_register.html",
                {
                    "student":
                        student,

                    "students":
                        get_available_students(),

                    "error":
                        "Please enter a team name."
                }
            )

        # ====================================================
        # CHECK DUPLICATE TEAM NAME
        # ====================================================

        if Team.objects.filter(
            name=team_name
        ).exists():

            return render(
                request,
                "iic/prototype_register.html",
                {
                    "student":
                        student,

                    "students":
                        get_available_students(),

                    "error":
                        (
                            f'The team name "{team_name}" '
                            "is already used. "
                            "Please choose a different team name."
                        )
                }
            )

        # ====================================================
        # VALIDATE PROJECT TITLE
        # ====================================================

        if not project_title:

            return render(
                request,
                "iic/prototype_register.html",
                {
                    "student":
                        student,

                    "students":
                        get_available_students(),

                    "error":
                        "Please enter the project title."
                }
            )

        # ====================================================
        # SOLO PROJECT
        # ====================================================

        if team_type == "SOLO":

            member_ids = []

        # ====================================================
        # TEAM PROJECT
        # ====================================================

        if team_type == "TEAM":

            # Remove empty values

            member_ids = [
                member_id
                for member_id in member_ids
                if member_id
            ]

            # Remove duplicates

            member_ids = list(
                dict.fromkeys(
                    member_ids
                )
            )

            # ------------------------------------------------
            # TEAM MUST HAVE AT LEAST ONE OTHER MEMBER
            # ------------------------------------------------

            if not member_ids:

                return render(
                    request,
                    "iic/prototype_register.html",
                    {
                        "student":
                            student,

                        "students":
                            get_available_students(),

                        "error":
                            (
                                "Please add at least one team member. "
                                "If you are working alone, select Solo."
                            )
                    }
                )

            # ------------------------------------------------
            # GET SELECTED MEMBERS
            # ------------------------------------------------

            selected_members = list(
                Student.objects
                .filter(
                    id__in=member_ids,
                    is_active=True
                )
                .select_related(
                    "department"
                )
            )

            # ------------------------------------------------
            # VALIDATE ALL MEMBERS
            # ------------------------------------------------

            if len(selected_members) != len(member_ids):

                return render(
                    request,
                    "iic/prototype_register.html",
                    {
                        "student":
                            student,

                        "students":
                            get_available_students(),

                        "error":
                            "One or more selected team members are invalid."
                    }
                )

            # ------------------------------------------------
            # CHECK WHETHER MEMBERS ARE ALREADY IN A TEAM
            # ------------------------------------------------

            already_registered_member = (
                TeamMember.objects
                .filter(
                    student__in=selected_members,
                    is_active=True,
                    team__is_active=True
                )
                .select_related(
                    "student",
                    "team"
                )
                .first()
            )

            if already_registered_member:

                member = (
                    already_registered_member.student
                )

                return render(
                    request,
                    "iic/prototype_register.html",
                    {
                        "student":
                            student,

                        "students":
                            get_available_students(),

                        "error":
                            (
                                f"{member.first_name} "
                                f"{member.last_name} "
                                f"({member.register_number}) "
                                "is already registered in another active team."
                            )
                    }
                )

        # ====================================================
        # CREATE TEAM
        # ====================================================

        team = Team.objects.create(

            name=team_name,

            description=description,

            team_leader=student,

            is_active=True
        )

        # ====================================================
        # ADD CURRENT STUDENT AS LEADER
        # ====================================================

        TeamMember.objects.create(

            team=team,

            student=student,

            role="LEADER",

            is_active=True
        )

        # ====================================================
        # ADD OTHER MEMBERS
        # ====================================================

        if team_type == "TEAM":

            for member in selected_members:

                TeamMember.objects.create(

                    team=team,

                    student=member,

                    role="MEMBER",

                    is_active=True
                )

        # ====================================================
        # CREATE PROJECT
        # ====================================================

        Project.objects.create(

            team=team,

            title=project_title,

            category=category,

            problem_statement=problem_statement,

            description=description,

            development_level=
                development_level,

            current_status=
                "NOT_STARTED"
        )

        # ====================================================
        # SUCCESS
        # ====================================================

        return redirect(
            "student_dashboard"
        )

    # --------------------------------------------------------
    # GET REQUEST
    # --------------------------------------------------------

    students = get_available_students()

    return render(
        request,
        "iic/prototype_register.html",
        {
            "student":
                student,

            "students":
                students,
        }
    )


# ============================================================
# STUDENT - DAILY ATTENDANCE
# ============================================================

def punch_attendance(request):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:

        return redirect(
            "student_login"
        )

    try:

        student = Student.objects.get(
            id=student_id,
            is_active=True
        )

    except Student.DoesNotExist:

        request.session.flush()

        return redirect(
            "student_login"
        )

    today = timezone.localdate()

    current_time = (
        timezone.localtime().time()
    )

    attendance, created = (
        DailyAttendance.objects
        .get_or_create(

            student=student,

            date=today,

            defaults={
                "status":
                    "PRESENT",

                "punch_time":
                    current_time,
            }
        )
    )

    if (
        not created
        and attendance.status != "PRESENT"
    ):

        attendance.status = "PRESENT"

        attendance.punch_time = current_time

        attendance.save()

    return redirect(
        "student_dashboard"
    )


# ============================================================
# IIC ADMIN - DAILY ATTENDANCE
# ============================================================

@staff_member_required
def iic_admin_attendance(request):

    today = timezone.localdate()

    students = (
        Student.objects
        .filter(
            is_active=True
        )
        .select_related(
            "department"
        )
        .order_by(
            "register_number"
        )
    )

    attendance = (
        DailyAttendance.objects
        .filter(
            date=today
        )
        .select_related(
            "student"
        )
    )

    attendance_map = {

        record.student_id:
            record

        for record in attendance
    }

    attendance_rows = []

    for student in students:

        record = attendance_map.get(
            student.id
        )

        attendance_rows.append({

            "student":
                student,

            "attendance":
                record,
        })

    return render(

        request,

        "iic/iic_admin_attendance.html",

        {
            "attendance_rows":
                attendance_rows,

            "today":
                today,
        }
    )
# ============================================================
# IIC ADMIN - STUDENT DETAILS
# ============================================================

@staff_member_required
def iic_admin_student_details(request, student_id):

    student = get_object_or_404(
        Student.objects.select_related(
            "department"
        ),
        id=student_id,
        is_active=True
    )

    # All active teams this student belongs to
    team_memberships = (
        TeamMember.objects
        .filter(
            student=student,
            is_active=True,
            team__is_active=True
        )
        .select_related(
            "team",
            "team__team_leader",
            "team__project"
        )
    )

    teams = []

    for membership in team_memberships:

        team = membership.team

        members = (
            TeamMember.objects
            .filter(
                team=team,
                is_active=True
            )
            .select_related(
                "student",
                "student__department"
            )
            .order_by(
                "role",
                "student__register_number"
            )
        )

        project = getattr(
            team,
            "project",
            None
        )

        teams.append({
            "team": team,
            "membership": membership,
            "members": members,
            "project": project,
        })

    # Student attendance
    attendance = (
        DailyAttendance.objects
        .filter(
            student=student
        )
        .order_by(
            "-date"
        )
    )

    # Student project progress through their teams
    progress = (
        DailyProgress.objects
        .filter(
            team__members__student=student,
            team__members__is_active=True,
            team__is_active=True
        )
        .select_related(
            "team"
        )
        .distinct()
        .order_by(
            "-date"
        )
    )

    context = {
        "student": student,
        "teams": teams,
        "attendance": attendance,
        "progress": progress,
    }

    return render(
        request,
        "iic/iic_admin_student_details.html",
        context
    )