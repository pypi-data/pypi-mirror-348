import xfox
import discord
import Amisynth.utils as utils


@xfox.addfunc(xfox.funcs)
async def kick(user_id: int=None, reason="Ninguna", *args, **kwargs):
    contexto = utils.ContextAmisynth()

    try:
        if args:
            raise ValueError(f"❌ La función `$kick` devolvió un error: demasiados argumentos, se esperaban hasta 2, se obtuvieron {len(args)+2}")
        
        # Validación de tipo de ID
        if not isinstance(user_id, int):
            raise ValueError("El ID debe ser un número entero válido.")

        # Buscar al miembro
        member = await contexto.obj_guild.fetch_member(user_id)

        # Intentar expulsar al miembro
        await member.kick(reason=reason)

        return ""

    except ValueError as ve:
        # Imprimir el error de valor
        raise ValueError(f"❌ La funcion `$kick` devolvio un error: error de valor '{ve}'")

    except discord.NotFound:
        # Si no se encuentra al miembro en el servidor
        raise ValueError("❌ La funcion `$kick` devolvio un error: No se encontró al usuario en este servidor.")

    except discord.Forbidden:
        # Si no se tienen permisos suficientes
        raise ValueError(f"❌ La funcion `$kick` devolvio un error: No tengo permisos suficientes para expulsar al usuario `{user_id}`.")

    except discord.HTTPException as e:
        # Si ocurre un error HTTP al intentar la acción
       raise ValueError(f"❌ La funcion `$kick` devolvio un error: error de red al expulsar, se obtuvo el codigo {e.code}")

    except Exception as e:
        # Para cualquier otro error inesperado
        raise ValueError(f"❌ La funcion `$kick` devolvio un error: Ocurrió un error inesperado: {e}")
