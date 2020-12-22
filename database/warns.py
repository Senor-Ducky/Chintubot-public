from utilities import WARN
import datetime


async def add_warn(guild_id: int, receiver_id: int, giver_id: int, reason: str):
    await WARN.insert_one(
        {
            "guild_id": guild_id,
            "receiver_id": receiver_id,
            "giver_id": giver_id,
            "reason": reason,
            "time": datetime.datetime.now(),
        }
    )


async def retrieve_warns(guild_id: int, member_id: int):
    return (
        await WARN.find({"guild_id": guild_id, "receiver_id": member_id})
        .sort("time", -1)
        .to_list(length=10)
    )
