"""Guion de Integrante 3 (estructura de datos y ledger): fuente única del video y del Markdown.

Cada beat es un clip (una diapositiva en Canva). Habla de blockchain en general; Bitcoin
solo aparece en el modelo interno que genera los hashes reales.

Uso: uv run python -m ledger_viz.part3_script > docs/guion_integrante3.md
"""

from typing import Final

from ledger_viz.script import WORDS_PER_SECOND, Beat, Section, find_section

MAX_SECONDS: Final = 6 * 60 + 40  # deja ~20 s de margen para pausas y clics dentro de 7 min

SECTIONS: Final = (
    Section(
        "S0",
        "Puente desde criptografía",
        (
            Beat(
                "S0_1_puente",
                "Mi compañera nos mostró dos herramientas: el **hash**, la huella digital de "
                "cualquier dato, y la **firma digital**, que prueba quién autorizó algo. Pero "
                "¿dónde se usan? ¿Qué guarda un blockchain y **cómo lo organiza**?",
                title="¿Dónde se usan el hash y la firma?",
                visual="Título «Estructura de datos y Ledger». Entran los íconos de la parte de "
                "cripto: huella (hash) y pluma (firma). Viajan hacia un cubo de alambre con un "
                "«?» adentro.",
            ),
            Beat(
                "S0_2_ruta",
                "Lo veremos en cuatro pasos: **ledger**, **transacción**, **bloque** y **árbol "
                "de Merkle**. Y quédense con esta idea: un blockchain es un cuaderno al que "
                "**solo se puede agregar**, y su estructura hace que **cualquier alteración se "
                "note**.",
                title="Hoja de ruta y tesis",
                visual="Cuatro pasos en fila que se encienden al nombrarlos. Abajo aparece la "
                "frase-tesis.",
            ),
        ),
    ),
    Section(
        "S1",
        "El ledger",
        (
            Beat(
                "S1_1_cuaderno",
                "Empecemos con algo cotidiano. Alice, Bob y Carol llevan sus cuentas en un "
                "cuaderno compartido. Alice empieza con 10 monedas. Luego anotan: Alice le paga "
                "5 a Bob, Bob le paga 2 a Carol y Carol le devuelve 1 a Alice.",
                title="El cuaderno compartido",
                visual="Alice, Bob y Carol a la izquierda y un cuaderno al centro. Cada línea "
                "se escribe en el momento en que la dices.",
            ),
            Beat(
                "S1_2_saldos",
                "Fíjense: **no hay columna de saldos**. ¿Cuánto tiene Bob? Recorremos el "
                "historial: recibió 5, pagó 2, le quedan 3. El saldo no se guarda, **se "
                "calcula**. Muchas blockchains funcionan así: registran transacciones, y los "
                "saldos se derivan de ellas.",
                title="Los saldos no se guardan, se calculan",
                visual="Panel SALDOS. Un cursor baja línea por línea y los números cambian. "
                "Al final se resalta «Bob: 3».",
            ),
            Beat(
                "S1_3_definicion",
                "Regla de oro: aquí **no se borra**. Si hay un error, se agrega una línea que "
                "lo corrige. Eso es un **ledger**, o libro mayor: un registro **ordenado** de "
                "transacciones al que **solo se puede agregar**, *append-only*.",
                title="Solo se puede agregar → definición",
                visual="Una goma intenta borrar, tiembla y sale una ✗. Se agrega una línea "
                "nueva abajo. Aparece la tarjeta de definición con «append-only».",
            ),
            Beat(
                "S1_4_replicado",
                "Pero en blockchain **cada nodo guarda su propia copia**. Y aparece un "
                "problema: Alice, que ahora tiene 7 monedas, envía a la vez 7 a Bob por un "
                "lado y 7 a Carol por otro. Cada mensaje parece válido. ¿Cuál cuenta?",
                title="Replicado → el problema",
                visual="El cuaderno se copia en 5 nodos. Alice envía dos mensajes hacia lados "
                "opuestos. El nodo central recibe ambos y muestra un «?».",
            ),
            Beat(
                "S1_5_orden",
                "Es el **doble gasto** que quedó abierto en la introducción. Parte de la "
                "solución es estructural: si todos tienen las transacciones **en el mismo "
                "orden**, la segunda llega tarde y se rechaza por falta de fondos. Necesitamos "
                "un **orden único**.",
                title="Doble gasto → orden único",
                visual="«⚠ DOBLE GASTO». Las dos transacciones se ordenan en una fila "
                "numerada: la 1.ª ✓ (saldo 7 → 0) y la 2.ª ✗ «fondos insuficientes». Queda la "
                "caja «Orden único».",
            ),
        ),
    ),
    Section(
        "S2",
        "La transacción",
        (
            Beat(
                "S2_1_campos",
                "Veamos qué es una transacción: un mensaje con formato fijo: **de quién, para "
                "quién, cuánto** y una **firma digital**. Como explicó mi compañera, la firma "
                "prueba que fue Alice, y nadie más, quien autorizó el pago.",
                title="Qué contiene",
                visual="Una línea del cuaderno se convierte en una tarjeta. Los campos De, "
                "Para, Monto y Firma aparecen al nombrarlos. La firma se resalta con una llave: "
                "«solo Alice puede generarla».",
            ),
            Beat(
                "S2_2_extras",
                "Según la red, lleva más datos: una **comisión** para quien la procesa y un "
                "**contador** que impide ejecutarla dos veces. Las reglas de cada red definen "
                "qué transacción es válida.",
                title="Campos que agrega cada red",
                visual="La tarjeta crece con dos filas nuevas: «Comisión» y «Contador nº 7 "
                "(no se repite)». Abajo se lee «válida = cumple las reglas de la red».",
            ),
            Beat(
                "S2_3_id",
                "¿Cómo la identificamos? **Con su hash**: el hash de su contenido es su "
                "identificador. Si alguien cambia el monto de 5 a 50, el identificador cambia "
                "**por completo**. Ya es otra transacción.",
                title="Su identidad es su hash",
                visual="«ID = hash(transacción)» y 16 caracteres reales. El 5 pasa a 50 y se "
                "marcan en rojo los caracteres que cambian.",
            ),
        ),
    ),
    Section(
        "S3",
        "De transacciones a bloques",
        (
            Beat(
                "S3_1_mempool",
                "Volvamos al orden. Las transacciones nuevas esperan en una sala llamada "
                "**mempool**. Ponerse de acuerdo sobre cada una, **una por una**, sería "
                "lentísimo.",
                title="La mempool y el cuello de botella",
                visual="Desde los nodos llegan tarjetas a la zona punteada «mempool». Un "
                "contador de «rondas de acuerdo» sube y se pone rojo.",
            ),
            Beat(
                "S3_2_agrupar",
                "La solución es **agrupar**: se acuerda un paquete completo de una vez. Ese "
                "paquete es un **bloque**. Cada red define **cada cuánto** se crea uno, de "
                "segundos a minutos, y un **tamaño máximo**; así un bloque lleva de decenas a "
                "miles de transacciones.",
                title="La solución: agrupar",
                visual="Las tarjetas entran a un cubo y el contador baja a 1: «1 bloque = 1 "
                "acuerdo». Al lado: «cada red: intervalo · tamaño máximo».",
            ),
            Beat(
                "S3_3_diferencia",
                "¿Ledger o bloque? El **ledger es el cuaderno completo**, el **bloque es una "
                "página** y la **transacción una línea**. El ledger es el registro; el bloque, "
                "la unidad con la que crece.",
                title="Ledger vs. bloque",
                visual="Tres columnas que se encienden al nombrarlas: cuaderno = Ledger, "
                "página = Bloque, línea = Transacción.",
            ),
        ),
    ),
    Section(
        "S4",
        "La cadena: del dibujo a la estructura de datos",
        (
            Beat(
                "S4_1_dibujo",
                "Recuerdan esta imagen de la introducción: bloques unidos por una línea. Pero "
                "¿qué es **esa línea** en realidad?",
                title="La imagen de la intro",
                visual="El zigzag del Canva: 5 cubos amarillos, línea punteada desde la "
                "izquierda y «Hash Previo» bajo cada cubo. Las líneas parpadean y aparece un «?».",
            ),
            Beat(
                "S4_2_estructura",
                "Veámoslo como **estructura de datos**. Cada bloque guarda su **propio hash**, "
                "su huella, y un campo llamado **hash previo**. Al crear un bloque nuevo, el "
                "hash del anterior **se copia** en ese campo.",
                title="Se transforma en estructura de datos",
                visual="Los cubos se aplanan en una fila de cajas con «Hash previo» y «Hash». "
                "El hash de cada bloque vuela con una flecha y se escribe en el «Hash previo» "
                "del siguiente.",
            ),
            Beat(
                "S4_3_puntero",
                "Esa línea **no es un cable, es un dato**: un **puntero de hash**. Como en una "
                "lista enlazada, cada bloque apunta al anterior, pero el puntero dice **dónde** "
                "está y también **cómo era exactamente**. Si el anterior cambia, ya no coincide.",
                title="Puntero de hash",
                visual="Desde cada «Hash previo» sale una flecha curva hacia el bloque "
                "anterior. Abajo: «puntero de hash = dónde está + cómo era». Los valores iguales "
                "se iluminan en pares.",
            ),
            Beat(
                "S4_4_genesis",
                "El primer bloque no tiene anterior: su hash previo es **todo ceros**. Es el "
                "**bloque génesis**, y viene fijado en el propio software de la red. Desde ahí, "
                "la cadena **solo crece hacia adelante**.",
                title="Génesis y crecimiento",
                visual="El bloque 1 pasa a llamarse «Génesis», con «Hash previo: 0000…». Por la "
                "derecha entra un bloque nuevo que copia el hash del último.",
            ),
        ),
    ),
    Section(
        "S5",
        "Estructura del bloque",
        (
            Beat(
                "S5_1_abrir",
                "**Abramos un bloque.** Tiene una **cabecera**, un resumen pequeño de tamaño "
                "fijo, y un **cuerpo** con la lista de transacciones.",
                title="Abrir el bloque",
                visual="Una caja de la fila crece y se divide en «CABECERA» arriba y «CUERPO · "
                "8 transacciones» abajo.",
            ),
            Beat(
                "S5_2_campos",
                "Cada red define su cabecera, pero casi todas incluyen: **versión** del "
                "protocolo; **hash previo**, el enlace que vimos; **raíz de Merkle**, el "
                "resumen de las transacciones; **marca de tiempo**; y campos del consenso, "
                "como **dificultad** y **nonce**, que se verán más adelante.",
                title="Los campos de la cabecera",
                visual="Cada fila se ilumina al nombrarla, con su valor real. «Dificultad» y "
                "«nonce» llevan la etiqueta «→ consenso».",
            ),
            Beat(
                "S5_3_hash_cabecera",
                "Detalle clave: el hash del bloque se calcula **solo con la cabecera**. Las "
                "transacciones no entran directamente. Entonces, ¿qué protege a las "
                "transacciones?",
                title="El hash solo cubre la cabecera",
                visual="La cabecera entra a la caja «hash» y sale el hash del bloque. El cuerpo "
                "se atenúa con un «?». La fila «Raíz de Merkle» parpadea.",
            ),
        ),
    ),
    Section(
        "S6",
        "Árbol de Merkle",
        (
            Beat(
                "S6_1_construir",
                "La respuesta es el **árbol de Merkle**. Calculamos el hash de cada "
                "transacción: las **hojas**. Unimos los hashes **de dos en dos** y volvemos a "
                "calcular el hash, nivel por nivel, hasta que queda uno: la **raíz**.",
                title="Construcción",
                visual="Ocho transacciones abajo. Las hojas aparecen primero y luego cada "
                "nivel al ritmo de la frase, con «H(izq ‖ der)» a un lado. La raíz brilla.",
            ),
            Beat(
                "S6_2_raiz",
                "Si un nivel es impar, normalmente se **duplica el último**. Y esa raíz, de "
                "apenas **32 bytes**, va en la cabecera: resume **todas** las transacciones sin "
                "contenerlas.",
                title="Caso impar y raíz en la cabecera",
                visual="Nota «impar → se duplica el último». La raíz vuela a la fila «Raíz de "
                "Merkle» de la cabecera.",
            ),
            Beat(
                "S6_3_atacante",
                "**Seamos el atacante**: cambiamos el pago de Bob a Carol de 2 a **20**. Cambia "
                "su hash, el de su par, y así hasta la raíz. Cambia la cabecera y cambia **el "
                "hash del bloque**.",
                title="Seamos el atacante",
                visual="«B→C:2» pasa a «B→C:20» en rojo. El camino sube en rojo con los hashes "
                "nuevos reales. La raíz de la cabecera se pone roja.",
            ),
            Beat(
                "S6_4_rotura",
                "Y el bloque siguiente guardaba el hash anterior, que **ya no coincide**: la "
                "cadena se rompe, y cualquier nodo lo detecta comparando un valor. Para "
                "ocultarlo habría que rehacer ese bloque **y todos los siguientes**. La "
                "estructura no lo hace imposible, lo hace **evidente**; lo impracticable lo "
                "pone el consenso.",
                title="La cadena se rompe",
                visual="Vuelve la fila de estructura de datos. El hash del bloque alterado "
                "cambia; el «Hash previo» del siguiente queda viejo, en rojo con «≠», y su "
                "flecha se parte con una ✗. Los siguientes se ponen rojos: «evidente ≠ "
                "imposible → consenso».",
            ),
            Beat(
                "S6_5_prueba",
                "Segundo superpoder: Dave, desde su celular, quiere saber si su pago está en "
                "el bloque **sin descargarlo**. Le bastan su transacción y **tres hashes**, los "
                "hermanos en el camino a la raíz. Recalcula la raíz y la compara con la "
                "cabecera.",
                title="Prueba de inclusión",
                visual="Un celular: «¿«A→D:2» está?». Se resalta la hoja; los 3 hermanos se "
                "marcan en verde y numerados; el camino sube en amarillo y aparece ✓.",
            ),
            Beat(
                "S6_6_escala",
                "Y escala muy bien: con ocho transacciones, **3** hashes; con un millón, solo "
                "**20**. Se llama **verificación simplificada de pagos**, y permite billeteras "
                "ligeras que solo guardan las cabeceras.",
                title="Escala logarítmica",
                visual="Tabla: 8 → 3 · 4 096 → 12 · 1 000 000 → 20 (log₂ n), y «SPV: "
                "billeteras ligeras, solo cabeceras».",
            ),
        ),
    ),
    Section(
        "S7",
        "Cierre",
        (
            Beat(
                "S7_1_resumen",
                "En resumen: las transacciones, **firmadas** e **identificadas por su hash**, "
                "se agrupan en **bloques**; **Merkle** las resume en la cabecera; y el hash de "
                "cada cabecera va **en el siguiente bloque**, formando la cadena.",
                title="El viaje completo",
                visual="Recorrido de izquierda a derecha: transacción → bloque → Merkle → "
                "cabecera → cadena enlazada.",
            ),
            Beat(
                "S7_2_tesis",
                "Un blockchain es un cuaderno **al que solo se puede agregar**, donde "
                "**cualquier alteración se nota**. Falta saber **quién decide qué bloque "
                "entra**: eso lo veremos con el consenso.",
                title="Tesis y relevo",
                visual="Vuelve la frase-tesis junto a la cadena. Llega un bloque nuevo con un "
                "«?»: «¿quién decide? → consenso».",
            ),
        ),
    ),
)

SOURCES: Final = (
    ("Ledger append-only, replicado y *tamper evident*", "NIST IR 8202 (2018), §1–3"),
    ("Doble gasto y orden único", "Nakamoto (2008), §2; NIST IR 8202 §4"),
    ("Hash previo, cabecera y raíz de Merkle", "NIST IR 8202 §3.3–3.4"),
    (
        "Puntero de hash / lista enlazada",
        "Narayanan et al., *Bitcoin and Cryptocurrency Technologies* (Princeton, 2016), cap. 1",
    ),
    (
        "Comisión y contador (nonce de cuenta)",
        "Documentación de transacciones de Ethereum (ethereum.org)",
    ),
    (
        "Árbol de Merkle y prueba de inclusión",
        "Merkle (1987); NIST IR 8202 §3.4; Nakamoto §7–8 (SPV)",
    ),
)


def section(section_id: str) -> Section:
    return find_section(SECTIONS, section_id)


def _clock(seconds: float) -> str:
    whole = round(seconds)
    return f"{whole // 60}:{whole % 60:02d}"


def render_markdown() -> str:
    total = sum(b.seconds for s in SECTIONS for b in s.beats)
    n_beats = sum(len(s.beats) for s in SECTIONS)
    lines = [
        "# Integrante 3 — Estructura de datos y Ledger · Guion de 7 minutos",
        "",
        "> Generado desde `src/ledger_viz/part3_script.py` (no editar a mano: `make guion`).",
        (
            f"> Va después de **Integrante 2 (criptografía)**. Ritmo: **{WORDS_PER_SECOND} "
            "palabras/s**."
        ),
        (
            "> Cada **beat** = una diapositiva de Canva con su clip. La animación se dispara "
            "cuando dices cada frase, dura lo que tardas en decir el texto y luego "
            "**se queda quieta**: si vas lento, espera; si terminas, haces clic."
        ),
        (
            "> 🗣️ = lo que dices (conversacional, no literal) · 🎬 = lo que se ve · **negrita** = "
            "énfasis."
        ),
        "",
        "## Mapa de tiempos",
        "",
        "| § | Tema | Beats | Inicia |",
        "|---|---|---|---|",
    ]
    elapsed = 0.0
    for sec in SECTIONS:
        lines.append(f"| {sec.id[1:]} | {sec.slide} | {len(sec.beats)} | {_clock(elapsed)} |")
        elapsed += sum(b.seconds for b in sec.beats)
    lines += [
        f"| | **Total** | **{n_beats}** | **{_clock(total)} de habla** |",
        "",
        (
            f"{_clock(total)} de habla + pausas y clics ≈ **7:00**. Si al ensayar te pasas, "
            "recorta 2.2 (campos extra) y 6.2 (caso impar)."
        ),
        "",
        "---",
        "",
    ]
    clip = 0
    for sec in SECTIONS:
        lines += [f"## {sec.id[1:]} · {sec.slide}", ""]
        for number, b in enumerate(sec.beats, start=1):
            clip += 1
            lines += [
                (
                    f"**{sec.id[1:]}.{number} · {b.title}** · ⏱ {b.seconds:.0f} s · "
                    f"clip `{clip:02d}_{b.id}`"
                ),
                f'- 🗣️ "{b.text}"',
                f"- 🎬 {b.visual}",
                "",
            ]
    lines += ["---", "", "## Fuentes", "", "| Dato | Fuente |", "|---|---|"]
    lines += [f"| {fact} | {src} |" for fact, src in SOURCES]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_markdown())  # noqa: T201 - salida de CLI
