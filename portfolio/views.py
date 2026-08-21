from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, JsonResponse
from django.db.models import Prefetch
from .models import (
    PersonalInfo, SocialLink, SkillCategory, Skill,
    Project, ProjectTechnology, ProjectFeature, ProjectStatistic,
    Experience, Education, Certification, Achievement, SiteSettings
)


def get_common_context():
    personal_info = PersonalInfo.get_solo()
    site_settings = SiteSettings.get_solo()
    social_links = SocialLink.objects.filter(is_active=True)
    return {
        'personal_info': personal_info,
        'site_settings': site_settings,
        'social_links': social_links,
    }


def home_view(request):
    context = get_common_context()

    # Active skills grouped by category
    active_skills_prefetch = Prefetch(
        'skills',
        queryset=Skill.objects.filter(is_active=True).order_by('display_order', 'name'),
        to_attr='active_skills'
    )
    skill_categories = SkillCategory.objects.prefetch_related(active_skills_prefetch).order_by('display_order', 'name')

    # Filter out categories that have no active skills
    skill_categories = [cat for cat in skill_categories if getattr(cat, 'active_skills', [])]

    # Active Projects with related data
    projects = Project.objects.filter(is_active=True).prefetch_related(
        Prefetch('technologies', queryset=ProjectTechnology.objects.order_by('display_order')),
        Prefetch('features', queryset=ProjectFeature.objects.order_by('display_order')),
        Prefetch('statistics', queryset=ProjectStatistic.objects.order_by('display_order'))
    ).order_by('display_order', '-created_at')

    # Other section data
    experiences = Experience.objects.filter(is_active=True).order_by('display_order', 'id')
    education_list = Education.objects.filter(is_active=True).order_by('display_order', 'id')
    certifications = Certification.objects.filter(is_active=True).order_by('display_order', 'id')
    achievements = Achievement.objects.filter(is_active=True).order_by('display_order', 'id')

    context.update({
        'skill_categories': skill_categories,
        'projects': projects,
        'experiences': experiences,
        'education_list': education_list,
        'certifications': certifications,
        'achievements': achievements,
    })

    return render(request, 'home.html', context)


def project_detail_view(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            'technologies', 'features', 'statistics'
        ),
        slug=slug,
        is_active=True
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        data = {
            'id': project.id,
            'title': project.title,
            'category': project.category,
            'short_description': project.short_description,
            'detailed_description': project.detailed_description,
            'problem_statement': project.problem_statement,
            'solution_statement': project.solution_statement,
            'project_image': project.project_image.url if project.project_image else '',
            'github_url': project.github_url,
            'live_demo_url': project.live_demo_url,
            'technologies': [t.name for t in project.technologies.all()],
            'features': [f.feature for f in project.features.all()],
            'statistics': [{'label': s.label, 'value': s.value} for s in project.statistics.all()],
        }
        return JsonResponse(data)

    context = get_common_context()
    context['project'] = project
    return render(request, 'project_detail.html', context)


def resume_view(request):
    personal_info = PersonalInfo.get_solo()
    if personal_info and personal_info.resume_file:
        try:
            return FileResponse(personal_info.resume_file.open(), content_type='application/pdf')
        except Exception:
            pass

    context = get_common_context()
    return render(request, 'resume.html', context)


def custom_404_view(request, exception=None):
    context = get_common_context()
    return render(request, '404.html', context, status=404)


def custom_500_view(request):
    context = get_common_context()
    return render(request, '500.html', context, status=500)
