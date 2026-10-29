"""Genera el sitio estático con los resultados de las consultas."""

import html
from datetime import UTC, datetime
from pathlib import Path


def _celda(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return html.escape(str(v))


def tabla(columnas, filas):
    encabezado = "".join(f"<th>{html.escape(c)}</th>" for c in columnas)
    cuerpo = "".join(
        "<tr>" + "".join(f"<td>{_celda(v)}</td>" for v in f) + "</tr>" for f in filas
    )
    return f'<div class="tabla"><table><thead><tr>{encabezado}</tr></thead><tbody>{cuerpo}</tbody></table></div>'


def generar(resultados, destino: Path, plantilla: Path):
    secciones = []
    for r in resultados:
        secciones.append(
            f"""<section><h2>{html.escape(r["titulo"])}</h2>
{tabla(r["columnas"], r["filas"])}
<details><summary>Ver SQL</summary><pre><code>{html.escape(r["sql"])}</code></pre></details></section>"""
        )
    fecha = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    contenido = plantilla.read_text(encoding="utf-8").replace(
        "{{SECCIONES}}", "\n".join(secciones)
    )
    contenido = contenido.replace("{{GENERADO}}", fecha)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(contenido, encoding="utf-8")
