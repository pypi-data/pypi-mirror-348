import xfox
import Amisynth.utils as utils
import re


@xfox.addfunc(xfox.funcs)
async def research(patron=None, text=None, *args, **kwargs):
    # Si detectas que recibió "d+" en vez de "\d+", lo arreglamos
    # Esto reemplaza por ejemplo "d+" → "\d+", "w+" → "\w+", etc.

    if patron is None:
        raise ValueError("❌ La función `$reseach`devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    elif text is None:
        raise ValueError("❌ La función `$research`devolvió un error: se esperaba un valor válido en la posición 2, se obtuvo un valor vacío")
    
    patron_corregido = re.sub(r"\b([dwsS])", r"\\\1", patron)

    n = re.search(patron_corregido, text)
    return n.group() if n else None
