import asyncio

from chsu_schedule_api import CHSUApi
from chsu_schedule_api.types import Group

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
