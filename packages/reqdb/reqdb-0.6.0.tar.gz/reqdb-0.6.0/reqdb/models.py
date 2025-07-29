from pydantic import BaseModel, Field


class Base(BaseModel):
    id: int | None = None

class Configuration(BaseModel):
    key: str | None = None
    value: str | None = None

class TopicIdOnly(Base):
    id: int

class TagIdOnly(Base):
    id: int

class CatalogueIdOnly(Base):
    id: int

class RequirementIdOnly(Base):
    id: int

class ExtraEntry(Base):
    content: str = Field(min_length=1)
    extraTypeId: int
    requirementId: int


class ExtraType(Base):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    extraType: int = Field(ge=1, le=3)
    children: list[ExtraEntry] = []


class Requirement(Base):
    key: str = Field(max_length=20)
    title: str = Field(max_length=200)
    description: str
    visible: bool = Field(default=True)
    parentId: int
    tags: list["TagIdOnly"] | None = None


class Tag(Base):
    name: str = Field(min_length=1, max_length=50)
    requirements: list["RequirementIdOnly"] = []
    catalogues: list["CatalogueIdOnly"] = []


class Topic(Base):
    key: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    parentId: int | None = None


class Catalogue(Base):
    title: str  = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    topics: list["TopicIdOnly"] | None = None
    tags: list["TagIdOnly"] | None = None


class Comment(Base):
    comment: str  = Field(min_length=1)
    completed: bool | None = None
    requirementId: int
    parentId: int


