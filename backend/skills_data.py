"""
Master skill list for resume parsing and matching.
Organized by categories for better matching and analysis.
"""

SKILLS_DATABASE = {
    "programming_languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust",
        "TypeScript", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
        "Perl", "Shell", "Bash", "PowerShell", "SQL", "HTML", "CSS"
    ],
    
    "frameworks_libraries": [
        "React", "Angular", "Vue.js", "Next.js", "Node.js", "Express.js",
        "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", ".NET Core",
        "Laravel", "Ruby on Rails", "TensorFlow", "PyTorch", "Keras",
        "scikit-learn", "Pandas", "NumPy", "jQuery", "Bootstrap", "Tailwind CSS",
        "Material-UI", "Redux", "GraphQL", "REST API"
    ],
    
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
        "Microsoft SQL Server", "MariaDB", "Cassandra", "DynamoDB",
        "Elasticsearch", "Neo4j", "Firebase", "Supabase"
    ],
    
    "cloud_devops": [
        "AWS", "Azure", "Google Cloud Platform", "GCP", "Docker", "Kubernetes",
        "Jenkins", "GitLab CI/CD", "GitHub Actions", "Terraform", "Ansible",
        "CI/CD", "DevOps", "Microservices", "Serverless", "Lambda"
    ],
    
    "tools_platforms": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",
        "VS Code", "IntelliJ IDEA", "Eclipse", "Postman", "Swagger",
        "Nginx", "Apache", "Linux", "Unix", "Windows Server"
    ],
    
    "data_ai_ml": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP",
        "Computer Vision", "Data Analysis", "Data Science", "Big Data",
        "Apache Spark", "Hadoop", "Data Mining", "Statistical Analysis",
        "Neural Networks", "CNN", "RNN", "Transformer", "BERT", "GPT",
        "LLM", "Large Language Models", "AI", "Artificial Intelligence"
    ],
    
    "soft_skills": [
        "Leadership", "Communication", "Team Management", "Problem Solving",
        "Critical Thinking", "Time Management", "Agile", "Scrum",
        "Project Management", "Analytical Skills", "Collaboration",
        "Adaptability", "Creativity", "Attention to Detail"
    ],
    
    "methodologies": [
        "Agile", "Scrum", "Kanban", "Waterfall", "Test Driven Development", "TDD",
        "Behavior Driven Development", "BDD", "Domain Driven Design", "DDD",
        "Microservices Architecture", "RESTful API Design", "Object Oriented Programming", "OOP",
        "Functional Programming", "DevOps", "MLOps"
    ]
}

def get_all_skills():
    """Returns a flat list of all skills."""
    all_skills = []
    for category_skills in SKILLS_DATABASE.values():
        all_skills.extend(category_skills)
    return list(set(all_skills))  # Remove duplicates

def get_skills_by_category(category):
    """Returns skills for a specific category."""
    return SKILLS_DATABASE.get(category, [])

def categorize_skill(skill):
    """Returns the category of a given skill."""
    skill_lower = skill.lower()
    for category, skills in SKILLS_DATABASE.items():
        if any(s.lower() == skill_lower for s in skills):
            return category
    return "other"
