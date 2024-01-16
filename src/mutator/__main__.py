import asyncio

from .consts import ORGANIZATION_NAME
from .hubstaff import create_default_api

async def main():
    api = create_default_api()
    async for project in api.get_projects(ORGANIZATION_NAME):
        print(project)


if __name__ == '__main__':
    asyncio.run(main())
