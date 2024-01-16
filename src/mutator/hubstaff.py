import typing as t
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlencode
import aiohttp

from .consts import APP_TOKEN, AUTH_EMAIL, AUTH_PASSWORD, API_BASE_URL

@dataclass(slots=True, frozen=True)
class Organization:
    id: int
    name: str
    status: str

@dataclass(slots=True, frozen=True)
class Task:
    id: int
    name: str
    status: str

@dataclass(slots=True, frozen=True)
class Project:
    id: int
    name: str
    status: str
    tasks: list[Task] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class Credentials:
    email: str
    password: str
    app_token: str

class ApiError(Exception):
    pass


class HubstaffApi:
    def __init__(self, base_url: str, credentials: Credentials) -> None:
        self.base_url = base_url
        self.credentials = credentials 
        self._session = None
        self._auth_token = None

    async def get_projects(self, organization_name: str) -> t.Generator[Project, None, None]:
        async with self._get_session() as session:
            while True:
                page_start_id = 0
                query = { "page_start_id": page_start_id}
                url = self._build_url("companies", query)
                async with session.get(url) as response:
                    results = await response.json()
                    print(results)
                    for row in results["organizations"]:
                        if row["name"] == organization_name:

                    try:
                        page_start_id = results["pagination"]["next_page_start_id"]
                    except KeyError:
                        break


    @asynccontextmanager 
    async def _get_session(self):
        if self._auth_token is None:
            self._auth_token = await self._get_auth_token()
        headers = {
            "AuthToken": self._auth_token
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            yield session
 
    async def _get_auth_token(self) -> str:
        data = {
            "email": self.credentials.email,
            "password": self.credentials.password,
        }
        url = self._build_url("user/authentication")
        print(url)
        print(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                result = await response.json()
                return result["auth_token"]

    def _build_url(self, url: str, params: dict[str, str]|None = None) -> str:
        query = { "app_token": self.credentials.app_token }
        if params is not None:
            query.update(query)
        query_str = urlencode(query)
        sep = "&" if "?" in url else "?"
        return urljoin(self.base_url, url) + sep + query_str


def create_default_api() -> HubstaffApi:
    credentials = Credentials(AUTH_EMAIL, AUTH_PASSWORD, APP_TOKEN)
    return HubstaffApi(API_BASE_URL, credentials)
