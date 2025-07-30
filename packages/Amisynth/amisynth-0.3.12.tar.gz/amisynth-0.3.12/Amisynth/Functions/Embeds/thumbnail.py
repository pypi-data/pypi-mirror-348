import xfox
from Amisynth.utils import embeds
from Amisynth.utils import valid_url

@xfox.addfunc(xfox.funcs)
async def thumbnail(url: str, indice=1, *args, **kwargs):
    """
    Guarda un thumbnail en la lista de embeds, con una URL de imagen específica y un índice opcional.
    Si se especifica el índice, se inserta o actualiza en esa posición. Si no, se agrega en la posición 1.
    """
    if args:
        raise ValueError(f"❌ La función `$thumbnail` devolvió un error: demasiados argumentos, se esperaban hasta 2, se obtuvieron {len(args)+2}")

    if url is None:
        print("[DEBUG THUMBNAIL] La funciom $thumbnail esta vacia")
        raise ValueError("❌ La función `$thumbnail` devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    
    if valid_url(url) == False:
        raise ValueError(f"❌ La función `$thumbnail` devolvió un error: se esperaba una URL en la posición 1, se obtuvo '{url}'")
    
    elif not indice is None:
        if not indice.isdigit():
            raise ValueError(f"❌ La función `$thumbnail` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}'")

    
    embed = {
        "thumbnail_icon": url,  # URL de la imagen como thumbnail
        "index": indice    # Añadir el índice para identificar la posición
    }

    
    found = False
    for i, item in enumerate(embeds):
        if item.get("index") == indice:
           
            embeds[i]["thumbnail_icon"] = url
            found = True
            break
    if not found:

        embeds.append(embed)

    return ""
