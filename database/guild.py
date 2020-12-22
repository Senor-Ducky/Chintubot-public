from utilities import GUILD, GUILD_DATA


async def query_guild(guild_id: int):
    if guild_id in GUILD_DATA:
        return
    print("Creating")
    document = {"_id": guild_id, "prefix": "!"}
    await GUILD.insert_one(document)
    GUILD_DATA[guild_id] = {"prefix": "!"}


async def set_variable(guild_id: int, name: str, value):
    GUILD_DATA[guild_id][name] = value
    await GUILD.update_one({"_id": guild_id}, {"$set": {name: value}})


async def unset_variable(guild_id: int, name: str):
    try:
        del GUILD_DATA[guild_id][name]
    except KeyError:
        pass
    await GUILD.update_one({"_id": guild_id}, {"$unset": {name: ""}})


async def moderation(guild_id: int, arg: int, operation: str = None):
    if GUILD_DATA[guild_id].get("moderation_permissions") is None:
        GUILD_DATA[guild_id]["moderation_permissions"] = []
    if operation is None:
        if arg in GUILD_DATA[guild_id].get("moderation_permissions"):
            return False
        GUILD_DATA[guild_id]["moderation_permissions"].append(arg)
    else:
        if arg not in GUILD_DATA[guild_id].get("moderation_permissions"):
            return False
        GUILD_DATA[guild_id]["moderation_permissions"].remove(arg)
    await GUILD.update_one(
        {"_id": guild_id},
        {
            "$set": {
                "moderation_permissions": GUILD_DATA[guild_id]["moderation_permissions"]
            }
        },
    )
    return True


async def welcome_role(guild_id: int, arg: int, operation: str = None):
    roles = GUILD_DATA[guild_id].get("welcome_roles")
    if roles is None:
        roles = GUILD_DATA[guild_id]["welcome_roles"] = []
    if operation is None:
        if roles is None or arg in roles:
            return False
        GUILD_DATA[guild_id]["welcome_roles"].append(arg)
    else:
        if roles is None or arg not in roles:
            return False
        GUILD_DATA[guild_id]["welcome_roles"].remove(arg)
    await GUILD.update_one(
        {"_id": guild_id},
        {"$set": {"welcome_roles": GUILD_DATA[guild_id]["welcome_roles"]}},
    )
    return True
