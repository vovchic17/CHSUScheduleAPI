from chsu_schedule_api import CHSUApi
from chsu_schedule_api.types import Group

client = CHSUApi(username="USERNAME", password="PASSWORD")

client.auth_signin()
group_tt = client.get_time_table(
    Group(title="1ИСб-01-1оп-22")
)

for tt in group_tt:
    print(
        tt.start_time,
        tt.end_time,
        tt.discipline.title,
        tt.auditory.title
    )
