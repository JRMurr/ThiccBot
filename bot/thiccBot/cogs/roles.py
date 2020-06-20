from discord import Guild, Role, RawReactionActionEvent, Member
from discord.ext import commands, menus
from thiccBot.bot import ThiccBot
from thiccBot.cogs.utils import checks, misc
from thiccBot.cogs.utils.logError import get_error_str, log_and_send_error
import logging

log = logging.getLogger(__name__)


class RoleMenu(menus.Menu):
    def __init__(self, role: Role, *args, **kwargs):
        super(RoleMenu, self).__init__(*args, **kwargs)
        self.role = role

    async def send_initial_message(self, ctx, channel):
        msg = f"React with :white_check_mark: to add/remove the role ({self.role.name})"
        return await channel.send(msg)

    @menus.button("\N{White Heavy Check Mark}")
    async def on_check(self, payload: RawReactionActionEvent):
        user_id = payload.user_id
        member: Member = self.ctx.guild.get_member(user_id)
        is_add = payload.event_type == "REACTION_ADD"
        try:
            if is_add:
                await member.add_roles(self.role)
                await member.send(f"Added role: ({self.role.name})")
            else:
                await member.remove_roles(self.role)
                await member.send(f"Removed role: ({self.role.name})")
        except Exception as e:
            log.error(f"Error modifying role. {e}")
            self.ctx.send(f"Error modifying role")


class Roles(commands.Cog):
    def __init__(self, bot: ThiccBot):
        # TODO: add on unload to stop menus
        self.bot = bot
        self.initialized_guilds = set()
        self.menus = []
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            await self.setup_message_listener(guild)

    def cog_unload(self):
        for m in self.menus:
            m.stop()

    async def setup_message_listener(self, guild: Guild):
        if guild in self.initialized_guilds:
            return
        async with self.bot.backend_request(
            "get", f"/discord/roles/{guild.id}"
        ) as r:
            if r.status == 200:
                data = await r.json()
                for info in data:
                    role = guild.get_role(info["role_id"])
                    if not role:
                        log.error(
                            f"role: {info['role_id']} not found in guild: {guild}"
                        )
                        continue
                    channel = guild.get_channel(info["channel_id"])
                    if not channel:
                        log.error(
                            f"channel: {info['channel_id']} not found in guild: {guild}"
                        )
                        continue
                    try:
                        message = await channel.fetch_message(
                            info["message_id"]
                        )
                        m = RoleMenu(role, message=message)
                        ctx = await self.bot.get_context(message)
                        await m.start(ctx)
                        self.menus.append(m)
                    except Exception as e:
                        log.error(f"Error setting up menu: {info}. {e}")
                        continue
                self.initialized_guilds.add(guild)
            else:
                log.error(
                    await get_error_str(
                        r,
                        f"Error initializing message listeners for guild ({guild}): ",
                    )
                )

    @commands.group(name="roles", aliases=["role"])
    @commands.guild_only()
    async def roles(self, ctx):
        """Commands for creating and mangaging role assignment messages
        
        If no commands are showing up here, give the bot manage_roles
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f"run {ctx.prefix}help roles.\n")

    @roles.command(name="create_message")
    @checks.is_bot_admin()
    @commands.bot_has_permissions(manage_roles=True)
    async def create_message(self, ctx, role_name: str):
        role = await misc.get_role(ctx, role_name)
        if not role:
            return

        m = RoleMenu(role)
        await m.start(ctx)
        data = {
            "role_id": role.id,
            "message_id": m.message.id,
            "channel_id": ctx.channel.id,
        }
        async with self.bot.backend_request(
            "POST", f"/discord/roles/{ctx.guild.id}", json=data
        ) as r:
            if r.status != 200:
                log_and_send_error(
                    log, r, ctx, f"Error setting up role message: "
                )
                m.stop()
            else:
                self.menus.append(m)


def setup(bot):
    bot.add_cog(Roles(bot))

