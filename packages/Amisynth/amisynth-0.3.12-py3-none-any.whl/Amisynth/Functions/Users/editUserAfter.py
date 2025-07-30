import xfox

@xfox.addfunc(xfox.funcs)
async def editUserAfter(option=None, *args, **kwargs):
    if "ctx_guild_channel_edit" in kwargs:
        after = kwargs["ctx_user_edit"][1]
        return getattr(after, option, "")
    return ""
