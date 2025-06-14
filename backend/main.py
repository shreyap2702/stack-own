#api endpoints i want to get project details, then 
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Project(SQLModel, Table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    project_type: str
    curr_tech_stack: str
    project_complexity: str
    
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
    create_db_and_tables()
    
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
def create_recommendations():
    return

