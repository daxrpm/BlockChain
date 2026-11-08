# Integrante 1 — Introducción y fundamentos

> Guion generado desde `src/ledger_viz/intro_script.py` (no editar a mano).
> Duración mínima del video: 7.3 min a 2.4 palabras/s.
> ✏️ = cambio respecto al guion original (ver motivo en el chat / README).

## 01 · El problema de confianza (portada)

Clip: `I0_blockchain_vs_bitcoin`

- El problema de confianza: ¿por qué necesitamos Blockchain? Antes de comenzar, mi grupo y yo consideramos importante aclarar algunas dudas que probablemente muchos de nosotros tenemos.
- Creo que es normal que muchas personas confundan Blockchain con Bitcoin, porque ambos términos suelen aparecer juntos.
- Pero hay algo muy importante que debemos entender: Bitcoin es una criptomoneda que utiliza la tecnología Blockchain. Es decir, Blockchain es la tecnología y Bitcoin es una criptomoneda que utiliza esa tecnología.
- Muy sencillo hasta aquí. Pero entonces, ¿por qué surgió esta tecnología y qué problema busca resolver?

## 02 · Sistema centralizado

Clip: `I1_sistema_centralizado`

- Tradicionalmente, hemos utilizado sistemas centralizados, como los que encontramos en los bancos y otras entidades financieras. ¿Qué caracteriza a un sistema centralizado? Principalmente, que existe una autoridad central que tiene el control y gestiona los datos y las operaciones del sistema.
- Pongamos un ejemplo para entenderlo mejor. Tenemos dos participantes: Alice y Bob. Alice quiere transferir dinero a Bob.
- ¿Qué sucede? Alice solicita la transferencia a su banco. El banco recibe la solicitud,
- verifica que la transacción cumpla las condiciones necesarias, autoriza la operación
- y actualiza su registro contable, es decir, su base de datos. Finalmente, Bob recibe el dinero.
- Tanto Alice como Bob dependen del banco para realizar y verificar esta operación. Entonces, ¿qué podemos concluir? En un sistema centralizado, existe una autoridad de confianza que se encarga de gestionar y validar las transacciones. Los participantes dependen de esta entidad para garantizar que las operaciones se realicen correctamente.

## 03 · El problema de confianza

Clip: `I2_problema_de_confianza`

- Ahora imaginemos que queremos realizar estas transacciones sin depender de un intermediario como un banco. ¿Por qué alguien querría hacerlo? Porque no todos los participantes necesariamente quieren depender de una única entidad para gestionar sus transacciones. Buscan poder interactuar directamente entre ellos.
- Pero aquí aparece un problema importante. Si eliminamos esa autoridad central, ¿quién se encarga de validar las transacciones? ¿Dónde se almacena el registro contable? Y, sobre todo, ¿cómo podemos confiar en el sistema si no existe una entidad central que supervise las operaciones?
- En el ejemplo anterior, Alice y Bob confían en el banco porque saben que existe una entidad responsable de verificar y registrar sus transacciones. Pero ¿cómo conseguimos esa misma confianza en un sistema descentralizado?

## 04 · Sistema descentralizado

Clip: `I3_sistema_descentralizado`

- En un sistema descentralizado, el control y la gestión se distribuyen entre múltiples participantes, que pueden operar mediante diferentes nodos de una red.
- Ya no dependemos de una única autoridad central. En lugar de mantener un registro contable bajo el control de una sola entidad, podemos tener múltiples réplicas de ese registro, conocidas como ledgers, mantenidas por los nodos participantes.
- Esto significa que diferentes nodos pueden conservar y verificar el mismo registro de transacciones, siguiendo unas reglas de protocolo compartidas.
- Volvamos al ejemplo anterior. Si Alice quiere transferir dinero a Bob, ¿cómo podríamos realizar esta operación sin acudir a un banco? ¿Quién verifica que Alice realmente tiene los fondos? ¿Cómo evitamos que intente gastar el mismo dinero dos veces?

## 05 · La aparición de Blockchain

Clip: `I4_aparicion_de_blockchain`

- Precisamente, este es el problema que Bitcoin buscó resolver. En 2008, una persona o grupo bajo el seudónimo de Satoshi Nakamoto publicó el documento técnico de Bitcoin, proponiendo un sistema de efectivo electrónico entre pares.
- La propuesta permitió realizar transferencias de valor directamente entre participantes, sin depender de una autoridad central para gestionar y validar el registro de transacciones.
- Para conseguirlo, Bitcoin introdujo un sistema que utiliza criptografía, mecanismos de consenso y una estructura de datos conocida como cadena de bloques o Blockchain.
- Posteriormente, surgieron otras criptomonedas que también utilizan esta tecnología. Pero entonces, ¿cómo funciona exactamente Blockchain? ¿Cómo consigue que diferentes participantes puedan validar y mantener un mismo registro sin depender de una autoridad central?

## 06 · Blockchain: ¿qué es y cómo se organiza?

Clip: `I5_que_es_blockchain`

- ✏️ Blockchain es una estructura de datos distribuida que almacena registros en bloques enlazados criptográficamente.
- ✏️ Cada bloque guarda una referencia, un hash, del bloque anterior. Así se forma una cadena: el primer bloque no tiene anterior, por eso su hash previo es cero. Cómo está construido cada bloque por dentro lo explicará uno de mis compañeros.

## 07 · Propiedades fundamentales

Clip: `I6_propiedades`

- ¿Qué garantías nos proporciona esta tecnología? ¿Cómo podemos confiar en que la información registrada se mantenga y que las transacciones sean válidas? Para responder a esto, vamos a explicar tres propiedades fundamentales: persistencia, seguridad y progreso.
- Primero, persistencia. ¿Qué significa esto? Significa que una vez que una transacción ha sido confirmada e incorporada a la cadena, su registro está diseñado para permanecer en ella. Recordemos que los bloques están enlazados criptográficamente. Si alguien intenta modificar información de un bloque anterior, cambiaría su hash y se rompería la correspondencia con los bloques posteriores. Esto hace que modificar el historial de transacciones sea extremadamente difícil.
- ✏️ Segundo, seguridad. Los nodos honestos no discrepan sobre los registros confirmados: todos llegan a la misma versión de la historia. Para lograrlo intervienen los mecanismos de consenso y las reglas del protocolo. Los nodos verifican que las transacciones y los bloques cumplan esas reglas antes de aceptarlos.
- Por ejemplo, si Alice intenta realizar una transacción utilizando fondos que no tiene disponibles o que ya fueron gastados, los nodos deben rechazarla. De esta manera, la red busca garantizar que los participantes mantengan un registro consistente.
- Finalmente, progreso. ¿De qué nos serviría tener un sistema seguro si nunca pudiéramos registrar nuevas transacciones? El progreso se refiere a la capacidad de la red para seguir procesando transacciones válidas e incorporándolas a nuevos bloques. La cadena no solamente conserva las transacciones anteriores, sino que también puede seguir creciendo.
- En conjunto, estas tres propiedades buscan que Blockchain pueda mantener un registro persistente, verificar la validez de las operaciones y continuar incorporando nuevas transacciones sin depender de una autoridad central.

## 08 · ¿Cómo protegemos la información?

Clip: `I8_como_protegemos`

- ✏️ Ya sabemos qué garantías buscamos de esta tecnología. Pero todavía tenemos algunas preguntas importantes.
- ¿Cómo podemos saber que Alice realmente autorizó esa transacción? ¿Cómo podemos comprobar que nadie modificó la información durante su transmisión? Y, una vez que una transacción se incorpora a un bloque, ¿cómo podemos detectar si alguien intenta alterar su contenido?
- Recordemos que en un sistema descentralizado no dependemos de una autoridad central que verifique personalmente cada operación. Entonces, ¿cómo conseguimos garantizar la autenticidad de las transacciones y la integridad de la información?
- Aquí es donde entra la criptografía. La criptografía proporciona mecanismos que permiten proteger la información, verificar la identidad y autorización de los participantes, y detectar modificaciones en los datos. Para entender cómo se consigue esto, mi compañera nos explicará los principales mecanismos de criptografía que se utilizan en Blockchain.

