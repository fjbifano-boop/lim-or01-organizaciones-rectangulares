import math
import streamlit as st

st.set_page_config(page_title="LIM - Organizaciones rectangulares", layout="wide")

st.markdown("""
<style>
.block-container{max-width:1200px;padding-top:1.2rem}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#152238 0%,#0b111c 42%,#070b12 100%);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(0,0,0,0)}
h1,h2,h3,p,li,span,div{color:#f8fafc}
.top{display:flex;align-items:center;border-bottom:1px solid rgba(148,163,184,.45);padding-bottom:14px;margin-bottom:24px}
.code{color:#2f80ed;font-weight:800;font-size:22px}.title{font-size:22px;margin-left:12px}
.step{font-size:32px;font-weight:850;margin-top:24px;margin-bottom:18px}
.info{border:1px solid rgba(47,128,237,.55);background:rgba(14,71,125,.38);border-radius:10px;padding:18px 22px;font-size:19px;margin:18px 0}
.info .num{color:#2f80ed;font-weight:900}
.card{border:1px solid rgba(148,163,184,.38);background:rgba(2,6,23,.38);border-radius:10px;padding:14px;overflow-x:auto;min-height:120px;margin-bottom:14px}
.btitle{font-size:24px;font-weight:850;margin-bottom:14px}
.objects{display:inline-flex;flex-direction:column;gap:5px;align-items:flex-start}.row{display:flex;gap:5px}
.sq{display:inline-block;width:22px;height:22px;border-radius:3px;flex:0 0 auto}
.blueSq{background:#2f80ed;border:2px solid #1e40af}.redSq{background:#ef4444;border:2px solid #b91c1c}
.explain{border:1px solid rgba(47,128,237,.5);background:rgba(14,71,125,.34);border-radius:10px;padding:18px 22px;margin-top:18px;font-size:20px}
.explain-title{color:#facc15;font-size:24px;font-weight:900;margin-bottom:8px}.note{color:#cbd5e1;font-size:16px;font-style:italic;margin-top:12px}
.summary{display:grid;grid-template-columns:1fr .15fr 1fr .15fr 1fr .15fr 1fr;gap:14px;align-items:center;border:1px solid rgba(148,163,184,.35);background:rgba(15,23,42,.58);border-radius:12px;padding:18px;margin:18px 0}
.box{border-radius:10px;padding:12px;text-align:center;background:rgba(2,6,23,.36)}.bb{border:1px solid #2f80ed}.bg{border:1px solid #47d147}.by{border:1px solid #f2b705}.br{border:1px solid #ef4444}
.label{font-size:18px}.num2{font-size:32px;font-weight:900}.blue{color:#2f80ed}.green{color:#47d147}.yellow{color:#f2b705}.red{color:#ef4444}.op{font-size:28px;font-weight:800;text-align:center}
</style>
""", unsafe_allow_html=True)

def divisores(n):
    return [k for k in range(1, n+1) if n % k == 0]

def rect_html(filas, columnas, color="blue"):
    cls = "blueSq" if color=="blue" else "redSq"
    html = "<div class='objects'>"
    for _ in range(filas):
        html += "<div class='row'>"
        for _ in range(columnas):
            html += f"<span class='sq {cls}'></span>"
        html += "</div>"
    html += "</div>"
    return html

def line_html(n):
    if n == 0:
        return "<span style='color:#86efac;font-weight:800'>No quedaron objetos fuera del rectángulo.</span>"
    return rect_html(1, n, "red")

def step(n, txt):
    st.markdown(f"<div class='step'>{n}. {txt}</div>", unsafe_allow_html=True)

def summary(total, filas, columnas, fuera):
    st.markdown(f"""
    <div class="summary">
      <div class="box bb"><div class="label">Objetos totales</div><div class="num2 blue">{total}</div></div>
      <div class="op">=</div>
      <div class="box bg"><div class="label">Filas</div><div class="num2 green">{filas}</div></div>
      <div class="op">×</div>
      <div class="box by"><div class="label">Columnas</div><div class="num2 yellow">{columnas}</div></div>
      <div class="op">+</div>
      <div class="box br"><div class="label">Fuera</div><div class="num2 red">{fuera}</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="top"><span class="code">OR-01</span><span style="color:#94a3b8;margin-left:12px">|</span><span class="title">Explorar organizaciones rectangulares</span></div>', unsafe_allow_html=True)
st.title("Explorando organizaciones rectangulares")
st.subheader("Múltiplos y divisores a partir de rectángulos")
st.write("Exploramos cuándo una colección puede organizarse formando un rectángulo completo.")

st.info("Buscamos organizar todos los objetos en filas con la misma cantidad. Cuando no se puede completar el rectángulo, algunos objetos quedan fuera.")
st.divider()

step(1, "Elegí la cantidad de objetos")
total = st.slider("Cantidad de objetos", 1, 80, 24, step=1)

step(2, "Elegí cuántas filas querés formar")
filas = st.slider("Cantidad de filas", 1, min(20, total), min(4, total), step=1)

columnas = total // filas
fuera = total % filas
organizados = filas * columnas

st.markdown(f'<div class="info">Intentamos organizar <span class="num">{total}</span> objetos en <span class="num">{filas}</span> filas iguales.</div>', unsafe_allow_html=True)

step(3, "Observamos la organización")
col_rect, col_fuera = st.columns([2.2, 1])
with col_rect:
    st.markdown(f"<div class='btitle'>Rectángulo formado: {filas} filas de {columnas}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>{rect_html(filas, columnas, 'blue')}</div>", unsafe_allow_html=True)
with col_fuera:
    st.markdown("<div class='btitle'>Quedan fuera</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>{line_html(fuera)}</div>", unsafe_allow_html=True)

step(4, "¿Qué está pasando?")
if fuera == 0:
    st.markdown(f"""
    <div class="explain"><div class="explain-title">Se pudo formar un rectángulo completo</div>
    Los <span class="blue"><b>{total}</b></span> objetos quedaron organizados en <span class="green"><b>{filas}</b></span> filas de <span class="yellow"><b>{columnas}</b></span> objetos cada una.
    <div class="note">{total} es múltiplo de {filas}; {filas} es divisor de {total}.</div></div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="explain"><div class="explain-title">No se pudo completar el rectángulo</div>
    Se organizaron <span class="green"><b>{organizados}</b></span> objetos en <span class="green"><b>{filas}</b></span> filas de <span class="yellow"><b>{columnas}</b></span>. Quedaron <span class="red"><b>{fuera}</b></span> fuera.
    <div class="note">{total} no es múltiplo de {filas}.</div></div>
    """, unsafe_allow_html=True)

step(5, "Lo representamos matemáticamente")
summary(total, filas, columnas, fuera)

with st.container(border=True):
    st.markdown("### Para pensar")
    st.markdown("""
1. ¿Cuándo se forma un rectángulo completo?
2. ¿Qué cantidades de filas permiten organizar todos los objetos sin que quede ninguno fuera?
3. ¿Qué cantidades de filas dejan objetos fuera?
4. Si girás un rectángulo, ¿cambia la cantidad total de objetos?
5. ¿Qué relación encontrás entre filas, columnas y cantidad total?
""")

step(6, "Buscamos todas las organizaciones rectangulares")
if st.checkbox("Mostrar todas las organizaciones rectangulares posibles"):
    ds = divisores(total)
    st.write(f"Para {total} objetos, estas cantidades de filas permiten formar rectángulos completos:")
    st.markdown(", ".join([f"**{d}**" for d in ds]))
    pares = [(d, total//d) for d in ds if d <= total//d]
    for i in range(0, len(pares), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i+j
            if idx < len(pares):
                f, c = pares[idx]
                with col:
                    st.markdown(f"**{f} × {c} = {total}**")
                    st.markdown(f"<div class='card'>{rect_html(f, c, 'blue')}</div>", unsafe_allow_html=True)
                    if f != c:
                        st.caption(f"Si lo giramos, también podemos verlo como {c} × {f}.")

with st.container(border=True):
    st.markdown("### Relación con multiplicación y división")
    if st.checkbox("Mostrar relaciones"):
        if fuera == 0:
            st.markdown(f"""
- **{filas} × {columnas} = {total}**
- **{total} ÷ {filas} = {columnas}**
- **{total} ÷ {columnas} = {filas}**
""")
        else:
            st.markdown(f"""
Con esta cantidad de filas no se forma un rectángulo completo:

- **{filas} × {columnas} = {organizados}**
- **{total} = {filas} × {columnas} + {fuera}**
""")

st.divider()
st.markdown("### Sobre este laboratorio")
st.markdown("**Explorando organizaciones rectangulares** forma parte de **LIM (Laboratorio de Ideas Matemáticas)**.")
st.markdown("**Versión:** 0.1 (primer prototipo)")

