from aiohttp import ContentTypeError
from pprint import pformat


async def get_error_str(r, prefix=""):
    message = await get_error_message(r)
    if message is None:
        message = ""
    return f"{prefix}HTTPCODE: {r.status}, ERROR REASON: {r.reason}, {message}"


async def get_error_message(r):
    try:
        data = await r.json()
        if data is not None and "message" in data:
            return data["message"]
        else:
            return None
    except ContentTypeError:
        return None


async def log_and_send_error(log, r, ctx, prefix):
    error_message = await get_error_message(r)
    if error_message is None:
        error_message = "Unknown Error"
    await ctx.send(f"{prefix}: {error_message}")
    await log_with_ctx(log, r, ctx, prefix, error_message)


async def log_with_ctx(log, r, ctx, prefix, error_message=None):
    if error_message is None:
        error_message = await get_error_message(r)
        if error_message is None:
            error_message = ""
    log.error(
        f"""{prefix}HTTPCODE: {r.status}, ERROR REASON: {r.reason}, {error_message}
        Context: {context_info(ctx)}"""
    )


def context_info(ctx):
    return {
        "author": ctx.author,
        "command_args": ctx.args,
        "command_kwargs": ctx.kwargs,
    }

