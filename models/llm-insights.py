def generate_cfo_summary(
    ventas,
    utilidad,
    margen,
    forecast90,
    producto_top,
    categoria_top,
    pais_top
):

    texto = f"""
RESUMEN CFO

Las ventas acumuladas alcanzan ${ventas:,.0f}.

La utilidad consolidada asciende a ${utilidad:,.0f},
con un margen operativo de {margen:.2f}%.

La categoría con mejor desempeño es
{categoria_top}.

El producto líder es
{producto_top}.

El país con mayor contribución es
{pais_top}.

El forecast proyecta ventas por
${forecast90:,.0f}
durante los próximos 90 días.
"""

    return texto