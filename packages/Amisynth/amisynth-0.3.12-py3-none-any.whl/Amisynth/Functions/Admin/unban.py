import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def unban(user_id: int, *args, **kwargs):
    contexto = utils.ContextAmisynth()

    try:
        if args:
            raise ValueError(f"❌ La función `$unban` devolvió un error: demasiados argumentos, se esperaban hasta 1, se obtuvieron {len(args)+1}")

        # Validación del ID
        if not isinstance(user_id, int):
            raise ValueError("❌ La función `$unban` devolvió un error: el ID debe ser un número entero válido.")

        # Obtener lista de baneados
        banned_users = await contexto.obj_guild.bans()
        member_to_unban = discord.utils.get(banned_users, user__id=user_id)

        if member_to_unban is None:
            raise discord.NotFound("❌ La función `$unban` devolvió un error: no se encontró al usuario en la lista de baneos.")

        # Desbanear al usuario
        await contexto.obj_guild.unban(member_to_unban.user)

        return ""

    except ValueError as ve:
        raise ValueError(f"❌ La función `$unban` devolvió un error: error de valor: '{ve}'")

    except discord.NotFound:
        raise ValueError("❌ La función `$unban` devolvió un error: no se encontró al usuario en la lista de baneos del servidor.")

    except discord.Forbidden:
        raise ValueError("❌ La función `$unban` devolvió un error: no tengo permisos suficientes para desbanear al usuario.")

    except discord.HTTPException as e:
        raise ValueError(f"❌ La función `$unban` devolvió un error: error de red al desbanear: '{e}'")

    except Exception as e:
        raise ValueError(f"❌ La función `$unban` devolvió un error: ocurrió un error inesperado: '{e}'")
