# Integrante 3 — Estructura de datos y Ledger · Guion de 7 minutos

> Va después de **Integrante 2 (criptografía)**. Ritmo de cálculo: **2,4 palabras/s** (el mismo que la intro).
> Cada **beat** = una diapositiva en Canva con su clip. La animación dura lo que tardas en decir el texto y después **se queda quieta**: si vas lento, espera; si terminas, haces clic.
> 🗣️ = lo que dices (estilo conversacional, no hace falta literal) · 🎬 = lo que se ve · **negrita** = palabra que enfatizas.

## Mapa de tiempos

| § | Tema | Beats | Inicia |
|---|---|---|---|
| 0 | Puente desde criptografía | 2 | 0:00 |
| 1 | El ledger (Alice, Bob y Carol) | 5 | 0:30 |
| 2 | La transacción | 3 | 1:50 |
| 3 | De transacciones a bloques | 3 | 2:29 |
| 4 | La cadena: del dibujo a la estructura de datos | 4 | 3:06 |
| 5 | Estructura del bloque | 3 | 3:58 |
| 6 | Árbol de Merkle | 6 | 4:32 |
| 7 | Cierre | 2 | 6:01 |
| | **Total** | **28** | **6:28 de habla** |

6:28 de habla más unos 30 s de pausas y clics dan **≤ 7:00**. Si al ensayar te pasas, recorta 2.2 (UTXO) y 6.2 (impar): son los beats más técnicos y prescindibles (≈ 25 s).

---

## 0 · Puente desde criptografía

**0.1 · ¿Dónde se usan el hash y la firma?** · ⏱ 15 s (35 palabras)
- 🗣️ "Mi compañera nos mostró dos herramientas: el **hash**, la huella digital de cualquier dato, y la **firma digital**, que prueba quién autorizó algo. Pero ¿dónde se usan? ¿Qué guarda un blockchain y **cómo lo organiza**?"
- 🎬 Título "Estructura de datos y Ledger". Entran dos íconos de la parte de cripto: huella (hash) y pluma (firma). Se desplazan hacia un cubo de alambre con un "?" adentro.

**0.2 · Hoja de ruta y tesis** · ⏱ 15 s (37 palabras)
- 🗣️ "Lo veremos en cuatro pasos: **ledger**, **transacción**, **bloque** y **árbol de Merkle**. Y quédense con esta idea: un blockchain es un cuaderno al que **solo se puede agregar**, y su estructura hace que **cualquier alteración se note**."
- 🎬 Cuatro pasos en fila (ícono + nombre) que se encienden uno por uno. Abajo aparece la frase-tesis.

## 1 · El ledger

**1.1 · El cuaderno compartido** · ⏱ 17 s (41 palabras)
- 🗣️ "Empecemos con algo cotidiano. Alice, Bob y Carol llevan sus cuentas en un cuaderno compartido. Alice empieza con 10 monedas. Luego anotan: Alice le paga 5 a Bob, Bob le paga 2 a Carol y Carol le devuelve 1 a Alice."
- 🎬 Los tres personajes a la izquierda y un cuaderno al centro. Cada línea se escribe **en el momento en que la dices** (aprox. una cada 3 s).

**1.2 · Los saldos no se guardan, se calculan** · ⏱ 14 s (34 palabras)
- 🗣️ "Fíjense: **no hay columna de saldos**. ¿Cuánto tiene Bob? Recorremos el historial: recibió 5, pagó 2, le quedan 3. El saldo no se guarda, **se calcula**. Bitcoin hace lo mismo: guarda transacciones, no saldos."
- 🎬 Panel "SALDOS". Un cursor baja línea por línea y los números cambian. Al final se resalta "Bob: 3".

**1.3 · Solo se puede agregar → definición** · ⏱ 15 s (37 palabras)
- 🗣️ "Regla de oro: aquí **no se borra**. Si hay un error, se agrega una línea que lo corrige. Eso es un **ledger**, o libro mayor: un registro **ordenado** de transacciones al que **solo se puede agregar**, *append-only*."
- 🎬 Una goma intenta borrar una línea, tiembla y sale una ✗. Se agrega una línea nueva abajo. Aparece la tarjeta de definición con "append-only" en amarillo.

**1.4 · Replicado → el problema** · ⏱ 16 s (39 palabras)
- 🗣️ "Pero en blockchain **cada nodo guarda su propia copia**. Y aparece un problema: Alice, con 10 monedas, envía a la vez 7 a Bob por un lado y 7 a Carol por otro. Cada mensaje parece válido. ¿Cuál cuenta?"
- 🎬 El cuaderno se copia en 5 nodos. Alice, abajo, envía dos mensajes en direcciones opuestas. El nodo del centro recibe ambos y muestra un "?".

**1.5 · Doble gasto → orden único** · ⏱ 17 s (40 palabras)
- 🗣️ "Es el **doble gasto** que quedó abierto en la introducción. Parte de la solución es estructural: si todos tienen las transacciones **en el mismo orden**, la segunda llega tarde y se rechaza por falta de fondos. Necesitamos un **orden único**."
- 🎬 Aparece "⚠ DOBLE GASTO". Las dos transacciones se colocan en una sola fila numerada: la 1.ª ✓ (saldo 10 → 3) y la 2.ª ✗ "fondos insuficientes". Queda una caja: "Orden único".

## 2 · La transacción

**2.1 · Qué contiene** · ⏱ 15 s (36 palabras)
- 🗣️ "Veamos qué es una transacción: un mensaje con formato fijo: **de quién, para quién, cuánto** y una **firma digital**. Como explicó mi compañera, la firma prueba que fue Alice, y nadie más, quien autorizó el pago."
- 🎬 Una línea del cuaderno se agranda hasta convertirse en una tarjeta. Los campos De / Para / Monto / Firma aparecen uno por uno. La firma se resalta con un ícono de llave y el texto "solo Alice puede generarla".

**2.2 · Por dentro (Bitcoin): entradas y salidas** · ⏱ 12 s (28 palabras)
- 🗣️ "En Bitcoin, además, una transacción **consume salidas** de transacciones anteriores, sus **entradas**, y **crea salidas nuevas** para quien recibe. Así cada moneda se puede rastrear hasta su origen."
- 🎬 Diagrama: a la izquierda "salida anterior: 10 → Alice" entra a la tarjeta de la transacción. A la derecha salen "5 → Bob" y "5 → Alice (cambio)". Una flecha punteada vuelve a la transacción anterior ("de dónde vino").

**2.3 · Su identidad es su hash (txid)** · ⏱ 12 s (30 palabras)
- 🗣️ "¿Cómo la identificamos? **Con su hash**: SHA-256 aplicado **dos veces**, el *txid*. Si alguien cambia el monto de 5 a 50, el identificador cambia **por completo**. Ya es otra transacción."
- 🎬 Debajo de la tarjeta: "txid = SHA-256(SHA-256(tx))" y 16 caracteres reales. El 5 cambia a 50 y se marcan en rojo todos los caracteres del txid que cambiaron.

## 3 · De transacciones a bloques

**3.1 · La mempool y el cuello de botella** · ⏱ 10 s (23 palabras)
- 🗣️ "Volvamos al orden. Las transacciones nuevas esperan en una sala llamada **mempool**. Ponerse de acuerdo sobre cada una, **una por una**, sería lentísimo."
- 🎬 Desde los nodos llegan tarjetas pequeñas a una zona punteada "mempool". Un contador "rondas de acuerdo" sube y se pone rojo.

**3.2 · La solución: agrupar** · ⏱ 14 s (34 palabras)
- 🗣️ "La solución es **agrupar**: se acuerda un paquete completo de una vez. Ese paquete es un **bloque**. En Bitcoin se agrega uno **cada diez minutos** aproximadamente, con **tamaño limitado**: unos pocos miles de transacciones."
- 🎬 Las tarjetas entran a un cubo. El contador baja a "1". Aparecen "1 bloque = 1 acuerdo" y "Bitcoin: ≈ 10 min · tamaño limitado · miles de tx".

**3.3 · Ledger vs. bloque** · ⏱ 13 s (32 palabras)
- 🗣️ "¿Ledger o bloque? El **ledger es el cuaderno completo**, el **bloque es una página** y la **transacción una línea**. El ledger es el registro; el bloque, la unidad con la que crece."
- 🎬 Tres columnas que se encienden en orden: cuaderno = Ledger, página = Bloque, línea = Transacción. Debajo: "registro" frente a "unidad de crecimiento".

## 4 · La cadena: del dibujo a la estructura de datos

**4.1 · La imagen de la intro** · ⏱ 8 s (18 palabras)
- 🗣️ "Recuerdan esta imagen de la introducción: bloques unidos por una línea. Pero ¿qué es **esa línea** en realidad?"
- 🎬 **El zigzag del Canva**: 5 cubos amarillos de alambre, línea punteada que entra desde la izquierda y "Hash Previo" debajo de cada cubo. Las líneas punteadas parpadean y aparece un "?" sobre una de ellas.

**4.2 · Se transforma en estructura de datos** · ⏱ 14 s (33 palabras)
- 🗣️ "Veámoslo como **estructura de datos**. Cada bloque guarda su **propio hash**, su huella, y un campo llamado **hash previo**. Al crear un bloque nuevo, el hash del anterior **se copia** en ese campo."
- 🎬 Los cubos se aplanan y se reordenan en una fila horizontal de 4 cajas. Cada caja tiene "Bloque n", la fila "Hash previo: ____" y la fila "Hash: 7A3F…". **El hash del bloque 1 sale volando con una flecha y se escribe en el "Hash previo" del bloque 2.** Lo mismo de 2 a 3 y de 3 a 4.

**4.3 · Puntero de hash** · ⏱ 17 s (41 palabras)
- 🗣️ "Esa línea **no es un cable, es un dato**: un **puntero de hash**. Como en una lista enlazada, cada bloque apunta al anterior, pero el puntero dice **dónde** está y también **cómo era exactamente**. Si el anterior cambia, ya no coincide."
- 🎬 Desde cada campo "Hash previo" sale una flecha curva hacia el bloque anterior, con la etiqueta "apunta a". Abajo se ve la ecuación "puntero de hash = dónde está + cómo era". Los valores que coinciden se iluminan en pares del mismo color.

**4.4 · Génesis y crecimiento** · ⏱ 14 s (34 palabras)
- 🗣️ "El primer bloque no tiene anterior: su hash previo es **todo ceros**. Es el **bloque génesis**; el de Bitcoin es del **3 de enero de 2009**. Desde ahí, la cadena **solo crece hacia adelante**."
- 🎬 El bloque 1 cambia su etiqueta a "Génesis" y muestra "Hash previo: 0000…0000" y "3-ene-2009". Por la derecha entra el bloque 5, que copia el hash del 4. La fila se desliza para hacerle espacio.

## 5 · Estructura del bloque

**5.1 · Abrir el bloque** · ⏱ 8 s (18 palabras)
- 🗣️ "**Abramos un bloque.** Tiene una **cabecera** de exactamente **80 bytes** y un **cuerpo** con la lista de transacciones."
- 🎬 Una caja de la fila crece al centro y se divide en "CABECERA · 80 bytes" arriba y "CUERPO · 8 transacciones" abajo.

**5.2 · Los 6 campos** · ⏱ 17 s (40 palabras)
- 🗣️ "La cabecera tiene seis campos. **Versión**: qué reglas sigue. **Hash previo**: el enlace que vimos. **Raíz de Merkle**: el resumen de las transacciones. **Marca de tiempo**. Y **dificultad** y **nonce**, que son de la minería y se verán en consenso."
- 🎬 Cada fila se ilumina **cuando la nombras**, con su tamaño (4 · 32 · 32 · 4 · 4 · 4 bytes) y su valor real. "Dificultad" y "nonce" llevan la etiqueta "→ consenso".

**5.3 · El hash solo cubre la cabecera** · ⏱ 10 s (24 palabras)
- 🗣️ "Detalle clave: el hash del bloque se calcula **solo con esos 80 bytes** de cabecera, con SHA-256 doble. Entonces, ¿qué protege a las transacciones?"
- 🎬 La cabecera entra a una caja "SHA-256²" y sale el hash del bloque. El cuerpo se atenúa con un "?" grande. La fila "Raíz de Merkle" parpadea.

## 6 · Árbol de Merkle

**6.1 · Construcción** · ⏱ 15 s (37 palabras)
- 🗣️ "La respuesta es el **árbol de Merkle**. Calculamos el hash de cada transacción: las **hojas**. Unimos los hashes **de dos en dos** y volvemos a calcular el hash, nivel por nivel, hasta que queda uno: la **raíz**."
- 🎬 Ocho transacciones abajo. Las hojas aparecen primero y luego cada nivel **al ritmo de la frase**, con la fórmula "H(a ‖ b)" a un lado. La raíz brilla.

**6.2 · Impar y raíz en la cabecera** · ⏱ 10 s (25 palabras)
- 🗣️ "Si un nivel es impar, se **duplica el último**. Y esa raíz, de **32 bytes**, va en la cabecera: resume **todas** las transacciones sin contenerlas."
- 🎬 Mini-ejemplo de 3 hojas en el que la 3.ª se duplica (en gris). La raíz del árbol grande vuela a la fila "Raíz de Merkle" de la cabecera.

**6.3 · Seamos el atacante** · ⏱ 15 s (35 palabras)
- 🗣️ "**Seamos el atacante**: cambiamos el pago de Bob a Carol de 2 a **20**. Cambia su hash, el de su par, y así hasta la raíz. Cambia la cabecera y cambia **el hash del bloque**."
- 🎬 "B→C:2" pasa a "B→C:20" en rojo. El camino sube en rojo, nodo por nodo, con los hashes reales nuevos. La raíz, la cabecera y el hash del bloque se ponen rojos.

**6.4 · La cadena se rompe** · ⏱ 21 s (50 palabras)
- 🗣️ "Y el bloque siguiente guardaba el hash anterior, que **ya no coincide**: la cadena se rompe, y cualquier nodo lo detecta comparando un valor. Para ocultarlo habría que rehacer ese bloque **y todos los siguientes**. La estructura no lo hace imposible, lo hace **evidente**; lo impracticable lo pone el consenso."
- 🎬 Vuelve la **fila de estructura de datos** (la de §4). El hash del bloque alterado muestra el valor nuevo real. El "Hash previo" del bloque siguiente queda con el valor viejo, se marca en rojo con "≠" y la flecha se parte con una ✗. Los bloques siguientes se ponen rojos. Al final aparece "evidente ≠ imposible → consenso".

**6.5 · Prueba de inclusión** · ⏱ 17 s (41 palabras)
- 🗣️ "Segundo superpoder: Dave, desde su celular, quiere saber si su pago está en el bloque **sin descargarlo**. Le bastan su transacción y **tres hashes**, los hermanos en el camino a la raíz. Recalcula la raíz y la compara con la cabecera."
- 🎬 Un celular pregunta "¿«A→D:2» está?". Se resalta la hoja. Los 3 hermanos se marcan en verde y numerados. El camino sube en amarillo hasta la raíz y aparece ✓ "coincide con la cabecera".

**6.6 · Escala logarítmica** · ⏱ 10 s (25 palabras)
- 🗣️ "Y escala: con ocho transacciones, **3** hashes; con un millón, solo **20**. Satoshi lo llamó **verificación simplificada de pagos**, y así funcionan las billeteras ligeras."
- 🎬 Tabla animada: 8 → 3 · 4 096 → 12 · 1 000 000 → 20 (log₂ n). Al lado: "SPV · billeteras ligeras: solo cabeceras, 80 B por bloque".

## 7 · Cierre

**7.1 · El viaje completo** · ⏱ 14 s (34 palabras)
- 🗣️ "En resumen: las transacciones, **firmadas** e **identificadas por su hash**, se agrupan en **bloques**; **Merkle** las resume en la cabecera; y el hash de cada cabecera va **en el siguiente bloque**, formando la cadena."
- 🎬 Un pipeline horizontal que se recorre de izquierda a derecha: transacción (firma + txid) → bloque → Merkle → cabecera → cadena enlazada.

**7.2 · Tesis y relevo** · ⏱ 12 s (29 palabras)
- 🗣️ "Un blockchain es un cuaderno **al que solo se puede agregar**, donde **cualquier alteración se nota**. Falta saber **quién decide qué bloque entra**: eso lo veremos con el consenso."
- 🎬 Vuelve la frase-tesis de 0.2 junto a la cadena enlazada. Un bloque nuevo llega con un "?" encima: "¿quién decide? → consenso".
- ✏️ Adapta la última frase al nombre de quien hable después de ti.

---

## Fuentes de los datos técnicos que dices

| Dato | Fuente |
|---|---|
| Ledger append-only, replicado y *tamper evident* | NIST IR 8202, *Blockchain Technology Overview* (2018) |
| Doble gasto y necesidad de un orden único | Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System* (2008), §2 |
| Entradas/salidas (UTXO) y txid = SHA-256 doble | Bitcoin Developer Guide, *Transactions* |
| Cabecera de 80 bytes y sus 6 campos; el hash cubre solo la cabecera | Bitcoin Developer Reference, *Block Headers* |
| Puntero de hash / lista enlazada | Narayanan et al., *Bitcoin and Cryptocurrency Technologies* (Princeton, 2016), cap. 1 |
| Génesis 3-ene-2009 | Bitcoin Wiki, *Genesis block* |
| Merkle: duplicar el último nodo; SPV con log₂(n) hashes | Nakamoto §7–8; Bitcoin Developer Reference, *Merkle Trees* |
