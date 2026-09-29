from django.db import models


# ============================================================
# DEPARTMENT
# ============================================================

class Department(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


# ============================================================
# STUDENT
# ============================================================

class Student(models.Model):

    register_number = models.CharField(
        max_length=30,
        unique=True
    )

    date_of_birth = models.DateField()

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students"
    )

    year = models.PositiveSmallIntegerField()

    section = models.CharField(
        max_length=10
    )

    admission_year = models.PositiveIntegerField()

    graduation_year = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["register_number"]

    def __str__(self):
        return f"{self.register_number} - {self.first_name} {self.last_name}"


# ============================================================
# TEAM
# ============================================================

class Team(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    team_leader = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="led_teams",
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# TEAM MEMBERS
# ============================================================

class TeamMember(models.Model):

    ROLE_CHOICES = [
        ("LEADER", "Team Leader"),
        ("MEMBER", "Team Member"),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="team_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="MEMBER"
    )

    joined_date = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "student"],
                name="unique_team_student"
            )
        ]

        ordering = ["team", "student"]

    def __str__(self):
        return f"{self.team.name} - {self.student.register_number}"


# ============================================================
# PROJECT
# ============================================================

class Project(models.Model):

    DEVELOPMENT_LEVEL_CHOICES = [
        ("IDEA", "Idea"),
        ("THEORY", "Theory"),
        ("PROTOTYPE", "Prototype"),
        ("WORKING_PROTOTYPE", "Working Prototype"),
        ("COMPLETED", "Completed"),
    ]

    STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("ON_HOLD", "On Hold"),
        ("COMPLETED", "Completed"),
    ]

    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        related_name="project"
    )

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=150,
        blank=True
    )

    problem_statement = models.TextField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    development_level = models.CharField(
        max_length=30,
        choices=DEVELOPMENT_LEVEL_CHOICES,
        default="IDEA"
    )

    current_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="NOT_STARTED"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.team.name}"


# ============================================================
# IIC MEMBERSHIP
# ============================================================

class IICMembership(models.Model):

    MEMBERSHIP_TYPES = [
        ("CORE", "Core Member"),
        ("ACTIVE", "Active Member"),
        ("GENERAL", "General Member"),
        ("VOLUNTEER", "Volunteer"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="iic_memberships"
    )

    membership_number = models.CharField(
        max_length=50,
        unique=True
    )

    joined_date = models.DateField()

    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_TYPES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.membership_number} - {self.student}"


# ============================================================
# EVENTS
# ============================================================

class Event(models.Model):

    EVENT_TYPES = [
        ("WORKSHOP", "Workshop"),
        ("SEMINAR", "Seminar"),
        ("HACKATHON", "Hackathon"),
        ("COMPETITION", "Competition"),
        ("WEBINAR", "Webinar"),
        ("BOOTCAMP", "Bootcamp"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    venue = models.CharField(
        max_length=200
    )

    registration_required = models.BooleanField(
        default=True
    )

    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return self.title


# ============================================================
# EVENT REGISTRATION
# ============================================================

class EventRegistration(models.Model):

    STATUS_CHOICES = [
        ("REGISTERED", "Registered"),
        ("CANCELLED", "Cancelled"),
        ("ATTENDED", "Attended"),
        ("ABSENT", "Absent"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="event_registrations"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="REGISTERED"
    )

    certificate_eligible = models.BooleanField(
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "event"],
                name="unique_student_event_registration"
            )
        ]

    def __str__(self):
        return f"{self.student.register_number} - {self.event.title}"


# ============================================================
# EXTERNAL VENTURE
# ============================================================

class ExternalVenture(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("INACTIVE", "Inactive"),
    ]

    venture_id = models.CharField(
        max_length=50,
        unique=True
    )

    venture_name = models.CharField(
        max_length=200
    )

    contact_person = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    description = models.TextField(
        blank=True
    )

    industry = models.CharField(
        max_length=150,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    membership_start = models.DateField(
        null=True,
        blank=True
    )

    membership_end = models.DateField(
        null=True,
        blank=True
    )

    space_allocated = models.CharField(
        max_length=150,
        blank=True
    )

    membership_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["venture_name"]

    def __str__(self):
        return f"{self.venture_name} ({self.venture_id})"


# ============================================================
# EXTERNAL VENTURE PAYMENTS
# ============================================================

class ExternalPayment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    venture = models.ForeignKey(
        ExternalVenture,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    transaction_reference = models.CharField(
        max_length=150,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.venture.venture_name} - {self.amount}"


# ============================================================
# ATTENDANCE
# ============================================================

class Attendance(models.Model):

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        null=True,
        blank=True
    )

    external_venture = models.ForeignKey(
        ExternalVenture,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        null=True,
        blank=True
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):

        if self.student:
            person = self.student.register_number

        elif self.external_venture:
            person = self.external_venture.venture_name

        else:
            person = "Unknown"

        return f"{self.event.title} - {person} - {self.status}"


# ============================================================
# DAILY PROJECT PROGRESS
# ============================================================

class DailyProgress(models.Model):

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="daily_progress"
    )

    date = models.DateField()

    activity = models.CharField(
        max_length=200
    )

    work_completed = models.TextField(
        blank=True
    )

    problems = models.TextField(
        blank=True
    )

    next_day_plan = models.TextField(
        blank=True
    )

    progress_percentage = models.PositiveSmallIntegerField(
        default=0
    )

    mentor_remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.team.name} - {self.date}"


# ============================================================
# EXTERNAL EVENTS
# ============================================================

class ExternalEvent(models.Model):

    EVENT_TYPES = [
        ("HACKATHON", "Hackathon"),
        ("COMPETITION", "Competition"),
        ("WORKSHOP", "Workshop"),
        ("SEMINAR", "Seminar"),
        ("CONFERENCE", "Conference"),
        ("QUIZ", "Quiz"),
        ("PAPER_PRESENTATION", "Paper Presentation"),
        ("PROJECT_EXPO", "Project Expo"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    organizing_college = models.CharField(
        max_length=200
    )

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES
    )

    event_date = models.DateField()

    venue = models.CharField(
        max_length=250,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return f"{self.title} - {self.organizing_college}"


# ============================================================
# STUDENT ACHIEVEMENT
# ============================================================

class StudentAchievement(models.Model):

    RESULT_CHOICES = [
        ("PARTICIPATED", "Participated"),
        ("WINNER", "Winner"),
        ("FIRST", "First Prize"),
        ("SECOND", "Second Prize"),
        ("THIRD", "Third Prize"),
        ("RUNNER_UP", "Runner Up"),
        ("SPECIAL", "Special Award"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="achievements"
    )

    event = models.ForeignKey(
        ExternalEvent,
        on_delete=models.CASCADE,
        related_name="achievements"
    )

    result = models.CharField(
        max_length=30,
        choices=RESULT_CHOICES
    )

    prize_name = models.CharField(
        max_length=200,
        blank=True
    )

    prize_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    certificate = models.FileField(
        upload_to="achievement_certificates/",
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.student.register_number} - "
            f"{self.event.title} - {self.result}"
        )


# ============================================================
# DAILY ATTENDANCE
# ============================================================

class DailyAttendance(models.Model):

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="daily_attendance"
    )

    date = models.DateField()

    punch_time = models.TimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ABSENT"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date", "-punch_time"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_daily_attendance"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.register_number} - "
            f"{self.date} - {self.status}"
        )