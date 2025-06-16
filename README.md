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
- **Node.js 16.0+** (for frontend)
- **npm/yarn** (for frontend)

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

### Frontend Development
The frontend is built using modern web technologies to provide a responsive and user-friendly interface:

- **React 18+**: Component-based UI development
- **Vite**: Fast development server and optimized builds
- **Tailwind CSS**: Utility-first styling framework
- **TypeScript**: Type-safe development

The frontend communicates with the FastAPI backend to:
- Submit project descriptions
- Receive technology stack recommendations
- Display categorized technology suggestions
- Handle user interactions and form submissions

### Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Node.js 16.0 or higher (for frontend)
- npm or yarn (for frontend)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd stack-own
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   cd recommender
   python recommender.py
   cd ..
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install  # or yarn install
   npm run dev  # or yarn dev
   ```

4. **Run the Backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
