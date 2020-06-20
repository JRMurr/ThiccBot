from discord import Role


async def get_role(ctx, role_name: str) -> Role:
    guild = ctx.message.guild
    server_roles = guild.roles
    desired_role = next((x for x in server_roles if x.name == role_name), None)
    if desired_role is None:
        await ctx.send(
            f"role with name ({role_name}) not found, "
            "make sure spelling and capitalization are the same"
        )
        return
    return desired_role
