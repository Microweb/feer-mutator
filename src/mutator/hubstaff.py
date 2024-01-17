import typing as t
from contextlib import asynccontextmanager
from urllib.parse import urljoin, urlencode
from collections import defaultdict
import logging

import aiohttp

from .consts import APP_TOKEN, AUTH_EMAIL, AUTH_PASSWORD, API_BASE_URL
from .entities import Credentials, Organization, Period, User, Project, Activity

logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class NotFoundEntity(ApiError):
    def __init__(self, entity: str, value: int | str) -> None:
        super().__init__(f"Not found {entity}: {value}")


class HubstaffApi:
    def __init__(self, base_url: str, credentials: Credentials) -> None:
        self.base_url = base_url
        self.credentials = credentials
        self._session = None
        self._auth_token = None

    async def get_organization_activities(
        self, organization_name: str, period: Period
    ) -> Organization:
        organization = await self._get_organization_by_name(organization_name)
        async for project in self._get_activities(organization, period):
            organization.projects.append(project)
        return organization

    async def _get_organization_by_name(self, name: str) -> Organization:
        logger.debug("Search organization: %s", name)
        async for result in self._paginate("companies"):
            for row in result["organizations"]:
                if row["name"] == name:
                    return Organization(row["id"], row["name"], row["status"])
        raise NotFoundEntity(Organization.__name__, name)

    async def _get_activities(
        self, organization: Organization, period: Period
    ) -> t.AsyncGenerator[Project, None]:
        logger.debug("Search activities for organization: %s", organization.name)
        base_url = f"companies/{organization.id}/activity/day"
        query = {
            "date[start]": period.begin.isoformat(),
        }
        headers = {
            "DateStop": period.end.isoformat(),
            "Include": "users,projects",
        }
        users = {}
        projects = {}
        tracked = defaultdict(int)
        async for results in self._paginate(base_url, query, headers):
        # prepare easy search
            for row in results["users"]:
                users[row["id"]] = User.from_dict(row) 
            for row in results["projects"]:
                projects[row["id"]] = Project.from_dict(row) 


            # count tracked time
            activities = results["daily_activities"]
            logger.debug(
                "Found %s activities for organization: %s",
                len(activities),
                organization.name,
            )
            for row in activities:
                pid = row["project_id"]
                uid = row["user_id"]
                tracked[(pid, uid)] += row["tracked"]

        for (pid, uid), time in tracked.items():
            user = users[uid]
            project = projects[pid]
            project.activities.append(Activity(user, time))

        for project in sorted(projects.values(), key=lambda u: u.id, reverse=True):
            if project.activities:
                yield project

    async def _paginate(self, url: str, query: dict|None=None, headers: dict|None=None):
        query = {} if query is None else query
        headers = {} if headers is None else headers
        next_id = None
        while True:
            if next_id is not None:
                headers["PageStartId"] = str(next_id)
            url = self._build_url(url, query)
            async with self._get_session() as session:
                async with session.get(url, headers=headers) as response:
                    result = await response.json()
                    yield result
                    try:
                        next_id = result["pagination"]["next_page_start_id"]
                    except KeyError:
                        break

    @asynccontextmanager
    async def _get_session(self):
        if self._auth_token is None:
            self._auth_token = await self._get_auth_token()
        headers = {"AuthToken": self._auth_token}
        async with aiohttp.ClientSession(headers=headers) as session:
            yield session

    async def _get_auth_token(self) -> str:
        logger.debug("Authenticate user: %s", self.credentials.email)
        data = {
            "email": self.credentials.email,
            "password": self.credentials.password,
        }
        url = self._build_url("user/authentication")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                result = await response.json()
                return result["auth_token"]

    def _build_url(self, url: str, query: dict[str, str] | None = None) -> str:
        query = {} if query is None else query
        query.update({"app_token": self.credentials.app_token})
        query_str = urlencode(query)
        sep = "&" if "?" in url else "?"
        return urljoin(self.base_url, url) + sep + query_str


def create_hubstaff_api() -> HubstaffApi:
    credentials = Credentials(AUTH_EMAIL, AUTH_PASSWORD, APP_TOKEN)
    return HubstaffApi(API_BASE_URL, credentials)
