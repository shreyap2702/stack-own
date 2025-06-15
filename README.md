## stack-own
A simple system that analyzes project descriptions and recommends appropriate technology stacks.

### What This Project Is About
The tech stack recommender is a web tool that helps you pick the right technologies for your project. Just describe what you're building in plain English, and it'll suggest which programming languages, frameworks, and tools would work best for you.

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


### Requirements
- **Python 3.8+**
- **FastAPI**
- **SQLModel**
- **spaCy**
- **Uvicorn**

### Text Classification using Spacy

#### Model Architecture
```python
nlp = spacy.blank("en")
nlp.add_pipe("textcat_multilabel", last=True)
textcat = nlp.get_pipe("textcat_multilabel")
```



#### Training Process
1. **Data Preparation**: 20 examples with multi-label annotations
2. **Model Training**: 20 iterations with shuffled data
3. **Model Persistence**: Saved to `./recommender/model_output`
4. **Inference**: Real-time classification during API calls

#### Example Classification Output
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
### Mapping and Template Function for Recommendation Generation

The tech stack is determined using the project type and its complexity.
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
    # Similar structure is used further
}
```

### Workflow how the project works

1. **Project Submission**: User submits project description and complexity
2. **Text Classification**: spaCy model analyzes and classifies the project
3. **Tech Stack Mapping**: System maps classification + complexity to recommendations
4. **Response Generation**: Recommendations are generated with tech-stack mappings
5. **Storage**: Project and recommendations are saved to database

### Setup

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
