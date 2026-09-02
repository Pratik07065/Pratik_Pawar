import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import (
    PersonalInfo, SocialLink, SkillCategory, Skill,
    Project, ProjectTechnology, ProjectFeature, ProjectStatistic, ProjectAlias,
    Experience, Education, Certification, Achievement, SiteSettings
)


def normalize_string(text):
    if not text:
        return ""
    # Strip all non-alphanumeric characters and lowercase
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()


class Command(BaseCommand):
    help = "Seeds portfolio data safely, merging project duplicates based on canonical titles and alias system."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding portfolio data and deduplicating projects...")

        # 1. Personal Information
        personal_info, _ = PersonalInfo.objects.update_or_create(
            id=1,
            defaults={
                "name": "Pratik Kautik Pawar",
                "professional_title": "AI/ML Engineer | GenAI Engineer | Python Developer",
                "short_intro": "Results-driven AI/ML Engineer and Python Developer building production-grade ML models and full-stack AI solutions.",
                "about_text": (
                    "I'm a Computer Engineering student and aspiring AI/ML Engineer passionate about building intelligent, practical and user-focused software solutions.\n\n"
                    "My interests span Machine Learning, Generative AI, Python development, Data Science and full-stack web development. I enjoy transforming ideas into working applications by combining machine learning models, APIs, databases and modern frontend technologies."
                ),
                "email": "pratikpawar7028@email.com",
                "phone": "+91-8010966836",
                "location": "Nashik, Maharashtra, India",
                "github_url": "https://github.com/Pratik07065",
                "linkedin_url": "https://linkedin.com/in/pratik-pawar-554bbb283",
                "hero_badge": "AI/ML Engineer • GenAI Engineer • Python Developer",
                "hero_heading": "Building Intelligent Solutions With AI.",
                "hero_description": "AI/ML Engineer and Python Developer building intelligent, data-driven and full-stack applications using Machine Learning, Generative AI, Python and modern web technologies.",
                "contact_heading": "Let's Build Something Intelligent.",
                "contact_description": "I'm open to opportunities, collaborations, internships and interesting projects in AI/ML, GenAI and software development.",
                "is_active": True
            }
        )

        # 2. Social Links
        SocialLink.objects.all().update(is_active=False)
        socials_data = [
            ("GitHub", "https://github.com/Pratik07065", "github", 1),
            ("LinkedIn", "https://linkedin.com/in/pratik-pawar-554bbb283", "linkedin", 2),
            ("Email", "mailto:pratikpawar7028@email.com", "mail", 3),
        ]
        for platform, url, icon, order in socials_data:
            SocialLink.objects.update_or_create(
                platform=platform,
                defaults={"url": url, "icon": icon, "display_order": order, "is_active": True}
            )

        # 3. Skill Categories & Skills
        skills_structure = {
            "Programming": (1, [
                ("Python", "Primary programming language used for backend development, Machine Learning and AI applications.", "code-2", True),
                ("JavaScript", "Used for interactive web applications and frontend development.", "file-code", True),
                ("C++", "Programming language used for problem solving and fundamental programming concepts.", "terminal", False),
            ]),
            "Frontend": (2, [
                ("HTML5", "Semantic and structured web development.", "layout", False),
                ("CSS3", "Responsive layouts, styling and modern interface design.", "palette", False),
                ("ReactJS", "Component-based frontend application development.", "atom", True),
                ("React Router", "Client-side routing for React applications.", "git-branch", False),
                ("API Integration", "Connecting frontend applications with backend REST APIs.", "network", True),
            ]),
            "Backend": (3, [
                ("Python Flask", "Lightweight Python backend and REST API development.", "server", True),
                ("Django", "Python web application development and database-driven applications.", "shield", True),
                ("Django REST Framework", "Building RESTful APIs with Django.", "layers", True),
                ("FastAPI", "Modern Python API development.", "zap", True),
                ("REST APIs", "Backend communication between frontend applications and services.", "cpu", False),
            ]),
            "Machine Learning": (4, [
                ("NumPy", "Numerical computing & array operations.", "calculator", False),
                ("Pandas", "Data manipulation & analytical workflows.", "table", False),
                ("Matplotlib", "Data visualization & plotting.", "bar-chart-2", False),
                ("Scikit-Learn", "Supervised/unsupervised ML algorithms.", "brain-circuit", True),
                ("Random Forest", "Ensemble decision tree modeling.", "git-fork", True),
                ("XGBoost", "Gradient boosted decision trees.", "trending-up", True),
                ("Machine Learning", "End-to-end model training & evaluation.", "cpu", True),
                ("Deep Learning Fundamentals", "Neural networks & architectures.", "activity", False),
                ("NLP Fundamentals", "Text processing & feature extraction.", "message-square", False),
            ]),
            "Generative AI": (5, [
                ("Prompt Engineering", "Optimizing LLM inputs and instruction sets.", "sparkles", True),
                ("LLM Fundamentals", "Architecture & integration of language models.", "bot", True),
                ("Generative AI", "Generative workflows and AI integration.", "wand-2", True),
            ]),
            "Databases": (6, [
                ("MongoDB", "NoSQL document store.", "database", True),
                ("SQL", "Relational database querying and modeling.", "database", True),
            ]),
            "Tools": (7, [
                ("Git", "Version control system.", "git-commit", False),
                ("GitHub", "Collaborative code hosting.", "github", False),
                ("Postman", "API testing & documentation.", "send", False),
                ("Docker", "Containerization basics.", "box", False),
                ("Google Colab", "Cloud GPU model training.", "cloud", False),
                ("Power BI", "Business intelligence dashboards.", "pie-chart", True),
                ("Excel", "Data analysis & spreadsheet functions.", "file-spreadsheet", False),
            ])
        }

        Skill.objects.all().update(is_active=False)
        for cat_name, (cat_order, skills_list) in skills_structure.items():
            category, _ = SkillCategory.objects.update_or_create(
                name=cat_name,
                defaults={"display_order": cat_order}
            )

            skill_order = 1
            for s_name, desc, icon, featured in skills_list:
                Skill.objects.update_or_create(
                    category=category,
                    name=s_name,
                    defaults={
                        "description": desc,
                        "icon": icon,
                        "display_order": skill_order,
                        "is_featured": featured,
                        "is_active": True
                    }
                )
                skill_order += 1

        # 4. Canonical Projects Specs
        projects_specs = [
            {
                "title": "FarmEra – AI-Driven Smart Farming Platform",
                "slug": "farmera-ai-driven-smart-farming-platform",
                "aliases": [
                    "FarmEra", "FarmEra – Farming using AI & ML", "FarmEra AI",
                    "AI-Driven Smart Farming Platform", "Smart Agriculture Platform",
                    "FarmEra Smart Farming", "farmera-ai-smart-farming"
                ],
                "category": "AI / ML + Full Stack",
                "short_description": "An AI-driven smart farming platform designed to support farmers from crop planning to market access through intelligent prediction, disease detection and digital marketplace features.",
                "detailed_description": "FarmEra is a full-stack AgriTech platform designed to provide intelligent decision support for farmers. The platform combines Machine Learning, REST APIs and a ReactJS frontend to provide crop yield prediction, price forecasting, disease detection, an AI chatbot and a farmer-merchant marketplace.",
                "problem_statement": "Farmers face unpredictable crop yields, market price fluctuations, and plant diseases without accessible digital advice or direct merchant connection.",
                "solution_statement": "FarmEra delivers real-time predictive analytics, AI disease diagnosis, an automated chatbot assistant, and a direct digital marketplace to maximize agricultural yields and profits.",
                "github_url": "",
                "live_demo_url": "",
                "featured": True,
                "display_order": 1,
                "technologies": ["Python", "Flask", "MongoDB", "Machine Learning", "ReactJS", "HTML", "CSS", "JavaScript"],
                "features": ["Crop Yield Prediction", "Crop Price Forecasting", "Disease Detection", "AI Chatbot", "Farmer-Merchant Marketplace"],
                "statistics": [("Crop Yield Prediction", "93%"), ("Disease Detection", "91%"), ("Disease Classes", "13"), ("Intelligent Modules", "5")]
            },
            {
                "title": "Tourism Arrangement System",
                "slug": "tourism-arrangement-system",
                "aliases": [
                    "Tourism Arrangement System", "Tourism Management System", "Tourism Web Application"
                ],
                "category": "Full Stack Web Application",
                "short_description": "A comprehensive tourism management web application featuring an intuitive interface, dynamic information management and a streamlined booking workflow.",
                "detailed_description": "Developed a tourism management web application with an intuitive user interface, dynamic information management and streamlined booking workflow. Implemented CRUD operations with MySQL and Flask REST APIs to enable real-time data updates.",
                "problem_statement": "Legacy travel booking setups suffer from poor UI responsiveness, manual booking verification, and disconnected database records.",
                "solution_statement": "Created a responsive web platform with automated booking workflows, robust MySQL data relationships, and intuitive user dashboards.",
                "github_url": "",
                "live_demo_url": "",
                "featured": True,
                "display_order": 2,
                "technologies": ["HTML", "CSS", "JavaScript", "Flask", "MySQL"],
                "features": ["Tourism information management", "Booking workflow", "Dynamic information management", "CRUD operations", "Flask REST APIs", "MySQL database", "Responsive user interface"],
                "statistics": [("Booking Efficiency", "100%"), ("Database Operations", "CRUD"), ("REST Endpoints", "Modular")]
            },
            {
                "title": "Secure Voter Verification System",
                "slug": "secure-voter-verification-system",
                "aliases": [
                    "Secure Voter Verification System", "Voter Verification System", "Voter Verification Web Application"
                ],
                "category": "Full Stack Web Application",
                "short_description": "A secure voter verification web application with a responsive dashboard, real-time voter search and SQLite-based record management.",
                "detailed_description": "Built a secure voter verification web application featuring a responsive dashboard, real-time voter search and SQLite-based record management to streamline voter verification and improve authentication efficiency.",
                "problem_statement": "Unsecured or slow voter record checks risk duplication, lookup delays, and authentication bottlenecks.",
                "solution_statement": "Engineered an instant search engine with sanitized SQLite queries, responsive dashboard analytics, and clean access control.",
                "github_url": "",
                "live_demo_url": "",
                "featured": False,
                "display_order": 3,
                "technologies": ["HTML", "CSS", "JavaScript", "Python Flask", "SQLite"],
                "features": ["Voter verification", "Real-time voter search", "Responsive dashboard", "SQLite-based record management", "Flask backend", "Authentication/verification workflow"],
                "statistics": [("Verification Speed", "< 50ms"), ("Record Security", "Sanitized"), ("UI Responsiveness", "100%")]
            },
            {
                "title": "Real-Time Interview Assistant",
                "slug": "Real-time-interview-assistant",
                "aliases": [
                    "Interview AI", "AI Interview Assistant",
                    "Interview Support AI", "Real-time AI Interview Assistant", "Natively",
                    "Natively v2.8.5", "Desktop AI meeting copilot"
                ],
                "category": "AI + Desktop / Real-time",
                "short_description": "A desktop AI interview and meeting assistant offering real-time question detection, speech-to-text integration with Whisper and LLM response generation.",
                "detailed_description": "Engineered a desktop AI copilot built with Electron, Python, FastAPI, and Uvicorn. Integrates real-time audio capturing via Web Audio API and MediaRecorder, local/remote speech-to-text with Whisper, and low-latency LLM inference via Groq for instant question detection and desktop overlay assistance.",
                "problem_statement": "Candidates and professionals struggle with real-time question recall, technical interviewing stress, and rapid contextual reference during live video discussions.",
                "solution_statement": "Built a discrete desktop overlay combining low-latency Whisper speech-to-text with Groq LLM inference to automatically detect questions and present structured suggestions in real time.",
                "github_url": "",
                "live_demo_url": "",
                "featured": True,
                "display_order": 4,
                "technologies": ["Python", "FastAPI", "Uvicorn", "Electron", "JavaScript", "HTML", "CSS", "Web Audio API", "MediaRecorder", "Whisper", "Groq", "LLM", "Speech-to-Text"],
                "features": ["Real-time AI interview support", "Speech-to-Text integration via Whisper", "Real-time question detection & context extraction", "Discrete desktop screen overlay panel", "High-speed LLM inference powered by Groq"],
                "statistics": [("Audio Engine", "Real-time"), ("Speech-to-Text", "Whisper"), ("Inference Latency", "Low-latency")]
            }
        ]

        projects_created_count = 0
        projects_updated_count = 0
        duplicates_merged_count = 0

        # Deactivate all projects first, so only seeded/canonical ones become active
        Project.objects.all().update(is_active=False)

        for spec in projects_specs:
            target_slug = spec["slug"]
            target_title = spec["title"]
            target_norm = normalize_string(target_title)

            # Build list of normalized aliases for matching
            all_alias_norms = [normalize_string(target_title), normalize_string(target_slug)] + [normalize_string(a) for a in spec["aliases"]]

            # Search DB for any existing project matching slug, title, normalized title, or alias
            existing_candidates = []
            for p in Project.objects.all():
                p_norm = normalize_string(p.title)
                p_slug_norm = normalize_string(p.slug)
                if (p.slug == target_slug or p_norm == target_norm or
                    p_norm in all_alias_norms or p_slug_norm in all_alias_norms):
                    if p not in existing_candidates:
                        existing_candidates.append(p)

                # Check aliases database table
                if p not in existing_candidates:
                    for alias_obj in p.aliases.all():
                        if normalize_string(alias_obj.alias) in all_alias_norms or alias_obj.normalized_alias in all_alias_norms:
                            existing_candidates.append(p)
                            break

            if not existing_candidates:
                # Create brand new project
                primary_project = Project.objects.create(
                    title=target_title,
                    slug=target_slug,
                    category=spec["category"],
                    short_description=spec["short_description"],
                    detailed_description=spec["detailed_description"],
                    problem_statement=spec["problem_statement"],
                    solution_statement=spec["solution_statement"],
                    github_url=spec["github_url"],
                    live_demo_url=spec["live_demo_url"],
                    featured=spec["featured"],
                    display_order=spec["display_order"],
                    is_active=True
                )
                projects_created_count += 1
            else:
                # Pick the canonical record (or the first matching one)
                primary_project = existing_candidates[0]
                primary_project.title = target_title
                primary_project.slug = target_slug
                primary_project.category = spec["category"]
                primary_project.short_description = spec["short_description"]
                primary_project.detailed_description = spec["detailed_description"]
                primary_project.problem_statement = spec["problem_statement"]
                primary_project.solution_statement = spec["solution_statement"]
                if spec["github_url"]:
                    primary_project.github_url = spec["github_url"]
                if spec["live_demo_url"]:
                    primary_project.live_demo_url = spec["live_demo_url"]
                primary_project.featured = spec["featured"]
                primary_project.display_order = spec["display_order"]
                primary_project.is_active = True

                # Merge any duplicate candidate records into primary_project
                if len(existing_candidates) > 1:
                    duplicates = existing_candidates[1:]
                    for dup in duplicates:
                        # Reassign/merge URLs/images if primary lacks them
                        if not primary_project.github_url and dup.github_url:
                            primary_project.github_url = dup.github_url
                        if not primary_project.live_demo_url and dup.live_demo_url:
                            primary_project.live_demo_url = dup.live_demo_url
                        if not primary_project.project_image and dup.project_image:
                            primary_project.project_image = dup.project_image

                        # Delete duplicate record
                        dup.delete()
                        duplicates_merged_count += 1

                primary_project.save()
                projects_updated_count += 1

            # Ensure all aliases are attached to primary_project
            for alias_text in spec["aliases"]:
                ProjectAlias.objects.get_or_create(
                    project=primary_project,
                    alias=alias_text,
                    defaults={"normalized_alias": normalize_string(alias_text)}
                )

            # Refresh Technologies
            ProjectTechnology.objects.filter(project=primary_project).delete()
            for idx, t_name in enumerate(spec["technologies"], 1):
                ProjectTechnology.objects.create(project=primary_project, name=t_name, display_order=idx)

            # Refresh Features
            ProjectFeature.objects.filter(project=primary_project).delete()
            for idx, f_text in enumerate(spec["features"], 1):
                ProjectFeature.objects.create(project=primary_project, feature=f_text, display_order=idx)

            # Refresh Statistics
            ProjectStatistic.objects.filter(project=primary_project).delete()
            for idx, (lbl, val) in enumerate(spec["statistics"], 1):
                ProjectStatistic.objects.create(project=primary_project, label=lbl, value=val, display_order=idx)

        # 5. Experience
        Experience.objects.all().update(is_active=False)
        Experience.objects.update_or_create(
            job_title="Data Science Intern",
            company="Paarsh Infotech Pvt. Ltd.",
            defaults={
                "location": "Nashik, Maharashtra",
                "start_date": "January 2025",
                "end_date": "March 2025",
                "description": "Worked on practical assignments and projects involving Python, OOP, SQL, Machine Learning, data analysis, visualization and model development.",
                "technologies": "Python, SQL, NumPy, Pandas, Matplotlib, Scikit-Learn, Power BI, Jupyter Notebook, Google Colab, GitHub, Postman, VS Code",
                "display_order": 1,
                "is_active": True
            }
        )
        Experience.objects.update_or_create(
            job_title="Python Developer",
            company="BluJay Technologies",
            defaults={
                "location": "Hyderabad, Telangana, India",
                "start_date": "July 2026",
                "end_date": "Present",
                "description": "Working as a Python Developer Intern on AI-powered chatbot development. Gaining hands-on experience in Python, Generative AI, Prompt Engineering, API integration and backend development. Building and improving real-world conversational AI features and working with modern AI application development workflows.",
                "technologies": "Python, Generative AI, Prompt Engineering, API Integration, Backend Development, AI Chatbots, REST APIs, LangChain, RAG, GitHub, VS Code",
                "display_order": 2,
                "is_active": True
            }
        )

        # 6. Education
        Education.objects.all().update(is_active=False)
        Education.objects.update_or_create(
            degree="Bachelor of Engineering in Computer Engineering",
            institution="Savitribai Phule Pune University",
            defaults={
                "location": "Maharashtra, India",
                "start_year": "2022",
                "end_year": "2026",
                "grade": "CGPA: 8.65 / 10",
                "display_order": 1,
                "is_active": True
            }
        )
        Education.objects.update_or_create(
            degree="HSC – Science Stream",
            institution="Maharashtra State Board",
            defaults={
                "location": "Maharashtra, India",
                "start_year": "2022",
                "end_year": "2022",
                "grade": "70.67%",
                "display_order": 2,
                "is_active": True
            }
        )
        Education.objects.update_or_create(
            degree="SSC",
            institution="Maharashtra State Board",
            defaults={
                "location": "Maharashtra, India",
                "start_year": "2020",
                "end_year": "2020",
                "grade": "91.80%",
                "display_order": 3,
                "is_active": True
            }
        )

        # 7. Certifications
        Certification.objects.all().update(is_active=False)
        certs_data = [
            ("Machine Learning Fundamentals", "AWS Skill Builder", 1),
            ("Power BI – Data Visualization", "Mind Luster", 2),
            ("Python Programming", "Self-paced / Online", 3),
            ("ReactJS Development", "Self-paced / Online", 4),
            ("Deep Learning Basics", "Self-paced / Online", 5),
            ("NLP Fundamentals", "Self-paced / Online", 6),
        ]
        for c_name, issuer, order in certs_data:
            Certification.objects.update_or_create(
                name=c_name,
                defaults={
                    "issuer": issuer,
                    "certificate_url": "",
                    "display_order": order,
                    "is_active": True
                }
            )

        # 8. Achievements
        Achievement.objects.all().update(is_active=False)
        achievements_data = [
            ("93% Crop Yield Prediction Accuracy", "93%", "Achieved 93% crop yield prediction accuracy in the FarmEra AgriTech project.", "trending-up", 1),
            ("91% Disease Detection Accuracy", "91%", "Achieved 91% disease detection accuracy across 13 disease classes in FarmEra.", "shield-check", 2),
            ("13 Disease Classes", "13", "Disease detection system supporting 13 disease classes.", "grid", 3),
            ("15%+ Baseline Improvement", "15%+", "FarmEra models demonstrated more than 15% improvement over baseline ML benchmarks.", "award", 4),
            ("GTT Foundation Program", "Completed", "Completed GTT Foundation Communication & Personality Development Program.", "check-circle", 5),
            ("Continuous Learning", "AI • ML • GenAI", "Continuously upskilling in AI, ML, Generative AI, Data Science and Cloud technologies.", "cpu", 6),
        ]
        for title, val, desc, icon, order in achievements_data:
            Achievement.objects.update_or_create(
                title=title,
                defaults={
                    "value": val,
                    "description": desc,
                    "icon": icon,
                    "display_order": order,
                    "is_featured": True,
                    "is_active": True
                }
            )

        # 9. SiteSettings
        SiteSettings.objects.update_or_create(
            id=1,
            defaults={
                "site_name": "Pratik Pawar",
                "meta_title": "Pratik Pawar | AI/ML Engineer | GenAI Engineer | Python Developer",
                "meta_description": "Portfolio of Pratik Kautik Pawar, an AI/ML Engineer, GenAI Engineer and Python Developer building Machine Learning, Generative AI and full-stack applications.",
                "footer_text": "AI/ML Engineer • GenAI Engineer • Python Developer",
                "copyright_text": "© 2026 Pratik Kautik Pawar. All Rights Reserved.",
                "enable_animations": True,
                "enable_particles": True,
                "enable_cursor_effect": True,
            }
        )

        total_active_projects = Project.objects.filter(is_active=True).count()

        # Print summary
        self.stdout.write(self.style.SUCCESS("Portfolio data seeded successfully!\n"))
        self.stdout.write(f"Projects found: {total_active_projects + duplicates_merged_count}")
        self.stdout.write(f"Projects created: {projects_created_count}")
        self.stdout.write(f"Projects updated: {projects_updated_count}")
        self.stdout.write(f"Duplicates merged: {duplicates_merged_count}\n")

        self.stdout.write(f"Personal Information: {PersonalInfo.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Social Links: {SocialLink.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Skills: {Skill.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Projects: {total_active_projects}")
        self.stdout.write(f"Experience: {Experience.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Education: {Education.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Certifications: {Certification.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Achievements: {Achievement.objects.filter(is_active=True).count()}")
