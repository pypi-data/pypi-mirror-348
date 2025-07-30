import xfox
from Amisynth.utils import embeds  # Asumo que embeds es una lista global que estás usando

@xfox.addfunc(xfox.funcs)
async def author(texto: str=None, indice= 1, *args, **kwargs):
    """
    Guarda un autor en la lista de embeds, con el texto del autor y un índice opcional.
    Si se especifica el índice, se inserta o actualiza en esa posición. Si no, se agrega en la posición 1.
    
    :param texto: El texto que se quiere mostrar como autor en el embed.
    :param indice: El índice opcional del embed (posición en la lista).
    """
    if args:
        raise ValueError(f"❌ La función `$author` devolvió un error: demasiados argumentos, se esperaban hasta 2, se obtuvieron {len(args)+2}")
    
    if texto is None:
        print("[DEBUG AUTHOR] La funciom $author esta vacia.")
        raise ValueError("❌ La función `$author` devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    elif not indice is None:
        if not indice.isdigit():
            raise ValueError(f"❌ La función `$author` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}'")
        
   
    embed = {
        "author": texto, 
        "index": indice  
    }

    # Buscar si ya existe un embed con ese índice y actualizar solo el texto del autor
    for i, item in enumerate(embeds):
        if item.get("index") == indice:
            # Mantener los otros atributos del embed y solo actualizar el texto del autor
            embeds[i]["author"] = texto
            break
    else:
        # Si no se encontró, agregar uno nuevo
        embeds.append(embed)

    return ""
