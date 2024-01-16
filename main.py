import aiohttp
import asyncio
from datetime import datetime, timedelta


EMAIL = "p.smialkowski@gmail.com"
PASSWORD = "EGRT58MG"
APP_TOKEN = "K1S496Q79PNOGFGV"

API_URL = "https://mutator.reef.pl"

async def main():
    async with aiohttp.ClientSession() as session:
        payload = {
            "email": EMAIL,
            "password": PASSWORD,
        }
        url = API_URL +  "/v316/user/authentication?app_token=" + APP_TOKEN
        print(url)
        print(payload)
        return
        async with session.post(url, data=payload) as response:
            data = await response.json()
            auth_token = data["auth_token"]
        url = API_URL +  "/v316/companies?app_token=" + APP_TOKEN 
        headers = {
            "AuthToken": auth_token
        }
        print(url)
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            print(data)
            oid = data["organizations"][0]["id"]
    
        now = datetime.now()
        yesterday = now + timedelta(days=-1)
        start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        stop = start+timedelta(days=2)
        start, stop = start.isoformat(), stop.isoformat()

        print("PROJECTS") 
        url = API_URL + f"/v316/companies/{oid}/tasks?app_token=" + APP_TOKEN
        print(url)
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            for project in data["projects"]:
                print(project)

        print("TASKS")
        url = API_URL + f"/v316/companies/{oid}/task?app_token=" + APP_TOKEN
        print(url)
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            for task in data["tasks"]:
                print(task)

        headers["DateStop"] = stop
        url = API_URL + f"/v316/companies/{oid}/activity/day?date[start]={start}&app_token=" + APP_TOKEN
        print(url)
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            print(data)



if __name__ == '__main__':
    asyncio.run(main())
