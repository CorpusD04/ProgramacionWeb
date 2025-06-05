from pydantic import BaseModel
from typing import Optional

#  Definir esquema para usuarios
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str  #  Agregar contraseña para registro

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

#  Esquema de cursos
class CourseBase(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]
    url: str
    provider: Optional[str]
    image: Optional[str]

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True

#  Esquema de progreso de usuario en cursos
class UserCourseBase(BaseModel):
    course_id: int

class UserCourse(UserCourseBase):
    id: int
    completed: bool
    course: Course

    class Config:
        orm_mode = True
