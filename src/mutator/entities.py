from datetime import date, timedelta
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class User:
    id: int
    name: str

    @staticmethod
    def from_dict(row: dict[str, str]):
        return User(row["id"], row["name"])


@dataclass(slots=True, frozen=True)
class Activity:
    user: User
    tracked: int = 0

    @property
    def duration(self):
        return str(timedelta(seconds=self.tracked))


@dataclass(slots=True, frozen=True)
class Project:
    id: int
    name: str
    activities: list[Activity] = field(default_factory=list)

    @staticmethod
    def from_dict(row: dict):
        return Project(row["id"], row["name"])


@dataclass(slots=True, frozen=True)
class Organization:
    id: int
    name: str
    status: str
    projects: list[Project] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class Credentials:
    email: str
    password: str
    app_token: str


@dataclass(slots=True, frozen=True)
class Period:
    begin: date
    end: date

    def __str__(self):
        begin = self.begin.isoformat()
        end = self.end.isoformat()
        if begin == end:
            return begin
        return f"{begin}/{end}"
