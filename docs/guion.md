# Integrante 3 — Estructura de datos y Ledger

> Guía de estudio + guion + storyboard de animaciones (Manim).
> Estado: **teoría vigente · guion reemplazado por [guion_integrante3.md](guion_integrante3.md)** · Exposición: desde el 9-nov-2026 · Duración objetivo: 6–7 min.

---

## 0. Dónde encaja tu parte

| Antes de ti | Tú | Después de ti |
|---|---|---|
| Intro (1): problema de confianza, centralizado vs. descentralizado, "bloques enlazados por hash previo". Cripto (2): hash como huella digital, firmas. | **¿Qué se guarda y cómo se organiza?** Ledger → transacción → bloque → cabecera → Merkle. | Arquitectura (4), P2P (5), **Consenso (6)**: quién decide qué bloque entra. |

**Reglas para no pisar a nadie**

- **No** expliques qué es un hash ni cómo funciona una firma: eso lo hizo Integrante 2. Tú solo lo usas ("como vimos, el hash es la huella digital de los datos").
- **No** expliques minería ni prueba de trabajo: eso es del 6. Tú cierras con "quién decide qué página se agrega lo verá mi compañero".
- La intro ya mostró la cadena de cubos. Tú **abres el cubo**.

**Tu frase-tesis** (dila al inicio y al cierre):

> "Un blockchain es un cuaderno contable donde solo se puede agregar. Su estructura hace que cualquier alteración se note."

---

## 1. Teoría completa (lo que debes dominar, aunque no lo digas todo)

### 1.1 Ledger (libro mayor)

- **Definición:** un registro **ordenado** de transacciones al que **solo se puede agregar** (*append-only*). NIST lo describe como un ledger distribuido formado por bloques, donde cada cabecera enlaza criptográficamente a la anterior, lo que lo vuelve *tamper evident* (las alteraciones se notan).
- **Ledger de transacciones vs. ledger de saldos** (Gensler, MIT 15.S12): Bitcoin guarda **transacciones** y el saldo **se calcula**. Ethereum guarda **estados/saldos** (modelo de cuentas).
  - **UTXO (Bitcoin):** "salidas de transacción no gastadas", como billetes. Para pagar 7 con un billete de 10, gastas el 10 entero y te devuelves 3 de cambio.
  - **Cuentas (Ethereum):** un saldo por dirección, como un banco. Necesita un *nonce* por cuenta para evitar que se repita la misma transacción (ataque de repetición).
- **Por qué importa el orden:** el whitepaper de Bitcoin dice que la única forma de saber que una transacción **no** ocurrió es conocer **todas** las transacciones. Por eso deben anunciarse públicamente y los participantes deben acordar **un único historial del orden** en que llegaron. Ese es el problema del **doble gasto**.
- **Antecedente histórico (dato fuerte para el público):** Haber y Stornetta (1991), *How to Time-Stamp a Digital Document*. Encadenaban hashes de documentos y publicaban el hash en un periódico. Es la idea de "cadena de sellos de tiempo" que Satoshi cita en la sección 3 del whitepaper. Curiosidad: el whitepaper **nunca usa la palabra "blockchain"**.

### 1.2 Transacción

- Contenido mínimo: **de** quién, **para** quién, **monto** y **firma** del emisor (la firma la explicó Integrante 2).
- **ID de transacción (txid)** = hash de la transacción. Si cambias un solo dígito, el txid cambia por completo (efecto avalancha). En Bitcoin es SHA-256 aplicado dos veces.
- Para que sea válida, el emisor debe tener fondos según el historial y la firma debe verificar.

### 1.3 ¿Por qué agrupar en bloques?

1. **Acordar el orden cuesta.** En una red distribuida, ponerse de acuerdo transacción por transacción, con miles por minuto y nodos repartidos por el mundo, sería lentísimo. Se acuerda **por lotes**: un bloque = una página.
2. **Sello de tiempo por lote.** El whitepaper (sección 3, *Timestamp Server*) propone hashear un **bloque de elementos** y publicar ese hash. Cada sello incluye el anterior y así se forma la cadena.
3. **Ritmo:** en Bitcoin sale un bloque cada ~10 min en promedio con miles de transacciones. En Ethereum, cada ~12 s.

**Analogía central:** ledger = **cuaderno**, bloque = **página**, transacción = **línea**.

| | Ledger | Bloque |
|---|---|---|
| Qué es | El historial completo (concepto) | La unidad en que se agrega y se sella |
| Tamaño | Crece para siempre | Acotado |
| Identidad | — | Su hash (el de la cabecera) |
| Relación | Es la secuencia de todos los bloques | Apunta al bloque anterior con `prev_hash` |

### 1.4 Estructura del bloque (Bitcoin)

Fuente: *Mastering Bitcoin*, cap. "The Blockchain".

| Campo de la **cabecera** | Tamaño | Para qué sirve |
|---|---|---|
| Versión | 4 B | Reglas del protocolo que sigue |
| **Hash del bloque anterior** | 32 B | Enlace con el bloque previo: **forma la cadena** |
| **Raíz de Merkle** | 32 B | Resumen de **todas** las transacciones del cuerpo |
| Timestamp | 4 B | Cuándo se creó |
| Dificultad (bits) | 4 B | Objetivo de la prueba de trabajo (lo explica el 6) |
| Nonce | 4 B | Contador que usan los mineros (lo explica el 6) |
| **Total** | **80 B** | |

- **Cuerpo:** contador de transacciones + la lista de transacciones. La primera es la *coinbase*, que paga la recompensa al minero.
- **Hash del bloque = SHA-256(SHA-256(cabecera)).** Se calcula **solo sobre la cabecera**. La altura del bloque no se guarda dentro de él.
- **Bloque génesis:** el primero (3-ene-2009). Su "hash anterior" es todo ceros, como el 0000 de la diapositiva de la intro.
- Una cabecera pesa 80 B y una transacción media pesa ≥250 B, así que un bloque es del orden de mil veces más grande que su cabecera. Satoshi calcula que guardar solo cabeceras ocupa 80 B × 6 × 24 × 365 ≈ **4,2 MB por año**.

### 1.5 Árbol de Merkle (Ralph Merkle, 1979/1989)

- **Construcción:** se hashea cada transacción (hojas), se concatenan de dos en dos y se hashean, y así hasta llegar a una sola **raíz**. Si un nivel tiene un número impar de nodos, Bitcoin **duplica el último**.
- **Para qué sirve (Stanford CS251, Boneh):** es un **compromiso** (*commitment*) corto y vinculante con una lista. Basta escribir 32 B en la cabecera para comprometerse con miles de transacciones, y después se puede **probar** que cualquiera de ellas está incluida.
- **Prueba de inclusión:** para probar que la transacción *i* está en el bloque, basta dar sus **hermanos** en el camino hasta la raíz: **log₂(n) hashes**.

| Transacciones | Hashes en la prueba | Tamaño aprox. |
|---|---|---|
| 8 | 3 | 96 B |
| 4 096 | 12 | 384 B |
| 1 000 000 | 20 | 640 B |

- **SPV (sección 8 del whitepaper):** una billetera ligera (el celular) guarda solo las cabeceras y pide la *rama de Merkle* de su transacción. No descarga gigas de bloques.
- **Detección de cambios:** si cambias una transacción, cambia su hoja, luego todo el camino hasta la raíz, luego la cabecera y su hash, y el siguiente bloque deja de coincidir. **Toda la cadena posterior queda inválida.**
- **Matiz importante (te hace quedar muy bien):** la estructura hace las alteraciones **evidentes**, no **imposibles**. Un atacante podría recalcular todo. Lo que lo vuelve impracticable es el **consenso** (rehacer el trabajo de todos los bloques siguientes más rápido que la red). Ahí le pasas la palabra al Integrante 6.

### 1.6 Ángulo de seguridad (bonus para la materia, 30 s o para preguntas)

- **CVE-2012-2459 (maleabilidad del árbol de Merkle):** la regla "duplicar el último nodo si el número es impar" permitía construir **otra lista de transacciones con la misma raíz** (repitiendo una transacción). Un nodo podía marcar como inválido un bloque legítimo y quedarse en otra bifurcación. Se corrigió en 2012 rechazando bloques con transacciones duplicadas, y no se conoce que se haya explotado.
- **Ataque de segunda preimagen (nodo interno haciéndose pasar por hoja):** la raíz no codifica la profundidad del árbol. Defensa: **separación de dominio** con un prefijo `0x00` para hojas y `0x01` para nodos internos, como en Certificate Transparency (RFC 6962).
- **Lección para la materia:** incluso con un hash perfecto, **el diseño de la estructura** puede abrir vulnerabilidades.

---

## 2. Guion + storyboard (clip por clip)

> ⚠️ **Obsoleto.** El guion vigente (7 min, 28 beats, blockchain en general) es [guion_integrante3.md](guion_integrante3.md). Esta sección queda como referencia de la versión anterior.

**Técnica para que todo vaya sincronizado:** cada clip es **un beat** de lo que dices. En Canva, cada clip va en **su propia diapositiva**, con *autoplay* y sin transición. El **último fotograma de un clip es idéntico al primero del siguiente**, así al avanzar parece una sola animación continua que tú controlas con el clicker. Cada clip termina en una pose quieta (*hold*), así que si hablas más, la imagen espera.

Leyenda: 🎬 = lo que muestra el clip · 🗣️ = lo que dices (guía, no para memorizar literal).

### A. El ledger (≈1:45)

**A1 · El cuaderno compartido** (~12 s)
- 🎬 Aparecen Alice, Bob y Carol. Al centro, un cuaderno vacío con el título "Ledger". Se escriben líneas una a una: `Alice → Bob: 5`, `Bob → Carol: 2`, `Carol → Alice: 1`.
- 🗣️ "Imaginen que Alice, Bob y Carol se prestan dinero. En lugar de confiar en la memoria, lo anotan todo en un cuaderno compartido. Cada línea es un movimiento."

**A2 · Los saldos no se guardan, se calculan** (~12 s)
- 🎬 Al lado aparece "Saldo inicial: Alice 10". Un cursor recorre las líneas y los contadores de saldo se actualizan en vivo (Alice 10→5→6, Bob 0→5→3, Carol 0→2→1).
- 🗣️ "Fíjense que el cuaderno no guarda saldos. Para saber cuánto tiene Bob, se lee la historia desde el inicio. Así funciona Bitcoin: el saldo es una consecuencia del historial."

**A3 · Solo se puede agregar** (~10 s)
- 🎬 Una goma intenta borrar `Alice → Bob: 5`: aparece una ✗ roja y la línea vuelve. Abajo se agrega una línea nueva. Aparece la definición: **Ledger = registro ordenado de transacciones al que solo se puede agregar.**
- 🗣️ "Regla de oro: no se borra ni se edita. Si hubo un error, se agrega una transacción que lo corrija. Esto es un **ledger**."

**A4 · ¿Quién guarda el cuaderno?** (~15 s)
- 🎬 El cuaderno se copia en 5 nodos (enlaza con el "Replicated Ledger" de la intro). Luego Alice, con saldo 5, envía `Alice → Bob: 5` a la izquierda y `Alice → Carol: 5` a la derecha. Dos copias quedan con **órdenes distintos** y aparece un ⚠️ **Doble gasto**.
- 🗣️ "Como vimos en la intro, todos tienen una copia. Pero aparece un problema: si Alice manda el mismo dinero a dos personas a la vez, ¿cuál vale? Satoshi lo dice claro: necesitamos que todos acuerden **un único historial del orden**. Para eso necesitamos estructura."

### B. La transacción (≈0:45)

**B1 · Anatomía de una transacción** (~15 s)
- 🎬 Zoom a una línea, que se convierte en una tarjeta con campos **De · Para · Monto · Firma**. Debajo, `ID = hash(tx)` con un **hash SHA-256 real**. Luego el monto cambia de 5 a 50 y el ID cambia por completo (se resaltan los caracteres distintos).
- 🗣️ "Una línea del cuaderno es una **transacción**: quién paga, a quién, cuánto, y la firma que vimos con mi compañero. Su identificador es su hash: cambias un número y la huella es otra. Ya no se puede alterar una transacción sin que se note."

### C. De transacciones a bloques (≈1:00)

**C1 · La lluvia de transacciones** (~15 s)
- 🎬 Desde los nodos llegan muchas tarjetas pequeñas a una zona de "pendientes" (*mempool*). Un intento de ordenarlas una por una muestra un contador de "rondas de acuerdo" que se dispara. Luego las tarjetas se agrupan en un bloque que se cierra: **Bloque = lote de transacciones**.
- 🗣️ "En Bitcoin llegan miles de transacciones por minuto. Ponerse de acuerdo una por una entre nodos de todo el planeta sería imposible. La solución: agruparlas en lotes. Cada lote es un **bloque**, y la red acuerda bloque por bloque, más o menos cada 10 minutos."

**C2 · Cuaderno, página, línea** (~12 s)
- 🎬 Tres columnas que se animan: 📒 Ledger = cuaderno, 📄 Bloque = página, ✏️ Transacción = línea. Luego aparece **la misma cadena en zigzag de la diapositiva "Blockchain" de la intro** (5 cubos de alambre, línea punteada que entra desde la izquierda, "Hash Previo" bajo cada cubo y la frase "Cada bloque referencia criptográficamente al anterior."), ahora con hashes reales.
- 🗣️ "Si el ledger es el cuaderno, el bloque es una página y la transacción una línea. El ledger es toda la historia; el bloque es la unidad en que se agrega y se sella. Y cada página apunta a la anterior, la cadena que vieron en la intro. Ahora abramos una página."

### D. Estructura del bloque (≈1:00)

**D1 · Abrir el bloque** (~15 s)
- 🎬 Un cubo de la cadena se abre en dos partes: **Cabecera** arriba (6 campos con su tamaño en bytes, total 80 B) y **Cuerpo** abajo (lista de transacciones). Se resaltan `Hash anterior` (enlace hacia atrás) y `Raíz de Merkle`.
- 🗣️ "Un bloque tiene dos partes. El **cuerpo**, con las transacciones. Y la **cabecera**, de solo 80 bytes: versión, hash del bloque anterior (que forma la cadena), raíz de Merkle, la hora, y dos campos de minería que explicará mi compañero."

**D2 · ¿Qué protege el hash del bloque?** (~12 s)
- 🎬 La cabecera pasa por `SHA-256²` y sale el **hash del bloque** (real). El cuerpo queda gris y aparece la pregunta: **¿y las transacciones?** El campo "Raíz de Merkle" parpadea.
- 🗣️ "El hash del bloque se calcula **solo con la cabecera**. Entonces, ¿quién protege las transacciones? La respuesta está en un campo: la raíz de Merkle."

### E. Árbol de Merkle (≈1:45)

**E1 · Construir el árbol** (~18 s)
- 🎬 Cuatro transacciones abajo. Cada una baja a su hash (hoja). Se combinan de a pares, `H(H₁‖H₂)`, nivel por nivel, hasta la **raíz**. La raíz vuela al campo de la cabecera. Todos los hashes son reales y abreviados a 4 caracteres.
- 🗣️ "Se hashea cada transacción. Luego se juntan de dos en dos y se vuelven a hashear, hasta que queda uno solo: la **raíz de Merkle**. Esos 32 bytes resumen todas las transacciones, sean 4 o 4 000."

**E2 · Intento de manipulación** (~18 s)
- 🎬 Un atacante cambia `Bob → Carol: 2` por `20`. La hoja se pone roja, el camino sube en rojo hasta la raíz, la cabecera cambia y el hash del bloque cambia. En el **siguiente bloque**, su `hash anterior` ya no coincide: el enlace se rompe con un chispazo y todos los bloques posteriores quedan en rojo.
- 🗣️ "¿Qué pasa si alguien cambia un 2 por un 20? Cambia su hash, luego la raíz, luego el hash del bloque… y el siguiente bloque ya no reconoce a su padre. Una sola cifra rompe toda la cadena posterior. Ojo: esto hace la trampa **evidente**, no imposible. Lo que la vuelve impracticable es el consenso, que verá mi compañero."

**E3 · Prueba de inclusión** (~18 s)
- 🎬 Un celular pregunta: "¿mi pago está en el bloque?". Se ilumina una hoja y solo sus **hermanos** en el camino (3 hashes para 8 transacciones). Se recalcula la raíz y aparece ✓. Luego un contador: 8 → 3 hashes · 4 096 → 12 · 1 000 000 → 20.
- 🗣️ "Y aquí está la magia: para probar que mi transacción está en un bloque, no necesito todas las demás, solo un camino de hashes. Con un millón de transacciones bastan 20. Así funcionan las billeteras del celular: guardan solo cabeceras."

### F. Cierre (≈0:20, diapositiva estática en Canva)

- Resumen en una línea: **línea → transacción → página/bloque → cabecera + Merkle → cadena.**
- 🗣️ "Un blockchain es un cuaderno donde solo se agrega, organizado en páginas selladas, cada una resumida por un árbol de Merkle y enlazada a la anterior. Cualquier cambio se nota. Pero, ¿quién decide qué página se agrega? Eso lo explica [Integrante 6]…" *(o el siguiente en el orden real)*

### Diapositiva opcional (preguntas): seguridad del árbol de Merkle

CVE-2012-2459 y separación de dominio (§1.6). Sin animación, solo texto.

---

## 3. Preguntas probables y respuestas cortas

| Pregunta | Respuesta |
|---|---|
| ¿Por qué no hashear todas las transacciones juntas en vez de usar un árbol? | Funcionaría para detectar cambios, pero para probar que **una** está incluida tendrías que entregar todas. El árbol permite pruebas de log₂(n). |
| ¿Si la cabecera no tiene las transacciones, cómo se protegen? | La raíz de Merkle está en la cabecera; cambiar una transacción cambia la raíz y por lo tanto el hash del bloque. |
| ¿Entonces es imposible modificar un blockchain? | No: es **evidente**. Hacerlo impracticable depende del consenso (PoW/PoS). |
| ¿Dónde está mi saldo en Bitcoin? | En ningún lado como número: es la suma de tus UTXO (salidas no gastadas). |
| ¿Qué pasa si hay un número impar de transacciones? | Bitcoin duplica la última. Esto causó el CVE-2012-2459. |
| ¿Cuánto pesa la cadena si solo guardo cabeceras? | ~4,2 MB por año (80 B × 6 bloques/h × 24 × 365). |

---

## 4. Especificación técnica de los clips

- **Formato:** MP4 H.264, 1920×1080, 30 fps, sin audio, más un PNG del último fotograma (respaldo si falla el video).
- **Paleta (muestreada del Canva):** fondo `#1E2124`, acento amarillo `#E6E924`, texto `#F2F2F2`, gris `#8A8F98`, error `#FF5A5F`, ok `#3DDC84`.
- **Tipografía:** Montserrat (texto) + JetBrains Mono (hashes).
- **Datos:** todos los hashes salen del módulo `ledger_viz.domain`, con SHA-256 real y probado. Nada inventado.
- **Continuidad:** cada escena construye su estado inicial con la misma función que generó el estado final de la anterior.

## 5. Fuentes

- Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System*, §2, 3, 7, 8. https://bitcoin.org/bitcoin.pdf
- Boneh, D. — Stanford CS251, *Blockchain Technologies*, lecture 1 (Merkle commitments). https://securitylab.github.io/cs251-fall23/lectures/lecture1.pdf · https://cs251.stanford.edu
- Narayanan et al. — *Bitcoin and Cryptocurrency Technologies* (Princeton), cap. 1: hash pointers y árboles de Merkle. https://bitcoinbook.cs.princeton.edu
- Antonopoulos, A. — *Mastering Bitcoin*, cap. "The Blockchain". https://oreilly.com/library/view/mastering-bitcoin/9781491902639/ch07.html
- NIST IR 8202 (2018), *Blockchain Technology Overview*. https://doi.org/10.6028/NIST.IR.8202 · glosario: https://csrc.nist.gov/glossary/term/block_header
- Gensler, G. — MIT 15.S12 *Blockchain and Money*, sesión 3.
- Haber, S. y Stornetta, W. S. (1991). *How to Time-Stamp a Digital Document*. Journal of Cryptology.
- 3Blue1Brown — *But how does bitcoin actually work?* https://www.3blue1brown.com/lessons/bitcoin
- Brownworth, A. — *Blockchain 101: A Visual Demo*. https://anders.com/blockchain
- Bitcoin Optech — *Merkle tree vulnerabilities* (CVE-2012-2459). https://bitcoinops.org/en/topics/merkle-tree-vulnerabilities/
- RFC 6962 — Certificate Transparency (separación de dominio en árboles de Merkle).

## 6. Cómo montar los clips en Canva

1. Genera los clips con `make clips`. Salen en `renders/`: `01_A1_cuaderno.mp4` … `12_E3_prueba_inclusion.mp4`, cada uno con su `.png` (último fotograma).
2. En Canva crea **una diapositiva por clip**, en el mismo orden. Sube el MP4 y estíralo a pantalla completa (1920×1080, mismo fondo `#1E2124`).
3. En cada video: **Reproducción automática** activada, **sin bucle** y **sin transición** entre diapositivas. Así cada clip arranca donde terminó el anterior.
4. Respaldo: si en la sala falla el video, reemplázalo por el `.png` del mismo número, que muestra el estado final.
5. Ensayo: avanza solo cuando terminaste la frase del 🗣️ correspondiente. El clip queda quieto al final, así que no hay apuro.
