import asyncio

from .consts import ORGANIZATION_NAME
from .hubstaff import create_hubstaff_api
from .renders import render_cli_organization
from .time import get_period


async def main():
    api = create_hubstaff_api()
    yesterday = get_period()
    organization = await api.get_organization_activities(ORGANIZATION_NAME, yesterday)

    result = render_cli_organization(organization, yesterday)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
