from django.contrib import admin
from .models import (
    PersonalInfo, SocialLink, SkillCategory, Skill,
    Project, ProjectTechnology, ProjectFeature, ProjectStatistic, ProjectAlias,
    Experience, Education, Certification, Achievement, SiteSettings
)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'professional_title', 'email', 'phone', 'location', 'is_active', 'updated_at')
    fieldsets = (
        ('Header & Identity', {
            'fields': ('name', 'professional_title', 'hero_badge', 'hero_heading', 'hero_description', 'profile_image')
        }),
        ('About & Bio', {
            'fields': ('short_intro', 'about_text')
        }),
        ('Contact & Links', {
            'fields': ('email', 'phone', 'location', 'github_url', 'linkedin_url', 'resume_file', 'contact_heading', 'contact_description')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent multiple PersonalInfo records if one already exists
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'icon', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('platform',)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'display_order', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('display_order', 'is_featured', 'is_active')


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1


class ProjectStatisticInline(admin.TabularInline):
    model = ProjectStatistic
    extra = 1


class ProjectAliasInline(admin.TabularInline):
    model = ProjectAlias
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'display_order', 'is_active', 'updated_at')
    list_filter = ('category', 'featured', 'is_active')
    search_fields = ('title', 'short_description', 'detailed_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'display_order', 'is_active')
    inlines = [ProjectTechnologyInline, ProjectFeatureInline, ProjectStatisticInline, ProjectAliasInline]

    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'category', 'short_description', 'detailed_description', 'featured', 'display_order', 'is_active')
        }),
        ('Case Study Details', {
            'fields': ('problem_statement', 'solution_statement')
        }),
        ('Media & External Links', {
            'fields': ('project_image', 'project_logo', 'github_url', 'live_demo_url')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'start_date', 'end_date', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('job_title', 'company', 'description', 'technologies')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'grade', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('degree', 'institution')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'issue_date', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('name', 'issuer')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon', 'is_featured', 'display_order', 'is_active')
    list_editable = ('is_featured', 'display_order', 'is_active')
    search_fields = ('title', 'description')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'enable_animations', 'enable_particles', 'enable_cursor_effect')

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


# Customize Admin Header & Title
admin.site.site_header = "Pratik Pawar Portfolio Admin"
admin.site.site_title = "Portfolio Management System"
admin.site.index_title = "Manage Portfolio Content & Settings"
