#api endpoints i want to get project details, then 
from typing import Annotated, Optional, List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import spacy
from pathlib import Path

nlp_model = None #global model variable

class Project(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    project_complexity: str
    recommendations: List["Recommendation"] = Relationship(back_populates="project")
    
class Recommendation(SQLModel, table= True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    tech_stack_json : str
    reason_json : str
    project: Optional[Project] = Relationship(back_populates="recommendations")
    
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
    
    "dashboard": {
        "simple": {
            "frontend": ["Chart.js", "HTML/CSS", "Bootstrap"],
            "backend": ["Python Flask", "Express.js"],
            "database": ["SQLite", "CSV files"],
            "deployment": ["Heroku", "Netlify"],
            "tools": ["Excel", "Google Sheets"]
        },
        "medium": {
            "frontend": ["React", "D3.js", "Chart.js", "Material-UI"],
            "backend": ["Python FastAPI", "Node.js", "REST APIs"],
            "database": ["PostgreSQL", "InfluxDB"],
            "deployment": ["Docker", "AWS", "Grafana"],
            "tools": ["Tableau", "Power BI", "Jupyter"]
        },
        "complex": {
            "frontend": ["React", "D3.js", "Observable", "Custom Visualizations"],
            "backend": ["Python FastAPI", "Apache Kafka", "Real-time APIs"],
            "database": ["ClickHouse", "Apache Spark", "Data Lake"],
            "deployment": ["Kubernetes", "AWS Data Pipeline", "Streaming"],
            "tools": ["Apache Airflow", "Elastic Stack", "Custom Analytics"]
        }
    },
    
    "mobile_app": {
        "simple": {
            "frontend": ["React Native", "Flutter"],
            "backend": ["Firebase", "Node.js"],
            "database": ["Firebase Firestore", "SQLite"],
            "deployment": ["App Store", "Google Play"],
            "tools": ["Expo", "Android Studio"]
        },
        "medium": {
            "frontend": ["React Native", "Flutter", "Native Navigation"],
            "backend": ["Node.js", "Python FastAPI", "REST APIs"],
            "database": ["PostgreSQL", "MongoDB", "Offline Storage"],
            "deployment": ["CI/CD", "TestFlight", "Firebase Distribution"],
            "tools": ["Redux", "Push Notifications", "Analytics"]
        },
        "complex": {
            "frontend": ["Native iOS/Android", "React Native", "Offline-First"],
            "backend": ["Microservices", "GraphQL", "Real-time APIs"],
            "database": ["Multi-region DB", "Caching", "Sync Solutions"],
            "deployment": ["Enterprise Distribution", "A/B Testing"],
            "tools": ["Performance Monitoring", "Crash Analytics", "Security"]
        }
    }
}

    
    
sqlite_file_name = "database.db"
sqlite_url =  f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    global nlp_model
    create_db_and_tables()
    print("Database and tables created!")

    try:
        model_path= "./recommender/model_output"
        nlp_model = spacy.load(model_path)
        print("Model loaded successfully!")
        print(f"Labels: {list(nlp_model.get_pipe('textcat_multilabel').labels)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        nlp_model = None

def get_model():
    if nlp_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return nlp_model

def generate_techstack_recommendations(classifications, complexity):
    project_type = max(classifications, key=classifications.get)
    tech_stack = TECH_STACK_MAP[project_type][complexity]
    template = """
    Your project can be classified as {classifications} with this {complexity} complexity, so recommended tech stack is:
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

    
@app.post("/projects/")
def create_project(project: Project, session: SessionDep):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@app.post("/recommendations")
def create_recommendations(project_id: int, session: SessionDep):
    model = get_model()
    project = session.get(Project, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    doc = model(project.description)
    classifications = doc.cats
    
    recommendation_text = generate_techstack_recommendations(classifications, project.project_complexity)
    
    return {
        "project_id": project_id,
        "classifications": classifications,
        "description": project.description,
        "recommendation": recommendation_text
    }
    

