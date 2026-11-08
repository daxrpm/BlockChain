# ledger-viz

Animaciones en Manim para la exposición grupal **Blockchain** (Tecnologías de Seguridad, EPN).
Parte de Integrante 3: **Estructura de datos y Ledger**.

- Guía de estudio, guion y storyboard: [`docs/guion.md`](docs/guion.md)
- Todos los hashes de las animaciones son SHA-256 reales, generados en `ledger_viz.domain` y cubiertos por tests.

## Estructura

```
src/ledger_viz/
  domain/   lógica pura y testeada: transacción, ledger, bloque (cabecera de 80 B), Merkle
  viz/      tema visual (paleta del Canva) y componentes Manim reutilizables
  scenes/   una escena por clip del storyboard (A1, A2, …)
tests/      pytest + hypothesis
renders/    entregables finales (MP4 1080p30 + PNG de respaldo) para subir a Canva
```

## Uso

```bash
make dev                              # instala dependencias con uv
make check                            # ruff + ty + pytest
make preview SCENE=s00_smoke:Smoke    # render rápido 480p
make render  SCENE=s00_smoke:Smoke    # 1080p30 + PNG a renders/
```

Requisitos: `uv`, fuentes Montserrat y JetBrains Mono instaladas.
