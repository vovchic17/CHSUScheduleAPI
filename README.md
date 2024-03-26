<img src="https://raw.githubusercontent.com/vovchic17/static/main/src/logo.svg" alt="drawing" width="150"/>


# CHSUScheduleAPI
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Aiohttp](https://img.shields.io/badge/aiohttp-v3.9.3-2c5bb4?logo=aiohttp)](https://docs.aiohttp.org/en/stable/)

API wrapper for [CHSU schedule API](api.chsu.ru)

## Covered methods
* Auth (validate token and sign in)
* Building (get building list)
* StudentGroup (get all the student groups)
* Department (get list of departments and cathedras)
* Auditorium (get auditorium list)
* TimeTable (get number of academic week / get schedule for lecturer / group / full)
* Discipline (get list of discipline)
* Teacher (get list of lecturers)

## Example
```python
import asyncio

from chsu_api.api.api import CHSUApi

client = CHSUApi(username="USERNAME", password="PASSWORD")


async def main() -> None:
    await client.auth_signin()
    buildings = await client.get_buildings()
    print(buildings)


if __name__ == "__main__":
    asyncio.run(main())
```

## License
MIT