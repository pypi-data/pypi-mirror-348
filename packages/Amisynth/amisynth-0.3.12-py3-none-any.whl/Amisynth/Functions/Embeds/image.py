import xfox
from Amisynth.utils import embeds  # Asegúrate de que 'embeds' sea la lista global que deseas modificar
from Amisynth.utils import valid_url


@xfox.addfunc(xfox.funcs)
async def image(url_imagen: str=None, indice=1, *args, **kwargs):
    """
    Guarda una imagen en la lista de embeds, con una URL de imagen específica y un índice opcional.
    Si se especifica el índice, se inserta o actualiza en esa posición. Si no, se agrega en la posición 1.
    """
    if args:
        raise ValueError(f"❌ La función `$image` devolvió un error: demasiados argumentos, se esperaban hasta 2, se obtuvieron {len(args)+2}")
    
    if url_imagen is None:
        print("[DEBUG IMAGE] La funciom $image esta vacia.")
        raise ValueError("❌ La función `$image` devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    
    elif url_imagen:
        if valid_url(url_imagen) == False:
            raise ValueError(f"❌ La función `$image` devolvió un error: se esperaba una URL en la posición 1, se obtuvo '{url_imagen}'")
    
    elif not indice is None:
        if not indice.isdigit():
            raise ValueError(f"❌ La función `$image` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}'")
        
    embed = {
        "image": url_imagen,  # Solo la URL de la imagen
        "index": indice       # Añadir el índice para identificar la posición
    }

    # Buscar si ya existe un embed con ese índice y actualizar solo la imagen
    found = False
    for i, item in enumerate(embeds):
        if item.get("index") == indice:
            # Mantener los otros atributos del embed y solo actualizar la imagen
            embeds[i]["image"] = url_imagen
            found = True
            break
    if not found:
        # Si no se encontró, agregar uno nuevo
        embeds.append(embed)

    return ""
