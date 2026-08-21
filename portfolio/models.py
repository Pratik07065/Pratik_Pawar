from django.db import models
from django.utils.text import slugify


class PersonalInfo(models.Model):
    name = models.CharField(max_length=100, default="Pratik Kautik Pawar")
    professional_title = models.CharField(
        max_length=150,
        default="AI/ML Engineer | GenAI Engineer | Python Developer"
    )
    short_intro = models.CharField(
        max_length=255,
        default="Passionate about building intelligent, data-driven solutions and full-stack AI/ML applications."
    )
    about_text = models.TextField(
        default=(
            "I am a Computer Engineering student (2022–2026) at Savitribai Phule Pune University "
            "with a strong academic foundation (CGPA 8.65/10) and hands-on experience in Machine Learning, "
            "Generative AI, and Python web development. I specialize in building smart applications, predictive models, "
            "and scalable REST APIs."
        )
    )
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(default="pratikpawar7028@gmail.com")
    phone = models.CharField(max_length=30, default="+91-8010966836")
    location = models.CharField(max_length=100, default="Nashik, Maharashtra, India")
    github_url = models.URLField(default="https://github.com/Pratik07065")
    linkedin_url = models.URLField(default="https://linkedin.com/in/pratik-pawar-554bbb283")
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    hero_badge = models.CharField(max_length=100, default="Available for AI/ML & Engineering Roles")
    hero_heading = models.CharField(max_length=200, default="Hi, I'm Pratik Pawar")
    hero_description = models.TextField(
        default="Building intelligent, data-driven and full-stack applications with Machine Learning, Generative AI and Python."
    )
    
    contact_heading = models.CharField(max_length=150, default="Let's Build Something Intelligent")
    contact_description = models.TextField(
        default="Whether you have an opportunity, a project idea, or just want to connect, feel free to reach out!"
    )
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

    def __str__(self):
        return f"{self.name} - {self.professional_title}"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.filter(is_active=True).first()
        if not obj:
            obj = cls.objects.first()
        return obj


class SocialLink(models.Model):
    platform = models.CharField(max_length=50, help_text="e.g. GitHub, LinkedIn, Email, Phone")
    url = models.URLField(help_text="Full URL or mailto:/tel: link")
    icon = models.CharField(max_length=50, help_text="Icon identifier e.g. github, linkedin, mail, phone, code")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.platform


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier or SVG code/class")
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category__display_order', 'display_order', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=100, help_text="e.g. AI / ML + Full Stack, Full Stack Web Application")
    short_description = models.TextField()
    detailed_description = models.TextField(blank=True, help_text="Detailed description of the project architecture and features.")
    problem_statement = models.TextField(blank=True)
    solution_statement = models.TextField(blank=True)
    project_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    project_logo = models.ImageField(upload_to='projects/logos/', blank=True, null=True)
    github_url = models.URLField(blank=True, help_text="Editable GitHub repository link")
    live_demo_url = models.URLField(blank=True, help_text="Editable Live demo link")
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, related_name='technologies', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Project Technology"
        verbose_name_plural = "Project Technologies"

    def __str__(self):
        return f"{self.name} for {self.project.title}"


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, related_name='features', on_delete=models.CASCADE)
    feature = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Project Feature"
        verbose_name_plural = "Project Features"

    def __str__(self):
        return f"Feature for {self.project.title}"


class ProjectStatistic(models.Model):
    project = models.ForeignKey(Project, related_name='statistics', on_delete=models.CASCADE)
    label = models.CharField(max_length=100, help_text="e.g. Yield Prediction")
    value = models.CharField(max_length=50, help_text="e.g. 93%")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Project Statistic"
        verbose_name_plural = "Project Statistics"

    def __str__(self):
        return f"{self.label}: {self.value} ({self.project.title})"


class ProjectAlias(models.Model):
    project = models.ForeignKey(Project, related_name='aliases', on_delete=models.CASCADE)
    alias = models.CharField(max_length=200, help_text="Alternative title or nickname for this project")
    normalized_alias = models.CharField(max_length=200, db_index=True, blank=True)

    class Meta:
        verbose_name = "Project Alias"
        verbose_name_plural = "Project Aliases"

    def __str__(self):
        return f"'{self.alias}' -> {self.project.title}"

    def save(self, *args, **kwargs):
        if self.alias:
            self.normalized_alias = slugify(self.alias).replace('-', '')
        super().save(*args, **kwargs)



class Experience(models.Model):
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, default="Nashik, India")
    start_date = models.CharField(max_length=50, help_text="e.g. January 2025")
    end_date = models.CharField(max_length=50, help_text="e.g. March 2025 or Present")
    description = models.TextField()
    technologies = models.CharField(max_length=255, blank=True, help_text="Comma separated list of technologies")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default="Maharashtra, India")
    start_year = models.CharField(max_length=20)
    end_year = models.CharField(max_length=20)
    grade = models.CharField(max_length=50, help_text="e.g. CGPA: 8.65 / 10 or 91.80%")
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150)
    certificate_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    certificate_url = models.URLField(blank=True, help_text="Optional link to credential/certificate")
    issue_date = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return f"{self.name} ({self.issuer})"


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    value = models.CharField(max_length=50, blank=True, help_text="e.g. 93%, 91%, 13+")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier e.g. trophy, award, check-circle, zap")
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Pratik Pawar | Portfolio")
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    footer_text = models.CharField(max_length=255, default="Building intelligent, data-driven applications.")
    copyright_text = models.CharField(max_length=255, default="© 2026 Pratik Kautik Pawar. All rights reserved.")
    meta_title = models.CharField(
        max_length=200,
        default="Pratik Pawar | AI/ML Engineer | GenAI Engineer | Python Developer"
    )
    meta_description = models.TextField(
        default="Portfolio of Pratik Kautik Pawar, an AI/ML Engineer, GenAI Engineer and Python Developer building Machine Learning, Generative AI and full-stack applications."
    )
    og_image = models.ImageField(upload_to='settings/', blank=True, null=True)
    enable_animations = models.BooleanField(default=True)
    enable_particles = models.BooleanField(default=True)
    enable_cursor_effect = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj
