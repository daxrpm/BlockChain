"""Guion de Integrante 1 como datos: fuente única para el video y para docs/guion_integrante1.md.

Cada `Beat` es un fragmento de narración. La escena dura al menos lo que tarda en leerse
(a `WORDS_PER_SECOND`), así la animación nunca se adelanta a la expositora.

Uso: uv run python -m ledger_viz.intro_script > docs/guion_integrante1.md
"""

from typing import Final

from ledger_viz.script import MIN_SECONDS, WORDS_PER_SECOND, Beat, Section, find_section

__all__ = ["MIN_SECONDS", "SECTIONS", "WORDS_PER_SECOND", "Beat", "Section", "section"]

SECTIONS: Final = (
    Section(
        "I0_blockchain_vs_bitcoin",
        "El problema de confianza (portada)",
        (
            Beat(
                "portada",
                "El problema de confianza: ¿por qué necesitamos Blockchain? Antes de comenzar, "
                "mi grupo y yo consideramos importante aclarar algunas dudas que probablemente "
                "muchos de nosotros tenemos.",
            ),
            Beat(
                "confusion",
                "Creo que es normal que muchas personas confundan Blockchain con Bitcoin, porque "
                "ambos términos suelen aparecer juntos.",
            ),
            Beat(
                "diferencia",
                "Pero hay algo muy importante que debemos entender: Bitcoin es una criptomoneda "
                "que utiliza la tecnología Blockchain. Es decir, Blockchain es la tecnología y "
                "Bitcoin es una criptomoneda que utiliza esa tecnología.",
            ),
            Beat(
                "pregunta",
                "Muy sencillo hasta aquí. Pero entonces, ¿por qué surgió esta tecnología y qué "
                "problema busca resolver?",
            ),
        ),
    ),
    Section(
        "I1_sistema_centralizado",
        "Sistema centralizado",
        (
            Beat(
                "definicion",
                "Tradicionalmente, hemos utilizado sistemas centralizados, como los que "
                "encontramos en los bancos y otras entidades financieras. ¿Qué caracteriza a un "
                "sistema centralizado? Principalmente, que existe una autoridad central que tiene "
                "el control y gestiona los datos y las operaciones del sistema.",
            ),
            Beat(
                "participantes",
                "Pongamos un ejemplo para entenderlo mejor. Tenemos dos participantes: Alice y "
                "Bob. Alice quiere transferir dinero a Bob.",
            ),
            Beat(
                "solicitud",
                "¿Qué sucede? Alice solicita la transferencia a su banco. El banco recibe la "
                "solicitud,",
            ),
            Beat(
                "verifica",
                "verifica que la transacción cumpla las condiciones necesarias, autoriza la "
                "operación",
            ),
            Beat(
                "registra",
                "y actualiza su registro contable, es decir, su base de datos. Finalmente, Bob "
                "recibe el dinero.",
            ),
            Beat(
                "conclusion",
                "Tanto Alice como Bob dependen del banco para realizar y verificar esta "
                "operación. Entonces, ¿qué podemos concluir? En un sistema centralizado, existe "
                "una autoridad de confianza que se encarga de gestionar y validar las "
                "transacciones. Los participantes dependen de esta entidad para garantizar que "
                "las operaciones se realicen correctamente.",
            ),
        ),
    ),
    Section(
        "I2_problema_de_confianza",
        "El problema de confianza",
        (
            Beat(
                "sin_banco",
                "Ahora imaginemos que queremos realizar estas transacciones sin depender de un "
                "intermediario como un banco. ¿Por qué alguien querría hacerlo? Porque no todos "
                "los participantes necesariamente quieren depender de una única entidad para "
                "gestionar sus transacciones. Buscan poder interactuar directamente entre ellos.",
            ),
            Beat(
                "preguntas",
                "Pero aquí aparece un problema importante. Si eliminamos esa autoridad central, "
                "¿quién se encarga de validar las transacciones? ¿Dónde se almacena el registro "
                "contable? Y, sobre todo, ¿cómo podemos confiar en el sistema si no existe una "
                "entidad central que supervise las operaciones?",
            ),
            Beat(
                "confianza",
                "En el ejemplo anterior, Alice y Bob confían en el banco porque saben que existe "
                "una entidad responsable de verificar y registrar sus transacciones. Pero ¿cómo "
                "conseguimos esa misma confianza en un sistema descentralizado?",
            ),
        ),
    ),
    Section(
        "I3_sistema_descentralizado",
        "Sistema descentralizado",
        (
            Beat(
                "red",
                "En un sistema descentralizado, el control y la gestión se distribuyen entre "
                "múltiples participantes, que pueden operar mediante diferentes nodos de una red.",
            ),
            Beat(
                "replicas",
                "Ya no dependemos de una única autoridad central. En lugar de mantener un "
                "registro contable bajo el control de una sola entidad, podemos tener múltiples "
                "réplicas de ese registro, conocidas como ledgers, mantenidas por los nodos "
                "participantes.",
            ),
            Beat(
                "reglas",
                "Esto significa que diferentes nodos pueden conservar y verificar el mismo "
                "registro de transacciones, siguiendo unas reglas de protocolo compartidas.",
            ),
            Beat(
                "preguntas",
                "Volvamos al ejemplo anterior. Si Alice quiere transferir dinero a Bob, ¿cómo "
                "podríamos realizar esta operación sin acudir a un banco? ¿Quién verifica que "
                "Alice realmente tiene los fondos? ¿Cómo evitamos que intente gastar el mismo "
                "dinero dos veces?",
            ),
        ),
    ),
    Section(
        "I4_aparicion_de_blockchain",
        "La aparición de Blockchain",
        (
            Beat(
                "whitepaper",
                "Precisamente, este es el problema que Bitcoin buscó resolver. En 2008, una "
                "persona o grupo bajo el seudónimo de Satoshi Nakamoto publicó el documento "
                "técnico de Bitcoin, proponiendo un sistema de efectivo electrónico entre pares.",
            ),
            Beat(
                "directo",
                "La propuesta permitió realizar transferencias de valor directamente entre "
                "participantes, sin depender de una autoridad central para gestionar y validar "
                "el registro de transacciones.",
            ),
            Beat(
                "pilares",
                "Para conseguirlo, Bitcoin introdujo un sistema que utiliza criptografía, "
                "mecanismos de consenso y una estructura de datos conocida como cadena de "
                "bloques o Blockchain.",
            ),
            Beat(
                "otras",
                "Posteriormente, surgieron otras criptomonedas que también utilizan esta "
                "tecnología. Pero entonces, ¿cómo funciona exactamente Blockchain? ¿Cómo consigue "
                "que diferentes participantes puedan validar y mantener un mismo registro sin "
                "depender de una autoridad central?",
            ),
        ),
    ),
    Section(
        "I5_que_es_blockchain",
        "Blockchain: ¿qué es y cómo se organiza?",
        (
            Beat(
                "definicion",
                "Blockchain es una estructura de datos distribuida que almacena registros en "
                "bloques enlazados criptográficamente.",
                changed=True,
            ),
            Beat(
                "enlace",
                "Cada bloque guarda una referencia, un hash, del bloque anterior. Así se forma "
                "una cadena: el primer bloque no tiene anterior, por eso su hash previo es cero. "
                "Cómo está construido cada bloque por dentro lo explicará uno de mis compañeros.",
                changed=True,
            ),
        ),
    ),
    Section(
        "I6_propiedades",
        "Propiedades fundamentales",
        (
            Beat(
                "intro",
                "¿Qué garantías nos proporciona esta tecnología? ¿Cómo podemos confiar en que la "
                "información registrada se mantenga y que las transacciones sean válidas? Para "
                "responder a esto, vamos a explicar tres propiedades fundamentales: persistencia, "
                "seguridad y progreso.",
            ),
            Beat(
                "persistencia",
                "Primero, persistencia. ¿Qué significa esto? Significa que una vez que una "
                "transacción ha sido confirmada e incorporada a la cadena, su registro está "
                "diseñado para permanecer en ella. Recordemos que los bloques están enlazados "
                "criptográficamente. Si alguien intenta modificar información de un bloque "
                "anterior, cambiaría su hash y se rompería la correspondencia con los bloques "
                "posteriores. Esto hace que modificar el historial de transacciones sea "
                "extremadamente difícil.",
            ),
            Beat(
                "seguridad",
                "Segundo, seguridad. Los nodos honestos no discrepan sobre los registros "
                "confirmados: todos llegan a la misma versión de la historia. Para lograrlo "
                "intervienen los mecanismos de consenso y las reglas del protocolo. Los nodos "
                "verifican que las transacciones y los bloques cumplan esas reglas antes de "
                "aceptarlos.",
                changed=True,
            ),
            Beat(
                "seguridad_ejemplo",
                "Por ejemplo, si Alice intenta realizar una transacción utilizando fondos que no "
                "tiene disponibles o que ya fueron gastados, los nodos deben rechazarla. De esta "
                "manera, la red busca garantizar que los participantes mantengan un registro "
                "consistente.",
            ),
            Beat(
                "progreso",
                "Finalmente, progreso. ¿De qué nos serviría tener un sistema seguro si nunca "
                "pudiéramos registrar nuevas transacciones? El progreso se refiere a la capacidad "
                "de la red para seguir procesando transacciones válidas e incorporándolas a "
                "nuevos bloques. La cadena no solamente conserva las transacciones anteriores, "
                "sino que también puede seguir creciendo.",
            ),
            Beat(
                "conjunto",
                "En conjunto, estas tres propiedades buscan que Blockchain pueda mantener un "
                "registro persistente, verificar la validez de las operaciones y continuar "
                "incorporando nuevas transacciones sin depender de una autoridad central.",
            ),
        ),
    ),
    Section(
        "I8_como_protegemos",
        "¿Cómo protegemos la información?",
        (
            Beat(
                "repaso",
                "Ya sabemos qué garantías buscamos de esta tecnología. Pero todavía tenemos "
                "algunas preguntas importantes.",
                changed=True,
            ),
            Beat(
                "preguntas",
                "¿Cómo podemos saber que Alice realmente autorizó esa transacción? ¿Cómo podemos "
                "comprobar que nadie modificó la información durante su transmisión? Y, una vez "
                "que una transacción se incorpora a un bloque, ¿cómo podemos detectar si alguien "
                "intenta alterar su contenido?",
            ),
            Beat(
                "sin_autoridad",
                "Recordemos que en un sistema descentralizado no dependemos de una autoridad "
                "central que verifique personalmente cada operación. Entonces, ¿cómo conseguimos "
                "garantizar la autenticidad de las transacciones y la integridad de la "
                "información?",
            ),
            Beat(
                "criptografia",
                "Aquí es donde entra la criptografía. La criptografía proporciona mecanismos que "
                "permiten proteger la información, verificar la identidad y autorización de los "
                "participantes, y detectar modificaciones en los datos. Para entender cómo se "
                "consigue esto, mi compañera nos explicará los principales mecanismos de "
                "criptografía que se utilizan en Blockchain.",
            ),
        ),
    ),
)


def section(section_id: str) -> Section:
    return find_section(SECTIONS, section_id)


def render_markdown() -> str:
    total = sum(b.seconds for s in SECTIONS for b in s.beats)
    lines = [
        "# Integrante 1 — Introducción y fundamentos",
        "",
        "> Guion generado desde `src/ledger_viz/intro_script.py` (no editar a mano).",
        f"> Duración mínima del video: {total / 60:.1f} min a {WORDS_PER_SECOND} palabras/s.",
        "> ✏️ = cambio respecto al guion original (ver motivo en el chat / README).",
        "",
    ]
    for number, sec in enumerate(SECTIONS, start=1):
        lines += [f"## {number:02d} · {sec.slide}", "", f"Clip: `{sec.id}`", ""]
        lines += [f"- {'✏️ ' if b.changed else ''}{b.text}" for b in sec.beats]
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_markdown())  # noqa: T201 - salida de CLI
