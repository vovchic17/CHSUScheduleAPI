<img src="https://raw.githubusercontent.com/vovchic17/static/main/src/logo.svg" alt="drawing" width="150"/>


# CHSUScheduleAPI
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Aiohttp](https://img.shields.io/badge/aiohttp-v3.9.3-2c5bb4?logo=aiohttp)](https://docs.aiohttp.org/en/stable/)
[![Checked with mypy](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/vovchic17/static/main/src/badges/mypy.json)](https://mypy-lang.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Asynchronous API wrapper for [CHSU schedule API](http://api.chsu.ru)

## Covered methods
* Auth (validate token and sign in)
* Building (get building list)
* StudentGroup (get all the student groups)
* Department (get list of departments and cathedras)
* Auditorium (get auditorium list)
* TimeTable (get number of academic week / get schedule for lecturer / group / full)
* Discipline (get list of discipline)
* Teacher (get list of lecturers)

## Installation

Install via pip

```shell
pip install chsu_schedule_api
```

## Example
Get building list
```python
import asyncio

from chsu_schedule_api import CHSUApi

client = CHSUApi(username="USERNAME", password="PASSWORD")


async def main() -> None:
    await client.auth_signin()
    buildings = await client.get_buildings()
    print(buildings)


if __name__ == "__main__":
    asyncio.run(main())
```

## Example
Get your group schedule
```python
import asyncio

from chsu_schedule_api import CHSUApi
from chsu_schedule_api.models import Group

client = CHSUApi(username="USERNAME", password="PASSWORD")

async def main() -> None:
    await client.auth_signin()
    group_tt = await client.get_time_table(
        Group(title="1ИСб-01-1оп-22")
    )

    for tt in group_tt:
        print(
            tt.start_time,
            tt.end_time,
            tt.discipline.title,
            tt.auditory.title
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## License
MIT