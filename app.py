import math
import streamlit as st

st.set_page_config(page_title="LIM - Organizaciones rectangulares", layout="wide")

MAX_OBJETOS = 80
MAX_FILAS = 20

# -----------------------------
# Estado
# -----------------------------
if "or_total_anterior" not in st.session_state:
    st.session_state.or_total_anterior = 24

if "organizaciones_encontradas" not in st.session_state:
    st.session_state.organizaciones_encontradas = []

if "intentos_sin_rectangulo" not in st.session_state:
    st.session_state.intentos_sin_rectangulo = []


# -----------------------------
# Estilo
# -----------------------------
st.markdown("""
<style>
.block-container{max-width:1220px;padding-top:1.2rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#143322 0%,#0b111c 42%,#070b12 100%);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
h1,h2,h3,p,li,span,div{color:#f8fafc}
.top{display:flex;align-items:center;border-bottom:1px solid rgba(148,163,184,.45);padding-bottom:14px;margin-bottom:24px}
.code{color:#47d147;font-weight:850;font-size:22px}.title{font-size:22px;margin-left:12px}
.step{font-size:32px;font-weight:850;margin-top:24px;margin-bottom:18px}
.info{border:1px solid rgba(71,209,71,.55);background:rgba(21,128,61,.26);border-radius:10px;padding:18px 22px;font-size:19px;margin:18px 0}
.info .num{color:#47d147;font-weight:900}
.card{border:1px solid rgba(148,163,184,.38);background:rgba(2,6,23,.38);border-radius:10px;padding:14px;overflow-x:auto;min-height:120px;margin-bottom:14px}
.main{border:2px solid rgba(71,209,71,.85)}
.btitle{font-size:24px;font-weight:850;margin-bottom:14px}
.objects{display:inline-flex;flex-direction:column;gap:5px;align-items:flex-start}.row{display:flex;gap:5px}
.sq{display:inline-block;width:22px;height:22px;border-radius:3px;flex:0 0 auto}
.greenSq{background:#47d147;border:2px solid #15803d}.redSq{background:#ef4444;border:2px solid #b91c1c}
.explain{border:1px solid rgba(71,209,71,.5);background:rgba(21,128,61,.26);border-radius:10px;padding:18px 22px;margin-top:18px;font-size:20px}
.etitle{color:#facc15;font-size:24px;font-weight:900;margin-bottom:8px}.note{color:#cbd5e1;font-size:16px;font-style:italic;margin-top:12px}
.summary{display:grid;grid-template-columns:1fr .15fr 1fr .15fr 1fr .15fr 1fr;gap:14px;align-items:center;border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.58);border-radius:12px;padding:18px;margin:18px 0}
.box{border-radius:10px;padding:12px;text-align:center;background:rgba(2,6,23,.36)}.bt{border:1px solid #2f80ed}.bf{border:1px solid #47d147}.bc{border:1px solid #f2b705}.br{border:1px solid #ef4444}
.label{font-size:18px}.n{font-size:32px;font-weight:900}.blue{color:#2f80ed}.green{color:#47d147}.yellow{color:#f2b705}.red{color:#ef4444}.op{font-size:28px;font-weight:800;text-align:center}
.gallery{font-size:22px;font-weight:850;margin-top:18px;margin-bottom:10px}
.notebook{border:1px solid rgba(250,204,21,.55);background:rgba(113,63,18,.28);border-radius:12px;padding:18px;margin-top:18px}
.notebook h3{color:#facc15;margin-top:0}
.badge-ok{color:#86efac;font-weight:800}
.badge-no{color:#fca5a5;font-weight:800}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Funciones
# -----------------------------
def divisores(n: int) -> list[int]:
    return [k for k in range(1, n + 1) if n % k == 0]


def pares_rectangulares(n: int) -> list[tuple[int, int]]:
    return [(d, n // d) for d in divisores(n) if d <= n // d]


def normalizar_par(filas: int, columnas: int) -> tuple[int, int]:
    return (min(filas, columnas), max(filas, columnas))


def step(n: int, txt: str):
    st.markdown(f"<div class='step'>{n}. {txt}</div>", unsafe_allow_html=True)


def rect_html(filas: int, columnas: int, color: str = "green") -> str:
    cls = "greenSq" if color == "green" else "redSq"
    html = "<div class='objects'>"
    for _ in range(filas):
        html += "<div class='row'>"
        for _ in range(columnas):
            html += f"<span class='sq {cls}'></span>"
        html += "</div>"
    html += "</div>"
    return html


def fuera_html(n: int) -> str:
    if n == 0:
        return "<span style='color:#86efac;font-weight:800;'>No quedaron objetos fuera del rectángulo.</span>"
    return rect_html(1, n, "red")


def summary(total: int, filas: int, columnas: int, fuera: int):
    st.markdown(f"""
    <div class="summary">
      <div class="box bt"><div class="label">Objetos totales</div><div class="n blue">{total}</div></div>
      <div class="op">=</div>
      <div class="box bf"><div class="label">Filas</div><div class="n green">{filas}</div></div>
      <div class="op">×</div>
      <div class="box bc"><div class="label">Columnas</div><div class="n yellow">{columnas}</div></div>
      <div class="op">+</div>
      <div class="box br"><div class="label">Fuera</div><div class="n red">{fuera}</div></div>
    </div>""", unsafe_allow_html=True)


def rect_card(f: int, c: int, total: int, main: bool = False):
    klass = "card main" if main else "card"
    st.markdown(f"""<div class="{klass}"><b>{f} × {c} = {total}</b><br><br>{rect_html(f,c)}</div>""", unsafe_allow_html=True)
    if f != c:
        st.caption(f"Si lo giramos, también podemos verlo como {c} × {f}.")


def registrar_exploracion(total: int, filas: int, columnas: int, fuera: int):
    if fuera == 0:
        par = normalizar_par(filas, columnas)
        if par not in st.session_state.organizaciones_encontradas:
            st.session_state.organizaciones_encontradas.append(par)
    else:
        if filas not in st.session_state.intentos_sin_rectangulo:
            st.session_state.intentos_sin_rectangulo.append(filas)


def reiniciar_cuaderno():
    st.session_state.organizaciones_encontradas = []
    st.session_state.intentos_sin_rectangulo = []


def render_cuaderno(total: int):
    st.markdown("<div class='notebook'>", unsafe_allow_html=True)
    st.markdown("### Mi cuaderno de exploración")
    st.write(f"Estoy explorando organizaciones rectangulares para **{total} objetos**.")

    if st.session_state.organizaciones_encontradas:
        st.markdown("**Organizaciones rectangulares encontradas:**")
        for f, c in st.session_state.organizaciones_encontradas:
            st.markdown(f"<span class='badge-ok'>✓</span> **{f} × {c} = {total}**", unsafe_allow_html=True)
    else:
        st.caption("Todavía no registraste organizaciones rectangulares completas.")

    if st.session_state.intentos_sin_rectangulo:
        st.markdown("**Intentos en los que quedaron objetos fuera:**")
        st.write(", ".join([f"{k} filas" for k in st.session_state.intentos_sin_rectangulo]))

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Interfaz
# -----------------------------
st.markdown(
    '<div class="top"><span class="code">OR-01</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Explorar organizaciones rectangulares</span></div>',
    unsafe_allow_html=True
)

st.title("Explorando organizaciones rectangulares")
st.subheader("Múltiplos y divisores a partir de rectángulos")
st.write("Exploramos de cuántas maneras una misma colección puede organizarse formando rectángulos.")
st.info("En este laboratorio buscamos organizar todos los objetos en filas con la misma cantidad. Cuando no se puede completar el rectángulo, algunos objetos quedan fuera.")
st.divider()

step(1, "Elegí la cantidad de objetos")
total = st.slider("Cantidad de objetos", 1, MAX_OBJETOS, st.session_state.or_total_anterior, step=1)

if total != st.session_state.or_total_anterior:
    st.session_state.or_total_anterior = total
    reiniciar_cuaderno()

step(2, "Probá una cantidad de filas")
filas = st.slider("Cantidad de filas", 1, min(MAX_FILAS, total), min(4, total), step=1)

columnas = total // filas
fuera = total % filas
organizados = filas * columnas

registrar_exploracion(total, filas, columnas, fuera)

st.markdown(f'<div class="info">Intentamos organizar <span class="num">{total}</span> objetos en <span class="num">{filas}</span> filas iguales.</div>', unsafe_allow_html=True)

col_main, col_note = st.columns([2.2, 1])

with col_main:
    step(3, "Observamos la organización")
    col_rect, col_fuera = st.columns([2.2, 1])
    with col_rect:
        st.markdown("<div class='btitle'>Así queda organizada la colección</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="card main"><b>{filas} filas de {columnas}</b><br><br>{rect_html(filas,columnas)}</div>', unsafe_allow_html=True)
    with col_fuera:
        st.markdown("<div class='btitle'>Quedan fuera</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="card">{fuera_html(fuera)}</div>', unsafe_allow_html=True)

with col_note:
    render_cuaderno(total)
    if st.button("Reiniciar mi cuaderno"):
        reiniciar_cuaderno()
        st.rerun()

step(4, "¿Qué está pasando?")
if fuera == 0:
    st.markdown(f"""<div class="explain"><div class="etitle">Se pudo formar un rectángulo completo</div>
    Los <span class="blue"><b>{total}</b></span> objetos quedaron organizados en <span class="green"><b>{filas}</b></span> filas de <span class="yellow"><b>{columnas}</b></span> objetos cada una.
    <div class="note">Esta organización quedó registrada en tu cuaderno de exploración.</div></div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="explain"><div class="etitle">No se pudo completar el rectángulo</div>
    Se organizaron <span class="green"><b>{organizados}</b></span> objetos en <span class="green"><b>{filas}</b></span> filas de <span class="yellow"><b>{columnas}</b></span> objetos cada una. Quedaron <span class="red"><b>{fuera}</b></span> objetos fuera.
    <div class="note">Este intento también puede ayudarte a pensar qué cantidades de filas funcionan y cuáles no.</div></div>""", unsafe_allow_html=True)

step(5, "Lo representamos matemáticamente")
st.write("Esta es una forma de escribir la organización que acabamos de observar:")
summary(total, filas, columnas, fuera)

step(6, "¿Será la única organización posible?")
with st.container(border=True):
    st.radio(
        "¿Pensás que esta es la única manera de organizar esta colección formando un rectángulo completo?",
        ["Sí", "No", "No estoy seguro"],
        index=None
    )
    st.caption("Antes de mirar todas las posibilidades, probá otras cantidades de filas y observá qué se registra en tu cuaderno.")

step(7, "Comparamos con todas las organizaciones posibles")
if st.checkbox("Mostrar todas las organizaciones posibles"):
    pares = pares_rectangulares(total)
    encontradas = set(st.session_state.organizaciones_encontradas)
    todas = set(pares)

    st.markdown(
        f'<div class="info">Para <span class="num">{total}</span> objetos hay <span class="num">{len(pares)}</span> organizaciones rectangulares diferentes, sin contar los giros como organizaciones nuevas.</div>',
        unsafe_allow_html=True
    )

    faltan = todas - encontradas
    if faltan:
        st.warning(f"Todavía no aparecieron en tu cuaderno todas las organizaciones posibles. Podés seguir explorando o mirar la galería.")
    else:
        st.success("Tu cuaderno ya contiene todas las organizaciones rectangulares posibles para esta colección.")

    st.markdown("<div class='gallery'>Galería de organizaciones rectangulares</div>", unsafe_allow_html=True)

    for i in range(0, len(pares), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(pares):
                f, c = pares[idx]
                with col:
                    rect_card(f, c, total, main=(normalizar_par(f, c) in encontradas))

    with st.container(border=True):
        st.markdown("### Para mirar la galería")
        st.markdown("""
1. ¿Qué cambia entre una organización rectangular y otra?
2. ¿Qué permanece igual en todas?
3. ¿Qué cantidades de filas permiten formar rectángulos completos?
4. ¿Qué ocurre cuando giramos un rectángulo?
5. ¿Cómo podrías estar seguro de que encontraste todas las organizaciones posibles?
""")

    if st.checkbox("Mostrar una pista sobre divisores"):
        ds = divisores(total)
        st.info(f"Las cantidades de filas que permiten formar un rectángulo completo reciben el nombre de divisores de {total}. En este caso son: {', '.join(str(d) for d in ds)}.")

st.divider()
st.markdown("### Sobre este laboratorio")
st.markdown("**Explorando organizaciones rectangulares** forma parte de **LIM (Laboratorio de Ideas Matemáticas)**.")
st.markdown("**Versión:** 0.3 (prototipo)")
