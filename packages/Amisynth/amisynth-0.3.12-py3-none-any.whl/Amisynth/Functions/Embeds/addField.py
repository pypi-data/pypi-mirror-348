import xfox
from Amisynth.utils import embeds  # Asumo que embeds es una lista global que estás usando

@xfox.addfunc(xfox.funcs, name="addField")
async def add_field(nombre: str=None, valor: str=None, inline: bool = False, indice: int = 1, *args, **kwargs):
    """
    Agrega un campo (field) a un embed en la lista de embeds.
    Si el embed en el índice especificado ya existe, se agrega el field a su lista de fields.
    Si no existe, se crea un nuevo embed con ese índice y el field.
    
    :param nombre: Nombre del campo (name).
    :param valor: Contenido del campo (value).
    :param inline: Si el campo es inline o no (por defecto, True).
    :param indice: Índice del embed en la lista (por defecto, 1).
    """
    if args:
        raise ValueError(f"❌ La función `$addField` devolvió un error: demasiados argumentos, se esperaban hasta 4, se obtuvieron {len(args)+4}")
    
    if nombre is None:
        print("[DEBUG ADDFIELD] La funciom $addField esta vacia")
        raise ValueError("❌ La función `$addField` devolvió un error: se esperaba un valor válido en la posición 1, se obtuvo un valor vacío")
    elif valor is None:
        print(f"[DEBUG ADDFIELD] La función `$addField` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}")
        raise ValueError(f"❌ La función `$addField` devolvió un error: se esperaba un entero en la posición 2, se obtuvo '{indice}'")
    
    elif inline is not None:
        if not inline.lower() in ["yes", "no", "si", "false", "true"]:
            raise ValueError(f"❌ La función `$addField` devolvió un error: se esperaba un valor booleano en la posición 3, se obtuvo '{inline}'")


    elif not indice is None:
        if not indice.isdigit():
            raise ValueError(f"❌ La función `$addField` devolvió un error: se esperaba un entero en la posición 4, se obtuvo '{indice}'")
    

    # Buscar si ya existe un embed con ese índice
    for i, item in enumerate(embeds):
        if item["index"] == indice:
            # Si el embed no tiene fields, inicializar la lista
            if "fields" not in embeds[i]:
                embeds[i]["fields"] = []
            
            # Agregar el nuevo campo
            embeds[i]["fields"].append({
                "name": nombre,
                "value": valor,
                "inline": inline
            })
            break
    else:
        # Si no se encontró, crear un nuevo embed con el field
        embed = {
            "index": indice,
            "fields": [{
                "name": nombre,
                "value": valor,
                "inline": inline
            }]
        }
        embeds.append(embed)

    return ""
