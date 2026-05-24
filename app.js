/**
 * Morphos Demo - Resume Analysis & Job Matching
 * Simulates the full 5-Dimensional Atomic DNA scoring pipeline
 */

// ===== State =====
const state = {
    step: 1,
    questionnaire: {
        q1: '', q2: '', q3: '', q4: '', q5: ''
    },
    cv: {
        work: '',
        skills: '',
        growth: ''
    },
    scores: {
        q: [0, 0, 0, 0, 0],
        cv: [0, 0, 0, 0, 0],
        fused: [0, 0, 0, 0, 0]
    },
    dnaScore: 0,
    recommendations: []
};

// Dimension labels
const DIM_LABELS = ['D1 核心能力', 'D2 思维模式', 'D3 领域知识', 'D4 方法论', 'D5 工具平台'];
const DIM_NAMES = ['Core Competency', 'Mindset/Behavior', 'Domain Knowledge', 'Methodology', 'Tools & Platforms'];
const DIM_WEIGHTS = [0.40, 0.24, 0.13, 0.13, 0.10];

// Mock ACKG role database
const ACKG_ROLES = [
    // ===== Software Engineering =====
    {
        id: 'frontend_dev',
        title: 'Frontend Developer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'HTML/CSS', difficulty: 3 },
            { name: 'JavaScript', difficulty: 4 },
            { name: 'React/Vue/Angular', difficulty: 5 },
            { name: 'Git', difficulty: 3 },
            { name: 'Responsive Design', difficulty: 4 },
            { name: 'REST APIs', difficulty: 4 }
        ],
        userSkills: ['HTML/CSS', 'JavaScript', 'Git'],
        matchWeights: [0.25, 0.20, 0.10, 0.15, 0.30]
    },
    {
        id: 'backend_engineer',
        title: 'Senior Backend Engineer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'Java/Python/Go', difficulty: 5 },
            { name: 'Microservices', difficulty: 7 },
            { name: 'Database Design', difficulty: 6 },
            { name: 'System Design', difficulty: 8 },
            { name: 'Cloud Platforms', difficulty: 5 },
            { name: 'Performance Optimization', difficulty: 7 }
        ],
        userSkills: ['Java/Python/Go', 'Database Design', 'Cloud Platforms'],
        matchWeights: [0.35, 0.15, 0.10, 0.15, 0.25]
    },
    {
        id: 'fullstack_engineer',
        title: 'Fullstack Engineer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'Frontend Framework', difficulty: 5 },
            { name: 'Backend Language', difficulty: 5 },
            { name: 'Database', difficulty: 5 },
            { name: 'API Design', difficulty: 5 },
            { name: 'DevOps Basics', difficulty: 4 },
            { name: 'System Architecture', difficulty: 6 }
        ],
        userSkills: ['Frontend Framework', 'Backend Language', 'Database'],
        matchWeights: [0.30, 0.15, 0.10, 0.15, 0.30]
    },
    {
        id: 'mobile_dev',
        title: 'Mobile App Developer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'Swift/Kotlin', difficulty: 5 },
            { name: 'iOS/Android SDK', difficulty: 5 },
            { name: 'Mobile UI Design', difficulty: 4 },
            { name: 'API Integration', difficulty: 4 },
            { name: 'Firebase', difficulty: 4 },
            { name: 'CI/CD for Mobile', difficulty: 5 }
        ],
        userSkills: ['Swift/Kotlin', 'API Integration'],
        matchWeights: [0.25, 0.15, 0.10, 0.15, 0.35]
    },
    {
        id: 'devops_engineer',
        title: 'DevOps Engineer',
        category: 'Infrastructure & DevOps',
        requiredSkills: [
            { name: 'Linux', difficulty: 4 },
            { name: 'Docker/K8s', difficulty: 6 },
            { name: 'CI/CD Tools', difficulty: 5 },
            { name: 'Cloud Platforms', difficulty: 5 },
            { name: 'Infrastructure as Code', difficulty: 6 },
            { name: 'Monitoring/Logging', difficulty: 5 }
        ],
        userSkills: ['Linux', 'Docker/K8s', 'Cloud Platforms'],
        matchWeights: [0.25, 0.15, 0.10, 0.25, 0.25]
    },
    {
        id: 'cloud_architect',
        title: 'Cloud Architect',
        category: 'Infrastructure & DevOps',
        requiredSkills: [
            { name: 'AWS/Azure/GCP', difficulty: 6 },
            { name: 'System Design', difficulty: 8 },
            { name: 'Networking', difficulty: 6 },
            { name: 'Security', difficulty: 6 },
            { name: 'Cost Optimization', difficulty: 5 },
            { name: 'Terraform', difficulty: 5 }
        ],
        userSkills: ['AWS/Azure/GCP', 'System Design'],
        matchWeights: [0.35, 0.15, 0.15, 0.15, 0.20]
    },
    {
        id: 'security_engineer',
        title: 'Security Engineer',
        category: 'Infrastructure & DevOps',
        requiredSkills: [
            { name: 'Network Security', difficulty: 6 },
            { name: 'Cryptography', difficulty: 7 },
            { name: 'Penetration Testing', difficulty: 6 },
            { name: 'Security Frameworks', difficulty: 6 },
            { name: 'Incident Response', difficulty: 6 },
            { name: 'Compliance', difficulty: 5 }
        ],
        userSkills: ['Network Security', 'Security Frameworks'],
        matchWeights: [0.30, 0.10, 0.20, 0.20, 0.20]
    },
    {
        id: 'qa_engineer',
        title: 'QA Automation Engineer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'Test Automation', difficulty: 5 },
            { name: 'Selenium/Cypress', difficulty: 5 },
            { name: 'CI/CD Integration', difficulty: 5 },
            { name: 'API Testing', difficulty: 4 },
            { name: 'Performance Testing', difficulty: 5 },
            { name: 'BDD/TDD', difficulty: 4 }
        ],
        userSkills: ['Test Automation', 'API Testing'],
        matchWeights: [0.25, 0.15, 0.10, 0.25, 0.25]
    },
    {
        id: 'game_dev',
        title: 'Game Developer',
        category: 'Software Engineering',
        requiredSkills: [
            { name: 'C++/C#', difficulty: 5 },
            { name: 'Unity/Unreal', difficulty: 6 },
            { name: '3D Math', difficulty: 6 },
            { name: 'Physics Engine', difficulty: 5 },
            { name: 'Shader Programming', difficulty: 6 },
            { name: 'Game AI', difficulty: 6 }
        ],
        userSkills: ['C++/C#', 'Unity/Unreal'],
        matchWeights: [0.30, 0.15, 0.10, 0.15, 0.30]
    },
    // ===== Data & AI =====
    {
        id: 'ml_engineer',
        title: 'Machine Learning Engineer',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'Python', difficulty: 4 },
            { name: 'TensorFlow/PyTorch', difficulty: 6 },
            { name: 'MLOps', difficulty: 7 },
            { name: 'Distributed Systems', difficulty: 8 },
            { name: 'Docker/K8s', difficulty: 5 },
            { name: 'System Design', difficulty: 8 }
        ],
        userSkills: ['Python', 'Docker/K8s'],
        matchWeights: [0.35, 0.15, 0.15, 0.15, 0.20]
    },
    {
        id: 'data_scientist',
        title: 'Senior Data Scientist',
        category: 'Data & Analytics',
        requiredSkills: [
            { name: 'Statistical Modeling', difficulty: 7 },
            { name: 'SQL', difficulty: 4 },
            { name: 'A/B Testing', difficulty: 5 },
            { name: 'Data Visualization', difficulty: 4 },
            { name: 'Business Acumen', difficulty: 6 },
            { name: 'Python/R', difficulty: 4 }
        ],
        userSkills: ['SQL', 'Data Visualization', 'Python/R', 'A/B Testing'],
        matchWeights: [0.30, 0.30, 0.15, 0.10, 0.15]
    },
    {
        id: 'data_engineer',
        title: 'Data Engineer',
        category: 'Data & Analytics',
        requiredSkills: [
            { name: 'SQL/NoSQL', difficulty: 4 },
            { name: 'ETL Pipelines', difficulty: 5 },
            { name: 'Spark/Flink', difficulty: 6 },
            { name: 'Cloud Platforms', difficulty: 5 },
            { name: 'Data Modeling', difficulty: 6 },
            { name: 'Streaming', difficulty: 7 }
        ],
        userSkills: ['SQL/NoSQL', 'Cloud Platforms', 'ETL Pipelines'],
        matchWeights: [0.25, 0.15, 0.15, 0.20, 0.25]
    },
    {
        id: 'research_scientist',
        title: 'AI Research Scientist',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'Deep Learning Theory', difficulty: 9 },
            { name: 'Mathematics', difficulty: 8 },
            { name: 'Paper Writing', difficulty: 6 },
            { name: 'Experiment Design', difficulty: 7 },
            { name: 'PyTorch/JAX', difficulty: 6 },
            { name: 'Novel Architecture', difficulty: 10 }
        ],
        userSkills: ['PyTorch/JAX'],
        matchWeights: [0.45, 0.20, 0.15, 0.10, 0.05]
    },
    {
        id: 'mlops_engineer',
        title: 'MLOps Engineer',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'Docker/K8s', difficulty: 6 },
            { name: 'CI/CD', difficulty: 5 },
            { name: 'Model Monitoring', difficulty: 6 },
            { name: 'Feature Stores', difficulty: 6 },
            { name: 'ML Pipelines', difficulty: 6 },
            { name: 'Cloud Platforms', difficulty: 5 }
        ],
        userSkills: ['Docker/K8s', 'CI/CD', 'Cloud Platforms'],
        matchWeights: [0.25, 0.15, 0.10, 0.25, 0.25]
    },
    {
        id: 'bi_analyst',
        title: 'Business Intelligence Analyst',
        category: 'Data & Analytics',
        requiredSkills: [
            { name: 'SQL', difficulty: 4 },
            { name: 'BI Tools', difficulty: 4 },
            { name: 'Data Warehousing', difficulty: 5 },
            { name: 'Business Analysis', difficulty: 5 },
            { name: 'Reporting', difficulty: 4 },
            { name: 'KPI Design', difficulty: 5 }
        ],
        userSkills: ['SQL', 'BI Tools', 'Reporting'],
        matchWeights: [0.30, 0.20, 0.20, 0.10, 0.20]
    },
    {
        id: 'data_analyst',
        title: 'Data Analyst',
        category: 'Data & Analytics',
        requiredSkills: [
            { name: 'SQL', difficulty: 3 },
            { name: 'Excel', difficulty: 3 },
            { name: 'Data Visualization', difficulty: 4 },
            { name: 'Statistics', difficulty: 4 },
            { name: 'Business Understanding', difficulty: 5 },
            { name: 'Python', difficulty: 4 }
        ],
        userSkills: ['SQL', 'Excel', 'Data Visualization'],
        matchWeights: [0.25, 0.20, 0.20, 0.15, 0.20]
    },
    {
        id: 'cv_engineer',
        title: 'Computer Vision Engineer',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'Python', difficulty: 4 },
            { name: 'OpenCV', difficulty: 5 },
            { name: 'Deep Learning', difficulty: 7 },
            { name: 'Image Processing', difficulty: 6 },
            { name: 'TensorFlow/PyTorch', difficulty: 6 },
            { name: 'C++', difficulty: 5 }
        ],
        userSkills: ['Python', 'OpenCV'],
        matchWeights: [0.35, 0.15, 0.15, 0.10, 0.25]
    },
    {
        id: 'nlp_engineer',
        title: 'NLP Engineer',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'Python', difficulty: 4 },
            { name: 'NLP Libraries', difficulty: 6 },
            { name: 'Deep Learning', difficulty: 7 },
            { name: 'Linguistics', difficulty: 5 },
            { name: 'Text Mining', difficulty: 5 },
            { name: 'Transformer Models', difficulty: 7 }
        ],
        userSkills: ['Python', 'NLP Libraries'],
        matchWeights: [0.35, 0.15, 0.15, 0.10, 0.25]
    },
    {
        id: 'prompt_engineer',
        title: 'Prompt Engineer',
        category: 'AI & Machine Learning',
        requiredSkills: [
            { name: 'LLM Understanding', difficulty: 6 },
            { name: 'Prompt Design', difficulty: 5 },
            { name: 'Chain-of-Thought', difficulty: 5 },
            { name: 'Python', difficulty: 4 },
            { name: 'API Integration', difficulty: 4 },
            { name: 'Evaluation Metrics', difficulty: 5 }
        ],
        userSkills: ['Python', 'API Integration'],
        matchWeights: [0.30, 0.25, 0.15, 0.10, 0.20]
    },
    // ===== Product & Design =====
    {
        id: 'product_manager',
        title: 'Product Manager',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'Product Strategy', difficulty: 7 },
            { name: 'User Research', difficulty: 5 },
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Stakeholder Mgmt', difficulty: 5 },
            { name: 'Roadmapping', difficulty: 5 },
            { name: 'A/B Testing', difficulty: 4 }
        ],
        userSkills: ['User Research', 'Data Analysis', 'Roadmapping'],
        matchWeights: [0.20, 0.35, 0.20, 0.15, 0.10]
    },
    {
        id: 'technical_pm',
        title: 'Technical Product Manager',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'Product Strategy', difficulty: 6 },
            { name: 'Technical Architecture', difficulty: 6 },
            { name: 'API Design', difficulty: 5 },
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Stakeholder Mgmt', difficulty: 5 },
            { name: 'Agile/Scrum', difficulty: 4 }
        ],
        userSkills: ['Data Analysis', 'API Design', 'Agile/Scrum'],
        matchWeights: [0.25, 0.30, 0.20, 0.15, 0.10]
    },
    {
        id: 'growth_pm',
        title: 'Growth Product Manager',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'Growth Strategy', difficulty: 6 },
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Experimentation', difficulty: 5 },
            { name: 'User Psychology', difficulty: 5 },
            { name: 'Marketing Basics', difficulty: 4 },
            { name: 'A/B Testing', difficulty: 4 }
        ],
        userSkills: ['Data Analysis', 'A/B Testing'],
        matchWeights: [0.25, 0.35, 0.15, 0.15, 0.10]
    },
    {
        id: 'ai_product_manager',
        title: 'AI Product Manager',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'Product Strategy', difficulty: 6 },
            { name: 'AI/ML Literacy', difficulty: 6 },
            { name: 'Stakeholder Mgmt', difficulty: 5 },
            { name: 'Roadmapping', difficulty: 5 },
            { name: 'User Research', difficulty: 4 },
            { name: 'Ethics & Governance', difficulty: 8 }
        ],
        userSkills: ['Stakeholder Mgmt', 'Roadmapping'],
        matchWeights: [0.25, 0.35, 0.20, 0.10, 0.10]
    },
    {
        id: 'ux_designer',
        title: 'UX Designer',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'User Research', difficulty: 5 },
            { name: 'Wireframing', difficulty: 4 },
            { name: 'Prototyping', difficulty: 4 },
            { name: 'Usability Testing', difficulty: 5 },
            { name: 'Design Systems', difficulty: 5 },
            { name: 'Figma/Sketch', difficulty: 4 }
        ],
        userSkills: ['Figma/Sketch', 'Wireframing'],
        matchWeights: [0.20, 0.30, 0.15, 0.20, 0.15]
    },
    {
        id: 'ui_designer',
        title: 'UI Designer',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'Visual Design', difficulty: 5 },
            { name: 'Typography', difficulty: 4 },
            { name: 'Color Theory', difficulty: 4 },
            { name: 'Design Tools', difficulty: 4 },
            { name: 'Frontend Basics', difficulty: 4 },
            { name: 'Animation', difficulty: 4 }
        ],
        userSkills: ['Visual Design', 'Design Tools'],
        matchWeights: [0.15, 0.25, 0.15, 0.20, 0.25]
    },
    {
        id: 'product_designer',
        title: 'Product Designer',
        category: 'Product & Design',
        requiredSkills: [
            { name: 'User Research', difficulty: 5 },
            { name: 'Interaction Design', difficulty: 5 },
            { name: 'Visual Design', difficulty: 5 },
            { name: 'Prototyping', difficulty: 4 },
            { name: 'Design Systems', difficulty: 5 },
            { name: 'Frontend Basics', difficulty: 4 }
        ],
        userSkills: ['Visual Design', 'Prototyping'],
        matchWeights: [0.20, 0.30, 0.15, 0.20, 0.15]
    },
    // ===== Marketing & Operations =====
    {
        id: 'digital_marketing',
        title: 'Digital Marketing Manager',
        category: 'Marketing & Growth',
        requiredSkills: [
            { name: 'SEO/SEM', difficulty: 5 },
            { name: 'Google Analytics', difficulty: 4 },
            { name: 'Content Strategy', difficulty: 5 },
            { name: 'Social Media', difficulty: 4 },
            { name: 'Email Marketing', difficulty: 4 },
            { name: 'PPC Advertising', difficulty: 4 }
        ],
        userSkills: ['Social Media', 'Content Strategy'],
        matchWeights: [0.15, 0.30, 0.25, 0.15, 0.15]
    },
    {
        id: 'content_marketing',
        title: 'Content Marketing Manager',
        category: 'Marketing & Growth',
        requiredSkills: [
            { name: 'Content Strategy', difficulty: 6 },
            { name: 'SEO', difficulty: 5 },
            { name: 'Copywriting', difficulty: 4 },
            { name: 'Analytics', difficulty: 4 },
            { name: 'Brand Voice', difficulty: 5 },
            { name: 'Distribution', difficulty: 4 }
        ],
        userSkills: ['Copywriting', 'SEO'],
        matchWeights: [0.15, 0.30, 0.25, 0.15, 0.15]
    },
    {
        id: 'growth_hacker',
        title: 'Growth Hacker',
        category: 'Marketing & Growth',
        requiredSkills: [
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Experimentation', difficulty: 5 },
            { name: 'Marketing Automation', difficulty: 5 },
            { name: 'Product Analytics', difficulty: 5 },
            { name: 'A/B Testing', difficulty: 5 },
            { name: 'Viral Mechanics', difficulty: 5 }
        ],
        userSkills: ['Data Analysis', 'A/B Testing'],
        matchWeights: [0.25, 0.30, 0.15, 0.15, 0.15]
    },
    {
        id: 'social_media',
        title: 'Social Media Manager',
        category: 'Marketing & Growth',
        requiredSkills: [
            { name: 'Social Platforms', difficulty: 4 },
            { name: 'Content Creation', difficulty: 4 },
            { name: 'Community Mgmt', difficulty: 4 },
            { name: 'Analytics', difficulty: 4 },
            { name: 'Influencer Mgmt', difficulty: 4 },
            { name: 'Crisis Mgmt', difficulty: 5 }
        ],
        userSkills: ['Social Platforms', 'Content Creation'],
        matchWeights: [0.10, 0.30, 0.25, 0.20, 0.15]
    },
    {
        id: 'seo_specialist',
        title: 'SEO Specialist',
        category: 'Marketing & Growth',
        requiredSkills: [
            { name: 'Technical SEO', difficulty: 6 },
            { name: 'Content Optimization', difficulty: 5 },
            { name: 'Link Building', difficulty: 5 },
            { name: 'Analytics', difficulty: 4 },
            { name: 'Keyword Research', difficulty: 4 },
            { name: 'HTML/CSS', difficulty: 3 }
        ],
        userSkills: ['HTML/CSS', 'Analytics', 'Keyword Research'],
        matchWeights: [0.20, 0.15, 0.25, 0.20, 0.20]
    },
    {
        id: 'ops_manager',
        title: 'Operations Manager',
        category: 'Operations',
        requiredSkills: [
            { name: 'Process Optimization', difficulty: 5 },
            { name: 'Supply Chain', difficulty: 5 },
            { name: 'Data Analysis', difficulty: 4 },
            { name: 'Team Mgmt', difficulty: 5 },
            { name: 'Budgeting', difficulty: 4 },
            { name: 'Vendor Mgmt', difficulty: 4 }
        ],
        userSkills: ['Data Analysis', 'Team Mgmt'],
        matchWeights: [0.15, 0.25, 0.20, 0.25, 0.15]
    },
    {
        id: 'community_manager',
        title: 'Community Manager',
        category: 'Operations',
        requiredSkills: [
            { name: 'Community Building', difficulty: 5 },
            { name: 'Content Mgmt', difficulty: 4 },
            { name: 'Event Planning', difficulty: 4 },
            { name: 'Analytics', difficulty: 4 },
            { name: 'CRM Tools', difficulty: 4 },
            { name: 'Moderation', difficulty: 3 }
        ],
        userSkills: ['Content Mgmt', 'Event Planning'],
        matchWeights: [0.10, 0.35, 0.20, 0.20, 0.15]
    },
    // ===== Sales & Business =====
    {
        id: 'sales_manager',
        title: 'Sales Manager',
        category: 'Sales & Business',
        requiredSkills: [
            { name: 'Sales Strategy', difficulty: 6 },
            { name: 'Team Leadership', difficulty: 6 },
            { name: 'CRM', difficulty: 4 },
            { name: 'Negotiation', difficulty: 5 },
            { name: 'Forecasting', difficulty: 5 },
            { name: 'Pipeline Mgmt', difficulty: 5 }
        ],
        userSkills: ['CRM', 'Negotiation'],
        matchWeights: [0.15, 0.40, 0.20, 0.15, 0.10]
    },
    {
        id: 'account_exec',
        title: 'Account Executive',
        category: 'Sales & Business',
        requiredSkills: [
            { name: 'Prospecting', difficulty: 5 },
            { name: 'Relationship Building', difficulty: 5 },
            { name: 'Closing', difficulty: 5 },
            { name: 'CRM', difficulty: 4 },
            { name: 'Industry Knowledge', difficulty: 5 },
            { name: 'Presentation', difficulty: 4 }
        ],
        userSkills: ['CRM', 'Presentation'],
        matchWeights: [0.15, 0.40, 0.20, 0.15, 0.10]
    },
    {
        id: 'bd_manager',
        title: 'Business Development Manager',
        category: 'Sales & Business',
        requiredSkills: [
            { name: 'Market Analysis', difficulty: 5 },
            { name: 'Partnership Building', difficulty: 6 },
            { name: 'Negotiation', difficulty: 5 },
            { name: 'Strategy', difficulty: 5 },
            { name: 'Networking', difficulty: 5 },
            { name: 'CRM', difficulty: 4 }
        ],
        userSkills: ['CRM', 'Networking'],
        matchWeights: [0.20, 0.35, 0.20, 0.15, 0.10]
    },
    {
        id: 'customer_success',
        title: 'Customer Success Manager',
        category: 'Sales & Business',
        requiredSkills: [
            { name: 'Relationship Mgmt', difficulty: 5 },
            { name: 'Onboarding', difficulty: 4 },
            { name: 'Retention Strategy', difficulty: 5 },
            { name: 'Data Analysis', difficulty: 4 },
            { name: 'Product Knowledge', difficulty: 5 },
            { name: 'Communication', difficulty: 5 }
        ],
        userSkills: ['Communication', 'Data Analysis'],
        matchWeights: [0.15, 0.40, 0.15, 0.20, 0.10]
    },
    // ===== Finance =====
    {
        id: 'investment_analyst',
        title: 'Investment Analyst',
        category: 'Finance',
        requiredSkills: [
            { name: 'Financial Modeling', difficulty: 7 },
            { name: 'Valuation', difficulty: 7 },
            { name: 'Market Research', difficulty: 6 },
            { name: 'Excel', difficulty: 4 },
            { name: 'Bloomberg', difficulty: 5 },
            { name: 'Accounting', difficulty: 5 }
        ],
        userSkills: ['Excel', 'Market Research'],
        matchWeights: [0.35, 0.15, 0.30, 0.10, 0.10]
    },
    {
        id: 'financial_analyst',
        title: 'Financial Analyst',
        category: 'Finance',
        requiredSkills: [
            { name: 'Financial Modeling', difficulty: 6 },
            { name: 'Forecasting', difficulty: 6 },
            { name: 'Excel', difficulty: 4 },
            { name: 'ERP Systems', difficulty: 4 },
            { name: 'Reporting', difficulty: 4 },
            { name: 'Budgeting', difficulty: 5 }
        ],
        userSkills: ['Excel', 'Reporting'],
        matchWeights: [0.30, 0.15, 0.30, 0.15, 0.10]
    },
    {
        id: 'risk_manager',
        title: 'Risk Manager',
        category: 'Finance',
        requiredSkills: [
            { name: 'Risk Assessment', difficulty: 6 },
            { name: 'Regulatory Knowledge', difficulty: 6 },
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Financial Modeling', difficulty: 6 },
            { name: 'Compliance', difficulty: 5 },
            { name: 'Statistics', difficulty: 5 }
        ],
        userSkills: ['Data Analysis', 'Compliance'],
        matchWeights: [0.30, 0.20, 0.30, 0.15, 0.05]
    },
    {
        id: 'quant_analyst',
        title: 'Quantitative Analyst',
        category: 'Finance',
        requiredSkills: [
            { name: 'Mathematics', difficulty: 8 },
            { name: 'Python/R', difficulty: 5 },
            { name: 'Statistics', difficulty: 7 },
            { name: 'Financial Modeling', difficulty: 7 },
            { name: 'Machine Learning', difficulty: 6 },
            { name: 'C++', difficulty: 5 }
        ],
        userSkills: ['Python/R', 'Statistics'],
        matchWeights: [0.40, 0.15, 0.20, 0.10, 0.15]
    },
    {
        id: 'financial_advisor',
        title: 'Financial Advisor',
        category: 'Finance',
        requiredSkills: [
            { name: 'Client Relations', difficulty: 6 },
            { name: 'Financial Planning', difficulty: 6 },
            { name: 'Investment Strategy', difficulty: 6 },
            { name: 'Regulations', difficulty: 5 },
            { name: 'Sales', difficulty: 5 },
            { name: 'CRM', difficulty: 4 }
        ],
        userSkills: ['CRM', 'Client Relations'],
        matchWeights: [0.20, 0.35, 0.30, 0.10, 0.05]
    },
    // ===== Consulting & Leadership =====
    {
        id: 'mgmt_consultant',
        title: 'Management Consultant',
        category: 'Consulting',
        requiredSkills: [
            { name: 'Problem Solving', difficulty: 7 },
            { name: 'Strategy', difficulty: 6 },
            { name: 'Data Analysis', difficulty: 5 },
            { name: 'Presentation', difficulty: 5 },
            { name: 'Industry Knowledge', difficulty: 6 },
            { name: 'Change Mgmt', difficulty: 5 }
        ],
        userSkills: ['Data Analysis', 'Presentation'],
        matchWeights: [0.25, 0.30, 0.25, 0.15, 0.05]
    },
    {
        id: 'strategy_consultant',
        title: 'Strategy Consultant',
        category: 'Consulting',
        requiredSkills: [
            { name: 'Strategic Thinking', difficulty: 7 },
            { name: 'Market Analysis', difficulty: 6 },
            { name: 'Financial Modeling', difficulty: 6 },
            { name: 'Industry Knowledge', difficulty: 6 },
            { name: 'M&A', difficulty: 6 },
            { name: 'Stakeholder Mgmt', difficulty: 5 }
        ],
        userSkills: ['Market Analysis', 'Financial Modeling'],
        matchWeights: [0.30, 0.25, 0.30, 0.10, 0.05]
    },
    {
        id: 'eng_manager',
        title: 'Engineering Manager',
        category: 'Leadership',
        requiredSkills: [
            { name: 'Team Leadership', difficulty: 7 },
            { name: 'Technical Architecture', difficulty: 6 },
            { name: 'Hiring', difficulty: 5 },
            { name: 'Project Mgmt', difficulty: 5 },
            { name: 'Mentoring', difficulty: 5 },
            { name: 'Stakeholder Mgmt', difficulty: 5 }
        ],
        userSkills: ['Technical Architecture', 'Project Mgmt'],
        matchWeights: [0.20, 0.35, 0.10, 0.20, 0.15]
    },
    {
        id: 'eng_director',
        title: 'Engineering Director',
        category: 'Leadership',
        requiredSkills: [
            { name: 'Org Design', difficulty: 7 },
            { name: 'Strategic Planning', difficulty: 7 },
            { name: 'Cross-functional Leadership', difficulty: 7 },
            { name: 'Budgeting', difficulty: 5 },
            { name: 'Hiring', difficulty: 5 },
            { name: 'Technical Vision', difficulty: 6 }
        ],
        userSkills: ['Strategic Planning', 'Hiring'],
        matchWeights: [0.20, 0.40, 0.15, 0.15, 0.10]
    },
    {
        id: 'cto',
        title: 'Chief Technology Officer',
        category: 'Leadership',
        requiredSkills: [
            { name: 'Technology Strategy', difficulty: 8 },
            { name: 'Org Leadership', difficulty: 8 },
            { name: 'Business Acumen', difficulty: 7 },
            { name: 'Architecture', difficulty: 7 },
            { name: 'Innovation', difficulty: 7 },
            { name: 'Stakeholder Mgmt', difficulty: 6 }
        ],
        userSkills: ['Architecture', 'Innovation'],
        matchWeights: [0.25, 0.40, 0.15, 0.10, 0.10]
    },
    // ===== HR & People =====
    {
        id: 'hr_manager',
        title: 'HR Manager',
        category: 'Human Resources',
        requiredSkills: [
            { name: 'Employee Relations', difficulty: 6 },
            { name: 'Performance Mgmt', difficulty: 5 },
            { name: 'Labor Law', difficulty: 5 },
            { name: 'Recruitment', difficulty: 5 },
            { name: 'Training', difficulty: 5 },
            { name: 'HRIS', difficulty: 4 }
        ],
        userSkills: ['Recruitment', 'Training'],
        matchWeights: [0.10, 0.35, 0.20, 0.25, 0.10]
    },
    {
        id: 'talent_acquisition',
        title: 'Talent Acquisition Specialist',
        category: 'Human Resources',
        requiredSkills: [
            { name: 'Sourcing', difficulty: 5 },
            { name: 'Interviewing', difficulty: 5 },
            { name: 'Employer Branding', difficulty: 5 },
            { name: 'ATS Tools', difficulty: 4 },
            { name: 'Networking', difficulty: 5 },
            { name: 'Assessment', difficulty: 4 }
        ],
        userSkills: ['Sourcing', 'Interviewing'],
        matchWeights: [0.10, 0.35, 0.20, 0.25, 0.10]
    },
    {
        id: 'people_ops',
        title: 'People Operations Manager',
        category: 'Human Resources',
        requiredSkills: [
            { name: 'HR Strategy', difficulty: 6 },
            { name: 'Data Analysis', difficulty: 4 },
            { name: 'Employee Engagement', difficulty: 5 },
            { name: 'Process Design', difficulty: 5 },
            { name: 'Compliance', difficulty: 5 },
            { name: 'HR Tech', difficulty: 4 }
        ],
        userSkills: ['Employee Engagement', 'Compliance'],
        matchWeights: [0.10, 0.30, 0.15, 0.30, 0.15]
    },
    // ===== Creative & Content =====
    {
        id: 'content_writer',
        title: 'Content Writer',
        category: 'Creative & Content',
        requiredSkills: [
            { name: 'Copywriting', difficulty: 5 },
            { name: 'SEO', difficulty: 4 },
            { name: 'Research', difficulty: 4 },
            { name: 'Editing', difficulty: 4 },
            { name: 'CMS', difficulty: 3 },
            { name: 'Storytelling', difficulty: 5 }
        ],
        userSkills: ['Copywriting', 'CMS', 'Editing'],
        matchWeights: [0.15, 0.25, 0.25, 0.20, 0.15]
    },
    {
        id: 'video_producer',
        title: 'Video Producer',
        category: 'Creative & Content',
        requiredSkills: [
            { name: 'Video Editing', difficulty: 5 },
            { name: 'Scriptwriting', difficulty: 4 },
            { name: 'Camera Operation', difficulty: 4 },
            { name: 'Color Grading', difficulty: 5 },
            { name: 'Motion Graphics', difficulty: 5 },
            { name: 'Project Mgmt', difficulty: 4 }
        ],
        userSkills: ['Video Editing', 'Scriptwriting'],
        matchWeights: [0.15, 0.20, 0.15, 0.20, 0.30]
    },
    {
        id: 'creative_director',
        title: 'Creative Director',
        category: 'Creative & Content',
        requiredSkills: [
            { name: 'Creative Vision', difficulty: 7 },
            { name: 'Team Leadership', difficulty: 6 },
            { name: 'Brand Strategy', difficulty: 6 },
            { name: 'Client Mgmt', difficulty: 5 },
            { name: 'Budgeting', difficulty: 5 },
            { name: 'Trend Analysis', difficulty: 5 }
        ],
        userSkills: ['Brand Strategy', 'Trend Analysis'],
        matchWeights: [0.20, 0.35, 0.20, 0.15, 0.10]
    },
    // ===== Professional Services =====
    {
        id: 'project_manager',
        title: 'Project Manager',
        category: 'Professional Services',
        requiredSkills: [
            { name: 'Project Planning', difficulty: 6 },
            { name: 'Risk Mgmt', difficulty: 5 },
            { name: 'Stakeholder Mgmt', difficulty: 5 },
            { name: 'Agile/Scrum', difficulty: 4 },
            { name: 'Budgeting', difficulty: 5 },
            { name: 'Communication', difficulty: 5 }
        ],
        userSkills: ['Agile/Scrum', 'Communication'],
        matchWeights: [0.15, 0.30, 0.15, 0.30, 0.10]
    },
    {
        id: 'legal_counsel',
        title: 'Legal Counsel',
        category: 'Professional Services',
        requiredSkills: [
            { name: 'Contract Law', difficulty: 8 },
            { name: 'Litigation', difficulty: 7 },
            { name: 'Compliance', difficulty: 6 },
            { name: 'Negotiation', difficulty: 6 },
            { name: 'Due Diligence', difficulty: 6 },
            { name: 'Legal Research', difficulty: 6 }
        ],
        userSkills: ['Negotiation', 'Compliance'],
        matchWeights: [0.20, 0.20, 0.40, 0.15, 0.05]
    },
    {
        id: 'supply_chain',
        title: 'Supply Chain Manager',
        category: 'Operations',
        requiredSkills: [
            { name: 'Supply Chain Strategy', difficulty: 6 },
            { name: 'Logistics', difficulty: 5 },
            { name: 'Inventory Mgmt', difficulty: 5 },
            { name: 'Vendor Relations', difficulty: 5 },
            { name: 'Data Analysis', difficulty: 4 },
            { name: 'ERP Systems', difficulty: 5 }
        ],
        userSkills: ['Data Analysis', 'Vendor Relations'],
        matchWeights: [0.20, 0.25, 0.20, 0.25, 0.10]
    }
];

// ===== Domain/Industry Matching =====
const CATEGORY_DOMAIN_MAP = {
    'Software Engineering': ['software', 'engineering', 'coding', 'development', 'programming', 'developer', 'code', '软件', '开发', '编程', '程序员', '工程师', '代码', '系统开发', '软件开发', '前端', '后端', '全栈'],
    'Infrastructure & DevOps': ['devops', 'cloud', 'infrastructure', 'sre', '运维', '云', '基础设施', '容器', '自动化', 'kubernetes', 'docker'],
    'Data & Analytics': ['data', 'analytics', 'sql', 'database', 'report', 'bi', '数据', '分析', '报表', '数据库', '商业智能', '数据分析', '数据仓库', 'etl'],
    'AI & Machine Learning': ['machine learning', 'ai', 'artificial intelligence', 'deep learning', 'neural network', 'model', '算法', '人工智能', '机器学习', '深度学习', '神经网络', '模型', '智能', '大模型', 'llm'],
    'Product & Design': ['product', 'design', 'user', 'ux', 'ui', 'prototype', '产品', '设计', '用户', '交互', '原型', '用户体验', '产品经理', '设计师'],
    'Marketing & Growth': ['marketing', 'growth', 'campaign', 'brand', 'advertising', 'promotion', '营销', '增长', '品牌', '广告', '推广', '市场', '运营', '活动策划', 'seo', 'sem'],
    'Operations': ['operations', 'logistics', 'supply chain', '运营', '物流', '供应链', '流程', '仓储', '配送', '库存', '采购'],
    'Sales & Business': ['sales', 'business', 'client', 'revenue', 'account', '销售', '商务', '客户', '业绩', '订单', '渠道', '大客户', 'bd', 'business development'],
    'Finance': ['finance', 'financial', 'investment', 'banking', 'valuation', 'accounting', 'budget', 'forecast', 'risk', 'equity', 'stock', 'bond', 'portfolio', 'asset', 'trading', 'market', 'ipo', 'merger', 'acquisition', '金融', '投资', '银行', '证券', '基金', '理财', '财务', '会计', '审计', '风控', '估值', '股票', '债券', '交易', '资产配置', '投行', '风控', '经济', '财政', '税务', '保险'],
    'Consulting': ['consulting', 'strategy', 'advisory', '咨询', '战略', '顾问', '管理咨询', '战略规划', '行业研究', 'case', 'case study'],
    'Leadership': ['leadership', 'management', 'director', 'vp', 'cto', 'ceo', 'head', '领导', '管理', '总监', '副总裁', '首席', '负责人', '总经理', 'executive'],
    'Human Resources': ['hr', 'human resources', 'talent', 'recruitment', 'people', '人力', '招聘', '员工', '人事', '绩效', '培训', '薪酬', '组织发展', 'od', '组织'],
    'Creative & Content': ['creative', 'content', 'writing', 'video', 'copy', 'script', '创意', '内容', '视频', '写作', '文案', '脚本', '编导', '剪辑', '拍摄', '新媒体', '自媒体'],
    'Professional Services': ['project', 'legal', 'compliance', 'law', 'contract', 'supply chain', '项目', '法律', '合规', '法务', '合同', '供应链', '采购', '项目管理']
};

// ===== Experience-to-Role Aliases =====
const ROLE_EXPERIENCE_ALIASES = {
    'investment_analyst': ['投资分析师', '投资助理', '投资经理', '行研', '行业研究', 'equity research', 'vc', 'venture capital', 'pe', 'private equity', '投资实习生', '投资实习', 'vc实习', 'pe实习', '投行实习', '投行', 'ib', 'investment banking', '券商', '卖方研究', '买方研究'],
    'financial_analyst': ['财务分析师', '财务分析', '财务助理', '财务经理', 'fp&a', '财务bp', '财务实习生', '财务实习'],
    'risk_manager': ['风险管理', '风控', '风险经理', '合规', '信用风险', '市场风险', '风控实习'],
    'quant_analyst': ['量化分析师', '量化', 'quant', '量化研究员', '量化实习', '量化交易'],
    'financial_advisor': ['理财顾问', '投资顾问', '财富管理', '私人银行', 'fa'],
    'data_scientist': ['数据科学家', '算法工程师', '数据挖掘', '数据科学', 'ds实习'],
    'ml_engineer': ['机器学习工程师', 'ml工程师', '模型工程师', '模型开发', '算法工程'],
    'data_engineer': ['数据工程师', '大数据开发', 'etl工程师', '数据开发', '数仓'],
    'research_scientist': ['研究员', '算法研究员', '研究科学家', '科研', 'ai lab'],
    'mlops_engineer': ['mlops', '机器学习平台', '模型部署', '算法平台'],
    'bi_analyst': ['bi分析师', '商业智能', 'bi分析', '经营分析'],
    'data_analyst': ['数据分析师', '数据分析', '商业分析', '数据运营', '分析实习'],
    'cv_engineer': ['计算机视觉', 'cv工程师', '图像算法', '视觉算法', '图像识别'],
    'nlp_engineer': ['自然语言处理', 'nlp算法', '文本算法', '语言模型', '大模型算法'],
    'prompt_engineer': ['提示词工程', 'prompt', '大模型应用', 'ai应用'],
    'frontend_dev': ['前端开发', '前端工程师', '前端', 'web前端', 'h5开发', '前端实习'],
    'backend_engineer': ['后端工程师', '服务端开发', '后端开发', '后端', '后台开发', '后端实习'],
    'fullstack_engineer': ['全栈工程师', '全栈开发', 'full stack', '全栈'],
    'mobile_dev': ['移动端开发', 'ios开发', 'android开发', 'app开发', '移动开发'],
    'devops_engineer': ['devops', '运维工程师', '运维开发', 'sre', '运维'],
    'cloud_architect': ['云架构师', '架构师', 'cloud', '云平台'],
    'security_engineer': ['安全工程师', '网络安全', '信息安全', '渗透测试', '安全研究'],
    'qa_engineer': ['测试工程师', '自动化测试', 'qa', '质量保证', '测试开发'],
    'game_dev': ['游戏开发', '游戏工程师', 'unity开发', 'ue开发', '游戏客户端'],
    'product_manager': ['产品经理', '产品', 'pm', '产品助理', '产品实习', '产品专员'],
    'technical_pm': ['技术产品经理', '技术pm', '技术产品'],
    'growth_pm': ['增长产品经理', '增长pm', '增长产品'],
    'ai_product_manager': ['ai产品经理', '人工智能产品经理', '算法产品经理'],
    'ux_designer': ['用户体验设计', '交互设计', 'ux设计', 'ux designer'],
    'ui_designer': ['ui设计', 'ui设计师', '界面设计', '视觉设计'],
    'product_designer': ['产品设计师', '产品设计', '产品体验设计'],
    'digital_marketing': ['数字营销', '营销经理', '市场推广', '品牌营销', '营销策划'],
    'content_marketing': ['内容营销', '内容运营', '新媒体运营', '自媒体'],
    'growth_hacker': ['增长黑客', '用户增长', '增长运营', 'growth'],
    'social_media': ['社交媒体', '社媒运营', '新媒体', '社群运营'],
    'seo_specialist': ['seo', '搜索引擎优化', 'seo优化', '自然流量'],
    'ops_manager': ['运营经理', '运营主管', '运营管理', '运营总监'],
    'community_manager': ['社区运营', '社群运营', '用户运营', '社区经理'],
    'sales_manager': ['销售经理', '销售主管', '销售总监', '销售负责人'],
    'account_exec': ['大客户销售', '客户经理', '销售代表', 'bd', '商务'],
    'bd_manager': ['商务拓展', 'bd经理', '商务经理', '商务总监'],
    'customer_success': ['客户成功', '客户成功经理', 'csm', '客户运营'],
    'mgmt_consultant': ['管理咨询', '咨询顾问', '战略咨询', '咨询公司', 'consulting'],
    'strategy_consultant': ['战略咨询', '战略顾问', '战略分析', '商业分析'],
    'eng_manager': ['工程经理', '技术经理', '研发经理', '开发经理', '技术主管'],
    'eng_director': ['工程总监', '技术总监', '研发总监', '技术vp'],
    'cto': ['cto', '首席技术官', '技术副总裁', '技术vp'],
    'hr_manager': ['人力资源经理', '人事经理', 'hr经理', 'hrbp', '人力'],
    'talent_acquisition': ['招聘专员', '招聘专家', '猎头', '招聘经理', '招聘'],
    'people_ops': ['人力运营', '员工关系', '组织发展', 'od', 'coe'],
    'content_writer': ['内容作者', '撰稿人', '文案', '编辑', '写手', '记者'],
    'video_producer': ['视频制作', '视频编导', '制片人', '导演', '剪辑'],
    'creative_director': ['创意总监', '创意主管', '艺术总监', '创意负责人'],
    'project_manager': ['项目经理', '项目管理', 'pm', '项目主管', '项目助理'],
    'legal_counsel': ['法务', '法律顾问', '律师', '法务经理', '合规'],
    'supply_chain': ['供应链', '采购', '物流', '仓储', '供应链经理']
};



// ===== DOM Elements =====
const els = {
    steps: document.querySelectorAll('.step-section'),
    navSteps: document.querySelectorAll('.nav-step'),
    qInputs: document.querySelectorAll('.question-input'),
    qProgress: document.getElementById('q-progress'),
    btnStep1Next: document.getElementById('btn-step1-next'),
    btnStep2Next: document.getElementById('btn-step2-next'),
    btnStep2Back: document.getElementById('btn-step2-back'),
    btnRestart: document.getElementById('btn-restart'),
    step1Hint: document.getElementById('step1-hint'),
    cvWork: document.getElementById('cv-work'),
    cvSkills: document.getElementById('cv-skills'),
    cvGrowth: document.getElementById('cv-growth'),
    finalDnaScore: document.getElementById('final-dna-score'),
    qBars: document.getElementById('q-bars'),
    cvBars: document.getElementById('cv-bars'),
    fusedBars: document.getElementById('fused-bars'),
    roleList: document.getElementById('role-list'),
    skillGap: document.getElementById('skill-gap'),
    formulaDna: document.getElementById('formula-dna'),
    formulaRec: document.getElementById('formula-rec'),
    formulaTransition: document.getElementById('formula-transition'),
    cvFileInput: document.getElementById('cv-file-input'),
    uploadZone: document.getElementById('upload-zone'),
    uploadStatus: document.getElementById('upload-status'),
    cvUploadArea: document.getElementById('cv-upload-area'),
    jobMatchCard: document.getElementById('job-match-card'),
    jobMatchLoading: document.getElementById('job-match-loading'),
    jobMatchError: document.getElementById('job-match-error'),
    jobMatchConfig: document.getElementById('job-match-config'),
    jobList: document.getElementById('job-list'),
    bossCookieInput: document.getElementById('boss-cookie-input'),
    btnFindJobs: document.getElementById('btn-find-jobs'),
    btnSaveCookie: document.getElementById('btn-save-cookie')
};

let radarChart = null;

// ===== Initialization =====
function init() {
    bindEvents();
    updateProgress();
    validateStep1();
}

function bindEvents() {
    // Questionnaire inputs
    els.qInputs.forEach((input, idx) => {
        input.addEventListener('input', (e) => {
            const qKey = `q${idx + 1}`;
            state.questionnaire[qKey] = e.target.value;
            
            // Update word count
            const item = input.closest('.question-item');
            const countEl = item.querySelector('.word-count');
            countEl.textContent = e.target.value.length;
            
            updateProgress();
            validateStep1();
        });
    });

    // Navigation buttons
    els.btnStep1Next.addEventListener('click', () => goToStep(2));
    if (els.btnStep2Next) els.btnStep2Next.addEventListener('click', () => startAnalysis());
    els.btnStep2Back.addEventListener('click', () => goToStep(1));
    els.btnRestart.addEventListener('click', () => restart());
    if (els.btnFindJobs) els.btnFindJobs.addEventListener('click', () => findMatchingJobs());
    if (els.btnSaveCookie) els.btnSaveCookie.addEventListener('click', () => saveBossCookie());

    // CV Upload events
    bindUploadEvents();
}

// ===== Navigation =====
function goToStep(step) {
    state.step = step;
    
    els.steps.forEach((section, idx) => {
        section.classList.toggle('active', idx + 1 === step);
    });
    
    els.navSteps.forEach((nav, idx) => {
        nav.classList.remove('active', 'completed');
        if (idx + 1 === step) nav.classList.add('active');
        else if (idx + 1 < step) nav.classList.add('completed');
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateProgress() {
    const filled = Object.values(state.questionnaire).filter(v => v.length > 10).length;
    const pct = (filled / 5) * 100;
    els.qProgress.style.width = `${pct}%`;
}

function validateStep1() {
    const entries = Object.entries(state.questionnaire);
    const missing = entries
        .filter(([key, val]) => val.length < 5)
        .map(([key]) => key.replace('q', 'Q'));
    
    const allFilled = missing.length === 0;
    els.btnStep1Next.disabled = !allFilled;
    
    if (allFilled) {
        els.step1Hint.classList.add('valid');
        els.step1Hint.innerHTML = `
            <span class="hint-icon">✅</span>
            <span class="hint-text">完成！点击「继续」进入简历分析</span>
        `;
    } else {
        els.step1Hint.classList.remove('valid');
        const missingText = missing.join('、');
        els.step1Hint.innerHTML = `
            <span class="hint-icon">💡</span>
            <span class="hint-text">还差 <span class="missing-q">${missingText}</span> 未填够字数（至少 5 个字符）</span>
        `;
    }
}

function restart() {
    state.questionnaire = { q1: '', q2: '', q3: '', q4: '', q5: '' };
    state.cv = { work: '', skills: '', growth: '' };
    
    els.qInputs.forEach(input => input.value = '');
    document.querySelectorAll('.word-count').forEach(el => el.textContent = '0');
    els.cvWork.value = '';
    els.cvSkills.value = '';
    els.cvGrowth.value = '';
    
    updateProgress();
    validateStep1();
    goToStep(1);
}

// ===== Analysis Pipeline =====
function startAnalysis() {
    // Capture CV data
    state.cv.work = els.cvWork.value;
    state.cv.skills = els.cvSkills.value;
    state.cv.growth = els.cvGrowth.value;
    
    goToStep(3);
    
    // Simulate processing steps
    const procSteps = document.querySelectorAll('.proc-step');
    procSteps.forEach(s => s.classList.remove('active', 'completed'));
    
    const steps = [
        { id: 'proc-1', delay: 500, action: () => {} },
        { id: 'proc-2', delay: 1200, action: () => {} },
        { id: 'proc-3', delay: 2000, action: () => computeScores() },
        { id: 'proc-4', delay: 2800, action: () => fuseScores() },
        { id: 'proc-5', delay: 3500, action: () => generateRecommendations() }
    ];
    
    steps.forEach((step, idx) => {
        setTimeout(() => {
            // Mark previous as completed
            if (idx > 0) {
                document.getElementById(steps[idx - 1].id).classList.remove('active');
                document.getElementById(steps[idx - 1].id).classList.add('completed');
            }
            // Mark current as active
            document.getElementById(step.id).classList.add('active');
            step.action();
            
            // Final step - show results
            if (idx === steps.length - 1) {
                setTimeout(() => {
                    renderResults();
                    goToStep(4);
                }, 800);
            }
        }, step.delay);
    });
}

// ===== Scoring Logic =====
function computeScores() {
    // Simulate LLM-based questionnaire scoring
    // In a real app, this would call an LLM API
    const qText = Object.values(state.questionnaire).join(' ').toLowerCase();
    
    // Keyword-based heuristic scoring for demo
    state.scores.q = [
        scoreDimension(qText, 'd1'), // Core Competency
        scoreDimension(qText, 'd2'), // Mindset
        scoreDimension(qText, 'd3'), // Domain
        scoreDimension(qText, 'd4'), // Methodology
        scoreDimension(qText, 'd5')  // Tools
    ];
    
    // CV scoring
    const cvText = `${state.cv.work} ${state.cv.skills} ${state.cv.growth}`.toLowerCase();
    state.scores.cv = [
        scoreDimension(cvText, 'd1_cv'),
        scoreDimension(cvText, 'd2_cv'),
        scoreDimension(cvText, 'd3_cv'),
        scoreDimension(cvText, 'd4_cv'),
        scoreDimension(cvText, 'd5_cv')
    ];
}

function scoreDimension(text, dim) {
    const keywords = {
        d1: ['system', 'pattern', 'analytical', 'complex', 'problem', 'architecture', 'design', 'structure', 'model', 'framework', 'abstract', 'logic',
             '系统', '架构', '设计', '模型', '框架', '抽象', '逻辑', '复杂', '分析', '问题'],
        d2: ['curious', 'learn', 'adapt', 'collaborat', 'communicat', 'empathy', 'resilien', 'growth', 'mindset', 'team', 'lead', 'mentor',
             '好奇', '学习', '适应', '协作', '沟通', '同理心', '韧性', '成长', '团队', '领导', '指导'],
        d3: ['industry', 'domain', 'sector', 'expertise', 'subject', 'field', 'knowledge', 'specializ', 'deep', 'experience',
             '金融', '投资', '银行', '证券', '基金', '保险', '财务', '会计', '审计', '法律', '医疗', '教育', '制造', '零售', '电商', '房地产', '能源', '汽车', '医药',
             '行业', '领域', '专业', '知识', '经验', '深度', '专长'],
        d4: ['process', 'methodology', 'framework', 'agile', 'scrum', 'workflow', 'research', 'structured', 'systematic', 'approach', 'strategy',
             '流程', '方法论', '框架', '敏捷', '工作流', '研究', '结构化', '系统化', '方法', '策略', '规划'],
        d5: ['python', 'tool', 'software', 'platform', 'code', 'program', 'technical', 'proficien', 'language', 'certification',
             '工具', '软件', '平台', '代码', '编程', '技术', '语言', '认证', '熟练', '精通'],
        d1_cv: ['project', 'complex', 'system', 'architect', 'design', 'lead', 'implement', 'scale', 'performance', 'optimize',
                '项目', '复杂', '系统', '架构', '设计', '主导', '实现', '搭建', '优化', '提升', '改进', '性能', '规模'],
        d2_cv: ['lead', 'manage', 'team', 'collaborat', 'cross-functional', 'stakeholder', 'adapt', 'pivot', 'transform',
                '领导', '管理', '团队', '协作', '跨部门', '跨职能', '利益相关方', '适应', '转型', '变革', '带领', '协调'],
        d3_cv: ['industry', 'domain', 'sector', 'expert', 'specialist', 'certification', 'years', 'experience', 'deep',
                '金融', '投资', '银行', '证券', '基金', '保险', '财务', '会计', '审计', '风控', '估值', '投行', '理财', '经济', '财政', '税务',
                '行业', '领域', '专业', '专家', '认证', '经验', '资深', '深度'],
        d4_cv: ['process', 'framework', 'methodology', 'agile', 'scrum', 'kanban', 'manage', 'own', 'implement', 'design',
                '流程', '框架', '方法论', '敏捷', '看板', '管理', '负责', '实施', '设计', '落地', '执行', '推进', '落实'],
        d5_cv: ['python', 'sql', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'tensorflow', 'pytorch', 'tableau', 'tool', 'stack',
                'python', 'sql', '数据库', '云', '容器', '深度学习', '机器学习', '可视化', '工具', '技术栈', '编程', '开发']
    };
    
    const words = keywords[dim] || [];
    let matches = 0;
    words.forEach(word => {
        if (text.includes(word)) matches++;
    });
    
    // Add some randomness for demo variety, but keep it realistic (4-9 range)
    const base = Math.min(10, 4 + matches * 0.8);
    const noise = (Math.random() - 0.5) * 1.5;
    return Math.max(1, Math.min(10, Math.round((base + noise) * 10) / 10));
}

function fuseScores() {
    // D_Fused,i = 0.4 * D_Q,i + 0.6 * D_CV,i
    for (let i = 0; i < 5; i++) {
        state.scores.fused[i] = 0.4 * state.scores.q[i] + 0.6 * state.scores.cv[i];
    }
    
    // DNA_Fused = sum(D_i * weight_i)
    state.dnaScore = 0;
    for (let i = 0; i < 5; i++) {
        state.dnaScore += state.scores.fused[i] * DIM_WEIGHTS[i];
    }
    state.dnaScore = Math.round(state.dnaScore * 10) / 10;
}


function extractUserSkills(cvText) {
    const text = cvText.toLowerCase();
    const userSkills = new Set();
    
    // Scan all required skills from all roles against the resume text
    ACKG_ROLES.forEach(role => {
        role.requiredSkills.forEach(rs => {
            const name = rs.name.toLowerCase();
            // Exact match
            if (text.includes(name)) {
                userSkills.add(rs.name);
                return;
            }
            // Partial match for compound skills (e.g. "TensorFlow/PyTorch")
            const parts = name.split(/[\/\s&,.\-]+/).filter(p => p.length > 2);
            for (const part of parts) {
                if (text.includes(part)) {
                    userSkills.add(rs.name);
                    break;
                }
            }
        });
    });
    
    return Array.from(userSkills);
}

function calculateDomainMatch(cvText, category) {
    const indicators = CATEGORY_DOMAIN_MAP[category] || [];
    if (indicators.length === 0) return 0.3;
    
    const text = cvText.toLowerCase();
    let matches = 0;
    indicators.forEach(kw => {
        const regex = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        const found = text.match(regex);
        if (found) matches += found.length;
    });
    
    // Threshold: need at least some matches to be considered domain-relevant
    const threshold = 2;
    const score = Math.min(1, matches / threshold);
    return score;
}


function calculateExperienceMatch(cvText, role) {
    const text = cvText.toLowerCase();
    let score = 0;
    
    // 1. Explicit alias match (highest weight) - e.g. "VC实习" matches Investment Analyst
    const aliases = ROLE_EXPERIENCE_ALIASES[role.id] || [];
    aliases.forEach(alias => {
        if (text.includes(alias.toLowerCase())) score += 0.35;
    });
    
    // 2. Full job title match
    const titleLower = role.title.toLowerCase();
    if (text.includes(titleLower)) score += 0.6;
    
    // 3. Title word matches
    const titleWords = titleLower.split(/\s+/).filter(w => w.length > 3);
    titleWords.forEach(word => {
        if (text.includes(word)) score += 0.12;
    });
    
    // 4. Category/domain keyword matches
    const domainKeywords = CATEGORY_DOMAIN_MAP[role.category] || [];
    domainKeywords.forEach(kw => {
        const kwLower = kw.toLowerCase();
        if (text.includes(kwLower)) score += 0.08;
    });
    
    // 5. Experience pattern matches (intern, senior, assistant, etc.)
    titleWords.forEach(word => {
        const patterns = [
            word + ' intern', word + '实习',
            'senior ' + word, 'junior ' + word,
            word + '助理', word + '经理', word + '总监', word + '主管'
        ];
        patterns.forEach(p => {
            if (text.includes(p.toLowerCase())) score += 0.25;
        });
    });
    
    // 6. Required skill matches (low weight)
    role.requiredSkills.forEach(rs => {
        const parts = rs.name.toLowerCase().split(/[\/\s&,.\-]+/).filter(p => p.length > 2);
        parts.forEach(part => {
            if (text.includes(part)) score += 0.02;
        });
    });
    
    return Math.min(1, score);
}

function generateRecommendations() {
    const cvText = (state.cv.work + ' ' + state.cv.skills + ' ' + state.cv.growth).toLowerCase();
    const userSkills = extractUserSkills(cvText);
    
    state.recommendations = ACKG_ROLES.map(role => {
        // 5D profile alignment
        let matchScore = 0;
        for (let i = 0; i < 5; i++) {
            matchScore += state.scores.fused[i] * role.matchWeights[i];
        }
        
        // Domain/industry matching: boost roles that match the resume's industry
        const domainMatch = calculateDomainMatch(cvText, role.category);
        
        // Skill gaps based on ACTUAL extracted skills from resume (not hardcoded)
        const missingSkills = role.requiredSkills.filter(rs => {
            const rsName = rs.name.toLowerCase();
            return !userSkills.some(us => {
                const usName = us.toLowerCase();
                return usName.includes(rsName) || rsName.includes(usName) ||
                       rsName.split(/[\/\s&,.\-]+/).some(p => p.length > 2 && usName.includes(p));
            });
        });
        
        const transitionEffort = missingSkills.reduce((sum, s) => sum + s.difficulty, 0);
        const maxEffort = role.requiredSkills.reduce((sum, s) => sum + s.difficulty, 0);
        const normalizedEffort = transitionEffort / maxEffort;
        const transitionEase = Math.round((1 - normalizedEffort) * 10 * 10) / 10;
        
        // Penalty proportional to skill gap
        const penalty = normalizedEffort * 2;
        
        // GraphDebiaser
        const debiaser = 0.95 + Math.random() * 0.1;
        
        // Final score combines 5D match + domain match + experience match + skill coverage
        // Domain match: 0.1-1.0 multiplier (non-matching industry gets 10% only)
        const domainBoost = 0.1 + 0.9 * domainMatch;
        
        // Experience match: 0.2-1.0 multiplier (past role relevance)
        const experienceMatch = calculateExperienceMatch(cvText, role);
        const expBoost = 0.2 + 0.8 * experienceMatch;
        
        // Combined weighted match
        const weightedMatch = matchScore * domainBoost * expBoost;
        
        // Skill coverage boost: reward roles where user already has many required skills
        const skillCoverage = 1 - normalizedEffort;
        const skillBoost = skillCoverage * 1.5;
        
        // Extra penalty for completely mismatched domains
        const domainPenalty = domainMatch < 0.2 ? 1.5 : 0;
        const recScore = Math.round((weightedMatch + skillBoost - penalty - domainPenalty) * debiaser * 10) / 10;
        
        return {
            ...role,
            matchScore: Math.round(matchScore * 10) / 10,
            transitionEase,
            recScore,
            missingSkills,
            transitionEffort,
            maxEffort,
            domainMatch
        };
    }).sort((a, b) => b.recScore - a.recScore).slice(0, 3);
}
// ===== Rendering =====
function renderResults() {
    // DNA Score
    animateNumber(els.finalDnaScore, state.dnaScore);
    
    // Radar Chart
    renderRadarChart();
    
    // Score Bars
    renderBars(els.qBars, state.scores.q, 'q');
    renderBars(els.cvBars, state.scores.cv, 'cv');
    renderBars(els.fusedBars, state.scores.fused, 'fused');
    
    // Formulas
    renderFormulas();
    
    // Roles
    renderRoles();
    
    // Skill Gaps (removed)
}

function animateNumber(el, target) {
    let current = 0;
    const step = target / 40;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = current.toFixed(1);
    }, 25);
}

function renderRadarChart() {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    if (radarChart) radarChart.destroy();
    
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: DIM_LABELS,
            datasets: [
                {
                    label: '问卷 (隐性)',
                    data: state.scores.q,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#06b6d4',
                    pointRadius: 4
                },
                {
                    label: '简历 (显性)',
                    data: state.scores.cv,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#f59e0b',
                    pointRadius: 4
                },
                {
                    label: '融合画像',
                    data: state.scores.fused,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.15)',
                    borderWidth: 3,
                    pointBackgroundColor: '#6366f1',
                    pointRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    min: 0,
                    ticks: {
                        stepSize: 2,
                        color: '#64748b',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: '#2a3142'
                    },
                    angleLines: {
                        color: '#2a3142'
                    },
                    pointLabels: {
                        color: '#94a3b8',
                        font: { size: 12, weight: '600' }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function renderBars(container, scores, type) {
    container.innerHTML = '';
    scores.forEach((score, idx) => {
        const row = document.createElement('div');
        row.className = 'dim-bar-row';
        row.innerHTML = `
            <span class="dim-bar-label">D${idx + 1}</span>
            <div class="dim-bar-track">
                <div class="dim-bar-fill ${type}" style="width: 0%"></div>
            </div>
            <span class="dim-bar-value">${score.toFixed(1)}</span>
        `;
        container.appendChild(row);
        
        // Animate
        setTimeout(() => {
            row.querySelector('.dim-bar-fill').style.width = `${score * 10}%`;
        }, 100 + idx * 100);
    });
}

function renderFormulas() {
    // DNA Formula
    const dnaTerms = DIM_WEIGHTS.map((w, i) => 
        `D${i+1}<sub>Fused</sub> × ${(w * 100).toFixed(0)}%`
    ).join(' + ');
    
    els.formulaDna.innerHTML = `
        <div style="font-family:'JetBrains Mono',monospace;line-height:2;">
            <div style="color:var(--text-muted);margin-bottom:4px;">DNA<sub>Fused</sub> = Σ(D<sub>i</sub> × w<sub>i</sub>)</div>
            <div>${dnaTerms}</div>
            <div style="color:var(--accent-primary);font-weight:600;margin-top:4px;">= ${state.dnaScore.toFixed(2)}</div>
        </div>
    `;
    
    // Recommendation Formula
    els.formulaRec.innerHTML = `
        <div style="font-family:'JetBrains Mono',monospace;line-height:2;">
            <div>RecScore = (MatchScore − Penalty) × GraphDebiaser</div>
            <div style="color:var(--text-muted);font-size:12px;margin-top:4px;">Penalty = NormalizedEffort × 2</div>
        </div>
    `;
    
    // Transition Formula
    els.formulaTransition.innerHTML = `
        <div style="font-family:'JetBrains Mono',monospace;line-height:2;">
            <div>TransitionEase = (1 − TransitionEffort / MaxEffort) × 10</div>
            <div style="color:var(--text-muted);font-size:12px;margin-top:4px;">0 = very hard pivot, 10 = seamless transition</div>
        </div>
    `;
}

function renderRoles() {
    els.roleList.innerHTML = '';
    const ranks = ['gold', 'silver', 'bronze'];
    
    state.recommendations.forEach((role, idx) => {
        const item = document.createElement('div');
        item.className = 'role-item';
        
        const easeClass = role.transitionEase >= 7 ? 'high' : role.transitionEase >= 4 ? 'medium' : 'low';
        const easeLabel = role.transitionEase >= 7 ? 'Easy' : role.transitionEase >= 4 ? 'Medium' : 'Hard';
        
        const allSkillNames = role.requiredSkills.map(s => s.name);
        const missingNames = role.missingSkills.map(s => s.name);
        
        item.innerHTML = `
            <div class="role-rank ${ranks[idx]}">#${idx + 1}</div>
            <div class="role-content">
                <div class="role-title">${role.title}</div>
                <div class="role-category">${role.category}</div>
                <div class="role-metrics">
                    <div class="role-metric">
                        <span class="metric-label">匹配得分</span>
                        <span class="metric-value high">${role.matchScore.toFixed(1)}</span>
                    </div>
                    <div class="role-metric">
                        <span class="metric-label">推荐得分</span>
                        <span class="metric-value high">${role.recScore.toFixed(1)}</span>
                    </div>
                    <div class="role-metric">
                        <span class="metric-label">转型难度</span>
                        <span class="metric-value ${easeClass}">${role.transitionEase.toFixed(1)}</span>
                    </div>
                </div>
            </div>
            <div class="role-skills">
                <h5>技能覆盖</h5>
                <div class="skill-tags">
                    ${allSkillNames.map(name => 
                        `<span class="skill-tag ${missingNames.includes(name) ? 'missing' : ''}">${name}</span>`
                    ).join('')}
                </div>
            </div>
        `;
        els.roleList.appendChild(item);
    });
}

function renderSkillGaps() {
    els.skillGap.innerHTML = '';
    
    state.recommendations.forEach(role => {
        const card = document.createElement('div');
        card.className = 'gap-role';
        
        const easeClass = role.transitionEase >= 7 ? 'easy' : role.transitionEase >= 4 ? 'medium' : 'hard';
        const easeText = role.transitionEase >= 7 ? '较容易' : role.transitionEase >= 4 ? '中等' : '较困难';
        
        card.innerHTML = `
            <div class="gap-role-header">
                <span class="gap-role-name">${role.title}</span>
                <span class="gap-ease ${easeClass}">转型 ${easeText}</span>
            </div>
            <div class="gap-skills-list">
                ${role.requiredSkills.map(skill => {
                    const isMissing = role.missingSkills.some(ms => ms.name === skill.name);
                    const pct = (skill.difficulty / 10) * 100;
                    return `
                        <div class="gap-skill">
                            <span class="gap-skill-name">
                                ${isMissing ? '⚠️ ' : '✅ '}${skill.name}
                            </span>
                            <div class="gap-difficulty">
                                <div class="difficulty-bar">
                                    <div class="difficulty-fill" style="width: ${pct}%"></div>
                                </div>
                                <span class="difficulty-value">${skill.difficulty}</span>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
            <div class="gap-summary">
                <span class="gap-summary-label">缺失技能数</span>
                <span class="gap-summary-value">${role.missingSkills.length} / ${role.requiredSkills.length}</span>
            </div>
            <div class="gap-summary">
                <span class="gap-summary-label">总转型努力</span>
                <span class="gap-summary-value">${role.transitionEffort} / ${role.maxEffort}</span>
            </div>
        `;
        els.skillGap.appendChild(card);
    });
}

// ===== CV Upload & Parsing =====
function bindUploadEvents() {
    if (!els.cvFileInput) return;

    // Configure PDF.js worker (required for v3.x)
    if (typeof pdfjsLib !== 'undefined') {
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js';
    }

    // File selected (input now covers the whole upload zone via CSS)
    els.cvFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
        // Reset input so same file can be selected again
        els.cvFileInput.value = '';
    });

    // Drag & drop (on the card, not the input)
    if (els.cvUploadArea) {
        els.cvUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            els.cvUploadArea.classList.add('dragover');
        });

        els.cvUploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            els.cvUploadArea.classList.remove('dragover');
        });

        els.cvUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            els.cvUploadArea.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file) handleFile(file);
        });
    }
}

async function handleFile(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    const validExts = ['pdf', 'docx', 'doc', 'txt'];

    if (!validExts.includes(ext)) {
        setUploadStatus('❌ 不支持的文件格式，请上传 PDF / Word / 文本文件', 'error');
        return;
    }

    setUploadStatus('<span class="spinner"></span>正在提取简历文本...', 'processing');
    els.cvUploadArea.classList.add('processing');

    try {
        let text = '';
        if (ext === 'pdf') {
            text = await extractPDF(file);
        } else if (ext === 'docx' || ext === 'doc') {
            text = await extractWord(file);
        } else {
            text = await extractText(file);
        }

        if (!text || text.trim().length < 20) {
            setUploadStatus('⚠️ 未能提取到有效文本，请尝试手动粘贴', 'warning');
            els.cvUploadArea.classList.remove('processing');
            return;
        }

        classifyAndFill(text);
        setUploadStatus(`✅ 已提取「${file.name}」，正在启动分析...`, 'success');
        els.cvUploadArea.classList.add('done');
        
        // Auto-start analysis after brief delay
        setTimeout(() => {
            startAnalysis();
        }, 600);
    } catch (err) {
        console.error('File parse error:', err);
        setUploadStatus('⚠️ 解析失败，请尝试手动粘贴内容', 'error');
        els.cvUploadArea.classList.remove('processing');
    }
}

function setUploadStatus(html, type) {
    if (!els.uploadStatus) return;
    els.uploadStatus.innerHTML = html;
}

async function extractPDF(file) {
    try {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let text = '';
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            const pageText = content.items.map(item => item.str).join(' ');
            text += pageText + '\n';
        }
        return text;
    } catch (err) {
        console.error('PDF extract error:', err);
        throw new Error('PDF解析失败: ' + err.message);
    }
}

async function extractWord(file) {
    try {
        if (typeof mammoth === 'undefined') {
            throw new Error('Word解析库未加载');
        }
        const arrayBuffer = await file.arrayBuffer();
        const result = await mammoth.extractRawText({ arrayBuffer });
        return result.value;
    } catch (err) {
        console.error('Word extract error:', err);
        throw new Error('Word解析失败: ' + err.message);
    }
}

async function extractText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('文件读取失败'));
        reader.readAsText(file);
    });
}

// ===== Resume Section Classifier =====

// ===== Resume Text Classifier (Rewrite) =====
// Three categories: work (经历+项目), skills (技术+工具), growth (发展+领导力+教育)

// Exact section headers only — no loose prefix matching to avoid false positives
const SECTION_HEADERS = {
    work: [
        'work experience','professional experience','employment history','career history',
        'work history','professional background','experience','employment','career',
        'projects','selected projects','project experience','key projects',
        '工作经历','工作经验','项目经历','项目经验','实习经历','实习经验',
        '职业经历','从业经历','相关经验','工作履历','项目成果','主要项目',
        'professional experience','employment','work'
    ],
    skills: [
        'skills','technical skills','tech stack','technologies','technical expertise',
        'proficiencies','competencies','tools','software','programming languages',
        'certifications','technical proficiencies',
        '技能','技术栈','专业技能','技术能力','工具','证书','认证',
        '掌握技能','技术技能','开发工具','熟悉工具','语言能力','软件技能',
        '专业技能','计算机技能'
    ],
    growth: [
        'leadership','management experience','team leadership','professional development',
        'education','educational background','awards','honors','publications',
        'presentations','volunteer','summary','objective','profile','personal summary',
        'about me','career objective','professional summary',
        '领导力','管理能力','团队管理','教育背景','学历','荣誉','获奖',
        '自我评价','个人优势','核心竞争力','综合素质','个人简介','职业目标','关于我'
    ]
};

function classifyAndFill(fullText) {
    const lines = fullText.split(/\n|\r\n/).map(l => l.trim()).filter(l => l.length > 0);
    
    // Step 1: Split resume into sections based on explicit headers
    const sections = [];
    let current = { type: 'unknown', lines: [] };
    
    for (const line of lines) {
        if (isNoiseLine(line)) continue;
        
        const headerType = detectSectionHeader(line);
        if (headerType) {
            if (current.lines.length > 0) {
                sections.push(current);
            }
            current = { type: headerType, lines: [] };
        } else {
            current.lines.push(line);
        }
    }
    if (current.lines.length > 0) sections.push(current);
    
    // Step 2: Classify each section's content
    const result = { work: [], skills: [], growth: [] };
    
    for (const section of sections) {
        if (section.type !== 'unknown') {
            // Section had explicit header — content goes to that category
            // But within work sections, some lines might be skill lists
            if (section.type === 'work') {
                const { workLines, skillLines } = splitWorkSection(section.lines);
                result.work.push(...workLines);
                result.skills.push(...skillLines);
            } else {
                result[section.type].push(...section.lines);
            }
        } else {
            // No header — classify line by line
            for (const line of section.lines) {
                const cat = classifySingleLine(line);
                result[cat].push(line);
            }
        }
    }
    
    // Step 3: Fill textareas
    els.cvWork.value = formatLines(result.work);
    els.cvSkills.value = formatLines(result.skills);
    els.cvGrowth.value = formatLines(result.growth);
    
    state.cv.work = els.cvWork.value;
    state.cv.skills = els.cvSkills.value;
    state.cv.growth = els.cvGrowth.value;
}

function detectSectionHeader(line) {
    const cleaned = line.toLowerCase()
        .replace(/^[\s\-–—*•·◦○●▪▫\d\.]+/, '') // Remove leading bullets/numbers
        .replace(/[：:\-\*\#\=\_\|]+$/, '')     // Remove trailing separators
        .replace(/\s+/g, ' ')
        .trim();
    
    // Header must be short (1-5 words) and not contain dates
    const words = cleaned.split(/\s+/);
    if (words.length > 6 || cleaned.length > 50) return null;
    if (cleaned.match(/\d{4}/)) return null; // Lines with years are not headers
    
    // Exact match
    for (const [type, headers] of Object.entries(SECTION_HEADERS)) {
        for (const h of headers) {
            if (cleaned === h) return type;
        }
    }
    
    return null;
}

function isNoiseLine(line) {
    if (line.match(/^\s*\d+\s*\/\s*\d+\s*$/)) return true; // Page numbers
    if (line.match(/^\s*page\s*\d+\s*$/i)) return true;
    if (line.match(/^[\w\.-]+@[\w\.-]+\.\w+$/)) return true; // Email only
    if (line.match(/^[\+\(\)\d\s\-]{7,20}$/)) return true; // Phone only
    if (line.match(/^https?:\/\//)) return true; // URL only
    if (line.length < 3) return true;
    return false;
}

function classifySingleLine(line) {
    const lower = line.toLowerCase();
    
    // Strong signal: date range → work experience
    if (line.match(/20\d\d\s*[\-\–—~\/]\s*(20\d\d|至今|present|current|now)/i)) {
        return 'work';
    }
    if (line.match(/^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+20\d\d/i)) {
        return 'work';
    }
    
    // Strong signal: education pattern → growth
    if (line.match(/(university|college|institute|school|大学|学院|本科|硕士|博士|mba|ph\.?d)/i) &&
        line.match(/20\d\d/)) {
        return 'growth';
    }
    
    // Strong signal: skill list pattern → skills
    const techCount = countTechKeywords(lower);
    if (techCount >= 3 && line.length < 200) {
        return 'skills';
    }
    
    // Score-based classification
    const wScore = scoreWorkLine(lower);
    const sScore = scoreSkillsLine(lower);
    const gScore = scoreGrowthLine(lower);
    
    // Skills need to be clearly dominant
    if (sScore >= 2 && sScore > wScore + 1 && sScore > gScore + 1) {
        return 'skills';
    }
    
    // Growth needs strong signal
    if (gScore >= 2 && gScore > wScore && gScore > sScore) {
        return 'growth';
    }
    
    // Default to work (resume body is mostly work experience)
    return 'work';
}

function splitWorkSection(lines) {
    const workLines = [];
    const skillLines = [];
    
    for (const line of lines) {
        const lower = line.toLowerCase();
        const techCount = countTechKeywords(lower);
        
        // If line is mostly tech keywords and short → skill line
        if (techCount >= 3 && line.length < 150 && !line.match(/20\d\d/)) {
            skillLines.push(line);
        } else {
            workLines.push(line);
        }
    }
    
    return { workLines, skillLines };
}

function scoreWorkLine(text) {
    const workSignals = [
        'engineer','developer','manager','analyst','consultant','director','specialist',
        'architect','designer','scientist','researcher','coordinator','fellow',
        '工程师','分析师','经理','顾问','总监','专员','架构师','设计师',
        '研究员','科学家','协调员','主管','负责人','实习生',
        'project','product','platform','system','application','feature','module',
        'service','pipeline','workflow','dashboard','report','model','algorithm',
        '项目','产品','平台','系统','应用','功能','模块','服务','流程','报表','模型','算法',
        'company','inc','corp','ltd','limited','technologies','科技','公司','集团',
        'responsible','负责','主导','参与','承担','完成','实现','搭建','优化','提升',
        '改进','设计','开发','维护','部署','测试','上线','交付','支持','协助',
        'developed','implemented','designed','built','maintained','deployed',
        'launched','delivered','created','architected'
    ];
    return countMatches(text, workSignals);
}

function scoreSkillsLine(text) {
    const skillSignals = [
        'python','sql','java','javascript','typescript','go','golang','rust','c++','cpp',
        'c#','csharp','ruby','php','swift','kotlin','scala','r','matlab','perl','lua',
        'shell','bash','powershell','vba','objective-c','dart','julia',
        'aws','gcp','azure','alicloud','docker','kubernetes','k8s','terraform','ansible',
        'jenkins','gitlab ci','github actions','circleci','travis','ci/cd',
        'tensorflow','pytorch','keras','sklearn','pandas','numpy','scipy',
        'matplotlib','seaborn','xgboost','lightgbm','catboost',
        'spark','hadoop','kafka','flink','hive','presto',
        'redis','mongodb','postgresql','mysql','elasticsearch','dynamodb',
        'tableau','powerbi','looker','superset','metabase','grafana',
        'airflow','dbt','snowflake','bigquery','redshift',
        'react','vue','angular','svelte','next.js','nuxt.js',
        'html','css','sass','less','webpack','vite','babel',
        'node.js','nodejs','express','nestjs','django','flask','fastapi','spring',
        'rails','laravel','.net',
        'rest','graphql','grpc','websocket',
        'linux','unix','git','svn',
        'jira','confluence','notion','slack',
        'figma','sketch','photoshop','illustrator',
        'excel','word','powerpoint','outlook',
        'sap','salesforce','servicenow',
        'seo','sem','google analytics','ga4','mixpanel','amplitude',
        'aws certified','azure certified','gcp certified','cka','ckad','pmp',
        '编程语言','云','容器','数据库','前端','后端','移动端',
        '机器学习','深度学习','人工智能','大数据','数据仓库',
        '精通','熟练','掌握','熟悉','了解','使用过'
    ];
    return countMatches(text, skillSignals);
}

function scoreGrowthLine(text) {
    const growthSignals = [
        'leadership','manage','manager','management','director','supervise',
        'mentor','coach','train','guide',
        'promote','promoted','promotion','advance','advanced',
        'strategic','strategy','vision','mission','goal','objective','roadmap',
        'education','educational','university','college','institute','school',
        'degree','bachelor','masters','master','phd','doctorate','mba',
        'award','awards','awarded','honor','honors','scholarship',
        'patent','patents','published','publication','paper',
        'adapt','adaptable','resilient','flexible',
        '领导力','管理','带领','指挥','统筹','主管',
        '团队','部门','集体','组织',
        '晋升','提拔','升迁','升职',
        '战略','策略','规划','愿景','使命','目标',
        '教育','学历','学位','本科','硕士','博士',
        '大学','学院','学校','专业',
        '荣誉','奖项','奖励','奖学金','专利','论文',
        '适应','灵活','弹性','韧性'
    ];
    return countMatches(text, growthSignals);
}

function countTechKeywords(text) {
    const techWords = [
        'python','sql','java','javascript','typescript','go','rust','c++','c#','ruby','php',
        'swift','kotlin','scala','r','matlab','shell','bash',
        'aws','gcp','azure','docker','kubernetes','terraform','ansible',
        'jenkins','gitlab','github','ci/cd',
        'tensorflow','pytorch','keras','pandas','numpy',
        'spark','hadoop','kafka','flink',
        'redis','mongodb','postgresql','mysql','elasticsearch',
        'tableau','powerbi','looker','grafana',
        'airflow','dbt','snowflake','bigquery',
        'react','vue','angular','html','css','webpack','vite',
        'nodejs','express','django','flask','spring',
        'rest','graphql','grpc',
        'linux','git','jira','confluence',
        'figma','sketch','photoshop',
        'excel','sap','salesforce'
    ];
    return countMatches(text, techWords);
}

function countMatches(text, keywords) {
    let count = 0;
    for (const kw of keywords) {
        const regex = new RegExp('\\b' + kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
        const matches = text.match(regex);
        if (matches) count += matches.length;
    }
    return count;
}

function formatLines(lines) {
    if (lines.length === 0) return '';
    
    const paragraphs = [];
    let current = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const prev = lines[i - 1];
        
        const isBullet = line.match(/^[\-\*•·◦○●▪▫\d+\.[\s\t]/);
        const prevIsBullet = prev && prev.match(/^[\-\*•·◦○●▪▫\d+\.[\s\t]/);
        
        // Start new paragraph if line looks like a new entry (not bullet continuation)
        if (current.length > 0 && !isBullet && !prevIsBullet && 
            (line.match(/^[A-Z]/) || line.match(/^\d/) || line.length > prev.length * 2)) {
            paragraphs.push(current.join('\n'));
            current = [];
        }
        
        current.push(line);
    }
    
    if (current.length > 0) paragraphs.push(current.join('\n'));
    
    return paragraphs.join('\n\n');
}

// ===== Job Matching (Real Boss Zhipin API) =====

const API_BASE = window.location.origin;

async function findMatchingJobs() {
    if (!els.jobMatchCard) return;
    
    els.jobMatchCard.style.display = 'block';
    els.jobMatchLoading.style.display = 'block';
    els.jobMatchError.style.display = 'none';
    if (els.jobMatchConfig) els.jobMatchConfig.style.display = 'none';
    els.jobList.innerHTML = '';
    
    els.jobMatchCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    try {
        // 1. Check if cookie is configured
        const statusResp = await fetch(`${API_BASE}/api/config/status`);
        const status = await statusResp.json();
        
        if (!status.cookie_configured) {
            els.jobMatchLoading.style.display = 'none';
            els.jobMatchConfig.style.display = 'block';
            return;
        }
        
        // 2. Build user profile from CV
        const keywords = state.recommendations.map(r => r.title);
        const userSkills = extractUserSkills((state.cv.work + ' ' + state.cv.skills).toLowerCase());
        const userProfile = {
            skills: userSkills,
            experience: state.cv.work,
            city: '',
            industry: ''
        };
        
        // 3. Call backend to search real jobs
        const matchResp = await fetch(`${API_BASE}/api/jobs/match`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords, userProfile })
        });
        
        const data = await matchResp.json();
        
        if (data.error === 'NO_COOKIE') {
            els.jobMatchLoading.style.display = 'none';
            els.jobMatchConfig.style.display = 'block';
            return;
        }
        
        if (data.error) {
            throw new Error(data.message || data.error);
        }
        
        if (!data.recommendations || data.recommendations.length === 0) {
            els.jobMatchLoading.style.display = 'none';
            els.jobList.innerHTML = `
                <div style="text-align:center; padding:40px; color:#64748b;">
                    <div style="font-size:48px; margin-bottom:16px;">🔍</div>
                    <p>未找到匹配岗位，Cookie 可能已过期</p>
                    <button class="btn btn-secondary" onclick="els.jobMatchConfig.style.display='block'; this.parentElement.style.display='none';" style="margin-top:16px;">重新配置 Cookie</button>
                </div>
            `;
            return;
        }
        
        els.jobMatchLoading.style.display = 'none';
        renderJobMatches(data.recommendations);
        
    } catch (err) {
        console.error('Job matching error:', err);
        els.jobMatchLoading.style.display = 'none';
        els.jobMatchError.style.display = 'block';
        els.jobMatchError.innerHTML = `
            <strong>搜索失败</strong><br>
            ${err.message}<br>
            <small>请检查网络连接，或尝试重新配置 Cookie</small>
        `;
    }
}

function renderJobMatches(jobs) {
    if (!els.jobList) return;
    
    els.jobList.innerHTML = jobs.map((job, idx) => {
        const matchColor = job.matchScore >= 80 ? '#10b981' : job.matchScore >= 60 ? '#f59e0b' : '#64748b';
        const matchBg = job.matchScore >= 80 ? 'rgba(16,185,129,0.1)' : job.matchScore >= 60 ? 'rgba(245,158,11,0.1)' : 'rgba(100,116,139,0.1)';
        
        const skillsHtml = (job.skills || []).slice(0, 5).map(s => 
            `<span class="skill-tag">${s}</span>`
        ).join('');
        
        const welfareHtml = (job.welfare || []).slice(0, 3).map(w => 
            `<span class="welfare-tag">${w}</span>`
        ).join('');
        
        // Use the REAL job detail link with jobId
        const detailLink = job.detailLink || `https://www.zhipin.com/job_detail/${job.jobId}.html`;
        
        return `
            <div class="job-card" style="animation-delay: ${idx * 100}ms">
                <div class="job-card-header">
                    <div class="job-match-badge" style="background:${matchBg}; color:${matchColor}">
                        <span class="match-score">${job.matchScore}</span>
                        <span class="match-label">匹配度</span>
                    </div>
                    <div class="job-title-section">
                        <h4 class="job-name">${job.jobName}</h4>
                        <div class="job-meta">
                            <span class="job-salary">${job.salary}</span>
                            <span class="job-location">📍 ${job.city}${job.district ? ' · ' + job.district : ''}${job.businessDistrict ? ' · ' + job.businessDistrict : ''}</span>
                            <span class="job-exp">${job.experience} · ${job.degree}</span>
                        </div>
                    </div>
                </div>
                
                <div class="job-company">
                    <span class="company-name">🏢 ${job.company}</span>
                    <span class="company-info">${job.companyScale || ''} ${job.companyStage ? '· ' + job.companyStage : ''} ${job.industry ? '· ' + job.industry : ''}</span>
                </div>
                
                <div class="job-skills">
                    ${skillsHtml}
                </div>
                
                ${job.matchReasons && job.matchReasons.length > 0 ? `
                <div class="job-reasons">
                    <span class="reasons-label">💡 匹配理由：</span>
                    ${job.matchReasons.map(r => `<span class="reason-tag">${r}</span>`).join('')}
                </div>
                ` : ''}
                
                <div class="job-welfare">
                    ${welfareHtml}
                </div>
                
                <div class="job-boss">
                    <span>👤 ${job.bossName || 'HR'} ${job.bossTitle ? '(' + job.bossTitle + ')' : ''}</span>
                </div>
                
                <div class="job-actions">
                    <a href="${detailLink}" target="_blank" class="btn btn-primary btn-apply">
                        <span>📨 一键投递</span>
                        <small>直达 Boss直聘 岗位详情页</small>
                    </a>
                </div>
            </div>
        `;
    }).join('');
}

async function saveBossCookie() {
    const cookie = els.bossCookieInput.value.trim();
    if (!cookie) {
        alert('请输入 Cookie');
        return;
    }
    
    els.btnSaveCookie.innerHTML = '<span class="spinner" style="width:16px;height:16px;border-width:2px;display:inline-block;vertical-align:middle;"></span> 保存中...';
    
    try {
        const resp = await fetch(`${API_BASE}/api/config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cookie })
        });
        
        const data = await resp.json();
        if (data.success) {
            els.jobMatchConfig.style.display = 'none';
            findMatchingJobs();
        } else {
            alert('保存失败: ' + (data.error || '未知错误'));
        }
    } catch (err) {
        alert('保存失败: ' + err.message);
    } finally {
        els.btnSaveCookie.innerHTML = '💾 保存并搜索岗位';
    }
}

// Start
init();
