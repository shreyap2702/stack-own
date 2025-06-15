# 🚀 Tech Stack Recommender

An intelligent system that analyzes project descriptions and recommends appropriate technology stacks based on project type and complexity using machine learning and rule-based approaches.

## 📋 What This Project Is About

The Tech Stack Recommender is a **FastAPI-based web service** that helps developers and teams choose the right technology stack for their projects. It combines **Natural Language Processing (NLP)** with **intelligent mapping algorithms** to provide personalized, context-aware technology recommendations.

### Key Features:
- 🤖 **AI-Powered Classification**: Uses spaCy for multi-label text classification
- 🎯 **Complexity-Aware Recommendations**: Scales tech stacks from simple to complex
- 🔄 **Hybrid Approach**: Combines ML classification with rule-based pattern matching
- 📊 **Comprehensive Coverage**: Frontend, Backend, Database, Deployment, and Tools
- 🚀 **RESTful API**: Easy integration with any frontend application
- 💾 **Persistent Storage**: SQLite database for project and recommendation tracking

## 🏗️ Architecture and Requirements Explanation

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   SQLite DB     │
│   (Any Client)  │◄──►│   Backend       │◄──►│   (Projects &   │
│                 │    │                 │    │   Recommendations)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   spaCy ML      │
                       │   Model         │
                       │   (TextCat)     │
                       └─────────────────┘
```

### Technology Stack
- **Backend Framework**: FastAPI (Python)
- **Database ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: SQLite (development) / PostgreSQL (production)
- **NLP Library**: spaCy with TextCat classifier
- **API Server**: Uvicorn (ASGI)
- **Machine Learning**: Custom-trained spaCy model

### Requirements
- **Python 3.8+**: For modern type hints and async support
- **FastAPI**: High-performance web framework
- **SQLModel**: Type-safe database operations
- **spaCy**: Natural language processing
- **Uvicorn**: ASGI server for production deployment

## 🔧 FastAPI Backend

### API Endpoints

#### 1. Create Project
```http
POST /projects/
Content-Type: application/json

{
  "description": "Build a real-time dashboard for ecommerce analytics",
  "project_complexity": "medium"
}
```

#### 2. Generate Recommendations
```http
POST /recommendations?project_id=1
```

### Database Models

```python
class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    project_complexity: str
    recommendations: List["Recommendation"] = Relationship(back_populates="project")

class Recommendation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    tech_stack_json: str
    reason_json: str
    project: Optional[Project] = Relationship(back_populates="recommendations")
```

### Key FastAPI Features Used
- **Dependency Injection**: Automatic session management
- **Type Validation**: Pydantic models for request/response validation
- **Auto Documentation**: Swagger UI at `/docs`
- **Error Handling**: HTTPException for proper error responses
- **Startup Events**: Model loading and database initialization

## 🤖 Text Classification using spaCy

### Model Architecture
```python
nlp = spacy.blank("en")
nlp.add_pipe("textcat_multilabel", last=True)
textcat = nlp.get_pipe("textcat_multilabel")
```

### Classification Categories
- **`dashboard`**: Analytics panels, admin interfaces, data visualization
- **`realtime_system`**: Live updates, streaming data, instant feedback
- **`web_app`**: Browser-based applications, responsive web apps
- **`ecommerce`**: Online stores, shopping platforms
- **`ml_task`**: Machine learning, AI, data science projects
- **`portfolio`**: Personal websites, showcase projects
- **`mobile_app`**: iOS/Android applications

### Training Process
1. **Data Preparation**: 10 hand-curated examples with multi-label annotations
2. **Model Training**: 20 iterations with shuffled data
3. **Model Persistence**: Saved to `./recommender/model_output`
4. **Inference**: Real-time classification during API calls

### Example Classification Output
```python
{
    "dashboard": 0.85,      # 85% confidence
    "web_app": 0.92,        # 92% confidence
    "realtime_system": 0.78, # 78% confidence
    "ecommerce": 0.45,      # 45% confidence
    "ml_task": 0.12,        # 12% confidence
    "portfolio": 0.08,      # 8% confidence
    "mobile_app": 0.23      # 23% confidence
}
```

## 🗺️ Mapping and Template Function for Recommendation Generation

### Theoretical Foundation

The mapping and template system is built on several key theoretical concepts in software engineering and recommendation systems:

#### 1. **Technology Maturity Model**
The system implements a **three-tier complexity model** inspired by software development maturity frameworks:
- **Simple (Beginner/MVP)**: Focus on rapid prototyping and learning
- **Medium (Production)**: Balance between complexity and maintainability  
- **Complex (Enterprise)**: Scalability, reliability, and advanced features

#### 2. **Technology Stack Evolution Theory**
Based on the principle that technology choices should evolve with project requirements:
- **Frontend Evolution**: HTML/CSS → React → Next.js with TypeScript
- **Backend Evolution**: Flask → FastAPI → Microservices
- **Database Evolution**: SQLite → PostgreSQL → Distributed databases
- **Deployment Evolution**: Heroku → Docker → Kubernetes

#### 3. **Multi-dimensional Recommendation Framework**
The system considers five critical dimensions of modern software development:
- **Frontend**: User interface and client-side technologies
- **Backend**: Server-side logic and API design
- **Database**: Data persistence and management
- **Deployment**: Infrastructure and hosting solutions
- **Tools**: Development, testing, and monitoring utilities

### Tech Stack Hierarchy Architecture

The mapping system uses a **nested hierarchical structure** that enables precise, context-aware recommendations:

```python
TECH_STACK_MAP = {
    "web_app": {
        "simple": {
            "frontend": ["HTML/CSS/JavaScript", "Bootstrap"],
            "backend": ["Node.js Express", "Python Flask"],
            "database": ["SQLite", "MySQL"],
            "deployment": ["Netlify", "Heroku"],
            "tools": ["VS Code", "Git"]
        },
        "medium": {
            "frontend": ["React", "Vue.js", "Tailwind CSS"],
            "backend": ["Node.js Express", "Python FastAPI", "REST APIs"],
            "database": ["PostgreSQL", "MongoDB"],
            "deployment": ["Docker", "AWS EC2", "Nginx"],
            "tools": ["Webpack", "ESLint", "Postman"]
        },
        "complex": {
            "frontend": ["React", "TypeScript", "Next.js", "Redux"],
            "backend": ["Node.js", "Python FastAPI", "Microservices", "GraphQL"],
            "database": ["PostgreSQL", "Redis", "Elasticsearch"],
            "deployment": ["Kubernetes", "AWS/GCP", "CI/CD Pipeline"],
            "tools": ["Docker", "Jest", "Monitoring Tools"]
        }
    },
    # Similar structure for "dashboard" and "mobile_app"
}
```

#### **Hierarchical Design Principles**

1. **Project Type Classification** (First Level)
   - **`web_app`**: Browser-based applications, SPAs, web services
   - **`dashboard`**: Data visualization, analytics, admin panels
   - **`mobile_app`**: iOS/Android applications, cross-platform apps

2. **Complexity Scaling** (Second Level)
   - **`simple`**: Minimal viable products, learning projects, prototypes
   - **`medium`**: Production applications, small to medium scale
   - **`complex`**: Enterprise applications, high-scale systems

3. **Technology Categories** (Third Level)
   - **`frontend`**: User interface frameworks and libraries
   - **`backend`**: Server-side technologies and APIs
   - **`database`**: Data storage and management solutions
   - **`deployment`**: Infrastructure and hosting platforms
   - **`tools`**: Development, testing, and operational tools

### Recommendation Generation Algorithm

The recommendation system implements a **multi-stage decision algorithm**:

#### **Stage 1: Classification Confidence Analysis**
```python
def analyze_classifications(classifications):
    """
    Analyzes classification confidence scores and determines
    the primary project type with fallback mechanisms.
    """
    # Get the highest confidence classification
    primary_type = max(classifications, key=classifications.get)
    confidence_score = classifications[primary_type]
    
    # Apply confidence threshold (e.g., 0.5)
    if confidence_score < 0.5:
        # Fallback to rule-based classification
        return apply_rule_based_classification(text)
    
    return primary_type
```

#### **Stage 2: Complexity-Aware Mapping**
```python
def map_complexity_to_tech_stack(project_type, complexity):
    """
    Maps project type and complexity to appropriate technology stack
    using the hierarchical TECH_STACK_MAP structure.
    """
    if project_type not in TECH_STACK_MAP:
        raise ValueError(f"Unknown project type: {project_type}")
    
    if complexity not in TECH_STACK_MAP[project_type]:
        # Default to medium complexity if specified complexity not found
        complexity = "medium"
    
    return TECH_STACK_MAP[project_type][complexity]
```

#### **Stage 3: Template-Based Response Generation**
```python
def generate_techstack_recommendations(classifications, complexity):
    """
    Generates human-readable technology recommendations using
    a template-based approach with dynamic content insertion.
    """
    project_type = max(classifications, key=classifications.get)
    tech_stack = TECH_STACK_MAP[project_type][complexity]
    
    # Template with placeholders for dynamic content
    template = """
    Your project can be classified as {classifications} with this {complexity} complexity, 
    so recommended tech stack is:
    • Frontend: {frontend}
    • Backend: {backend}
    • Database: {database}
    • Deployment: {deployment}
    • Tools: {tools}
    """
    
    return template.format(
        classifications=project_type.replace("_", " ").title(),
        complexity=complexity,
        frontend=", ".join(tech_stack["frontend"]),
        backend=", ".join(tech_stack["backend"]),
        database=", ".join(tech_stack["database"]),
        deployment=", ".join(tech_stack["deployment"]),
        tools=", ".join(tech_stack["tools"])
    )
```

### Template System Design Theory

#### **1. Separation of Concerns**
The template system separates:
- **Content Logic**: Technology mapping and selection
- **Presentation Logic**: Formatting and structure
- **Data Binding**: Dynamic content insertion

#### **2. Template Design Patterns**

**A. Placeholder Pattern**
```python
template = "Your project is {project_type} with {complexity} complexity"
```
- Uses `{variable}` placeholders for dynamic content
- Enables flexible content insertion
- Maintains template reusability

**B. Conditional Pattern**
```python
template = """
Frontend: {frontend}
{backend_section}
Database: {database}
"""
```
- Supports conditional content blocks
- Allows for context-specific recommendations
- Reduces template complexity

**C. Iterative Pattern**
```python
template = """
Technologies:
{tech_list}
"""
```
- Handles variable-length technology lists
- Maintains consistent formatting
- Supports dynamic content expansion

#### **3. Template Optimization Strategies**

**A. Caching Mechanism**
```python
class TemplateCache:
    def __init__(self):
        self.cached_templates = {}
    
    def get_template(self, template_type):
        if template_type not in self.cached_templates:
            self.cached_templates[template_type] = self.load_template(template_type)
        return self.cached_templates[template_type]
```

**B. Lazy Evaluation**
```python
def format_tech_stack(tech_stack, complexity):
    """
    Lazy evaluation of technology stack formatting
    to improve performance for large stacks.
    """
    return {
        "frontend": lambda: ", ".join(tech_stack["frontend"]),
        "backend": lambda: ", ".join(tech_stack["backend"]),
        # ... other categories
    }
```

### Complexity Level Theory

#### **Simple Complexity (Beginner/MVP)**
**Philosophy**: "Get it working first, optimize later"
- **Focus**: Rapid prototyping and learning
- **Constraints**: Limited resources, tight deadlines
- **Technologies**: Beginner-friendly, well-documented
- **Trade-offs**: Simplicity over scalability

**Technology Selection Criteria**:
- Extensive documentation and community support
- Low learning curve
- Quick setup and deployment
- Cost-effective hosting options

#### **Medium Complexity (Production)**
**Philosophy**: "Balance between development speed and maintainability"
- **Focus**: Production-ready applications
- **Constraints**: Team collaboration, code maintainability
- **Technologies**: Modern frameworks with good practices
- **Trade-offs**: Development speed vs. scalability

**Technology Selection Criteria**:
- Industry-standard frameworks
- Good testing and debugging tools
- Scalable architecture patterns
- Production deployment capabilities

#### **Complex Complexity (Enterprise)**
**Philosophy**: "Build for scale, reliability, and long-term success"
- **Focus**: High-performance, scalable systems
- **Constraints**: High availability, security, compliance
- **Technologies**: Enterprise-grade, battle-tested solutions
- **Trade-offs**: Complexity vs. performance

**Technology Selection Criteria**:
- Microservices architecture support
- Advanced monitoring and observability
- High availability and fault tolerance
- Security and compliance features

### Mapping Algorithm Complexity Analysis

#### **Time Complexity**
- **Classification Lookup**: O(1) - Direct dictionary access
- **Complexity Mapping**: O(1) - Nested dictionary access
- **Template Generation**: O(n) - Where n is the number of technology categories
- **Overall Algorithm**: O(n) - Linear time complexity

#### **Space Complexity**
- **TECH_STACK_MAP**: O(p × c × t) - Where p=project types, c=complexity levels, t=technology categories
- **Template Storage**: O(1) - Fixed template size
- **Runtime Memory**: O(1) - Constant space for processing

#### **Scalability Considerations**
- **Horizontal Scaling**: Stateless algorithm enables easy scaling
- **Caching**: Template and mapping results can be cached
- **Database Integration**: Can be extended to use database-stored mappings
- **API Versioning**: Supports multiple mapping versions for different use cases

### Future Enhancement Possibilities

#### **1. Dynamic Mapping Updates**
```python
def update_tech_stack_mapping(project_type, complexity, new_technologies):
    """
    Allows runtime updates to technology mappings
    based on new trends or requirements.
    """
    TECH_STACK_MAP[project_type][complexity].update(new_technologies)
```

#### **2. Personalized Recommendations**
```python
def generate_personalized_recommendations(classifications, complexity, user_preferences):
    """
    Incorporates user preferences and past choices
    for personalized technology recommendations.
    """
    base_recommendations = get_base_recommendations(classifications, complexity)
    return apply_user_preferences(base_recommendations, user_preferences)
```

#### **3. A/B Testing Framework**
```python
def get_recommendation_variant(classifications, complexity, variant_id):
    """
    Supports A/B testing of different recommendation
    strategies and technology combinations.
    """
    return RECOMMENDATION_VARIANTS[variant_id](classifications, complexity)
```

This theoretical foundation ensures that the mapping and template system is not just functional but also scalable, maintainable, and theoretically sound for production use.

## 🎯 Overall System Overview

### Workflow
1. **Project Submission**: User submits project description and complexity
2. **Text Classification**: spaCy model analyzes and classifies the project
3. **Tech Stack Mapping**: System maps classification + complexity to recommendations
4. **Response Generation**: Human-readable recommendations are generated
5. **Storage**: Project and recommendations are saved to database

### Key Innovations
- **Multi-label Classification**: Projects can belong to multiple categories
- **Intelligent Scaling**: Tech stacks scale with project complexity
- **Explainable AI**: Clear reasoning for each recommendation
- **Hybrid Approach**: ML + rule-based for maximum reliability
- **Comprehensive Coverage**: All aspects of modern development stack

### Use Cases
- **Developer Onboarding**: New team members get appropriate tech recommendations
- **Project Planning**: Teams validate their technology choices
- **Learning Tool**: Developers discover new technologies and frameworks
- **Consulting**: Technical consultants provide data-driven recommendations

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd stack-own
   ```

2. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

3. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download spaCy Model (if needed)**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Train the Classification Model**
   ```bash
   cd recommender
   python recommender.py
   cd ..
   ```

7. **Run the Application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### API Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example Usage

#### Create a Project
```bash
curl -X POST "http://localhost:8000/projects/" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "Build a real-time dashboard for ecommerce analytics",
       "project_complexity": "medium"
     }'
```

#### Generate Recommendations
```bash
curl -X POST "http://localhost:8000/recommendations?project_id=1"
```

### Environment Variables (Optional)
```bash
export DATABASE_URL="sqlite:///database.db"
export MODEL_PATH="./recommender/model_output"
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### Troubleshooting

#### Common Issues
1. **Import Errors**: Ensure virtual environment is activated
2. **Model Loading Errors**: Check if model is trained and saved correctly
3. **Database Errors**: Ensure SQLite file has proper permissions
4. **Port Conflicts**: Change port in uvicorn command if 8000 is occupied

#### Development Tips
- Use `--reload` flag for automatic server restart during development
- Check logs for detailed error messages
- Use FastAPI's built-in debugging tools at `/docs`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section above 