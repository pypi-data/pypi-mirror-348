import xfox
from Amisynth.utils import embeds  # Asumo que embeds es una lista global que estás usando
from Amisynth.utils import valid_url

@xfox.addfunc(xfox.funcs)
async def titleURL(url: str, indice= 1, *args, **kwargs):
    """
    Guarda una URL en el título del embed, con un índice opcional.
    Si se especifica el índice, se inserta o actualiza en esa posición. Si no, se agrega en la posición 1.
    
    :param url: La URL que se quiere asociar al título del embed.
    :param indice: El índice opcional del embed (posición en la lista).
    """
    if args:
        raise ValueError(f"❌ La función `$titleURL` devolvió un error: demasiados argumentos, se esperaban hasta 2, se obtuvieron {len(args)+2}")

    if url is None:
        print("[DEBUG TITLEURL] La funciom $titleURL esta vacia.")

        raise ValueError("❌ La función `$titleURL` devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    elif valid_url(url) == False:
        raise ValueError(f"❌ La función `$titleURL` devolvió un error: se esperaba una URL en la posición 1, se obtuvo '{url}'")

    elif not indice is None:
        if not indice.isdigit():
            raise ValueError(f"❌ La función `$titleURL` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}'")
        
    # Crear el embed con la URL en el título
    embed = {
        "title_url": url,  # URL asociada al título
        "index": indice    # Añadir el índice para identificar la posición
    }

    # Buscar si ya existe un embed con ese índice y actualizar solo la URL
    for i, item in enumerate(embeds):
        if item.get("index") == indice:
            # Mantener los otros atributos del embed y solo actualizar la URL
            embeds[i]["title_url"] = url
            break
    else:
        # Si no se encontró, agregar uno nuevo
        embeds.append(embed)

    return ""
