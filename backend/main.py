#api endpoints i want to get project details, then 
from typing import Annotated, Optional, List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import spacy
from pathlib import Path

nlp_model = None #global model variable

class Project(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    project_type: str
    curr_tech_stack: str
    project_complexity: str
    
    recommendations: List["Recommendation"] = Relationship(back_populates="project")
    
class Recommendation(SQLModel, table= True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    tech_stack_json : str
    reason_json : str
    project: Optional[Project] = Relationship(back_populates="recommendations")
    
    
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

    
@app.post("/projects/")
def create_project(project: Project, session: SessionDep):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/projects/")
def read_porjects(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Project]:
    projects = session.exec(select(Project).offset(offset).limit(limit)).all()
    return projects

@app.post("/recommendations")
def create_recommendations(project_id: int, session: SessionDep):
    model = get_model()
    project = session.get(Project, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    doc = model(project.description)
    classifications = doc.cats
    
    return {
        "project_id": project_id,
        "classifications": classifications,
        "description": project.description
    }
    

