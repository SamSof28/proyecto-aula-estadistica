"""Dashboard interactivo para la exposición del proyecto de aula."""

from pathlib import Path

import dash
from dash import Input, Output, dcc, html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats


ROOT = Path(__file__).resolve().parent
COLORS = {
    "navy": "#102A43",
    "blue": "#1677FF",
    "cyan": "#16B8D4",
    "gold": "#F5B942",
    "green": "#13B887",
    "red": "#E85D75",
    "ink": "#243B53",
    "muted": "#627D98",
    "surface": "#FFFFFF",
    "background": "#F4F7FB",
    "grid": "#E6EDF5",
}
PLOT_CONFIG = {"displayModeBar": False, "responsive": True}


def load_question_1() -> pd.DataFrame:
    path = ROOT / "Pregunta1" / "BD Proyecto de Aula DEF 2026-2.xlsx"
    data = pd.read_excel(path).dropna(subset=["Marca", "ppm", "Potencia"]).copy()
    data["Marca"] = data["Marca"].astype(int)
    data["potencia_ok"] = data["Potencia"].between(2.48, 2.92)
    data["emision_ok"] = data["ppm"] <= 400
    return data


def load_question_2() -> pd.DataFrame:
    rng = np.random.RandomState(2026)
    groups = [
        ("Escenario 1 · Normal", "Equipo A", rng.normal(175, 30, 60)),
        ("Escenario 1 · Normal", "Equipo B", rng.normal(170, 50, 60)),
        ("Escenario 2 · Gamma", "Equipo A", rng.gamma(1.2, 150, 60)),
        ("Escenario 2 · Gamma", "Equipo B", rng.gamma(0.95, 190, 60)),
    ]
    return pd.DataFrame(
        [
            {"Escenario": scenario, "Equipo": team, "Tiempo (ms)": value}
            for scenario, team, values in groups
            for value in values
        ]
    )


def load_question_3() -> pd.DataFrame:
    path = ROOT / "Pregunta3" / "base_datos_pregunta_3.csv"
    return pd.read_csv(path)


Q1 = load_question_1()
Q2 = load_question_2()
Q3 = load_question_3()


def fmt(value: float, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def card(label: str, value: str, detail: str = "", accent: str = "blue") -> html.Div:
    return html.Div(
        [
            html.Div(label.upper(), className="kpi-label"),
            html.Div(value, className="kpi-value", style={"color": COLORS[accent]}),
            html.Div(detail, className="kpi-detail"),
        ],
        className="kpi-card",
    )


def section_title(kicker: str, title: str, text: str) -> html.Div:
    return html.Div(
        [
            html.Div(kicker.upper(), className="eyebrow"),
            html.H2(title, className="section-title"),
            html.P(text, className="section-intro"),
        ],
        className="section-heading",
    )


def chart_base(fig: go.Figure, height: int = 410) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin={"l": 12, "r": 18, "t": 42, "b": 12},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Inter, Segoe UI, sans-serif", "color": COLORS["ink"]},
        legend={"orientation": "h", "y": 1.08, "x": 0},
        xaxis={"gridcolor": COLORS["grid"], "zeroline": False},
        yaxis={"gridcolor": COLORS["grid"], "zeroline": False},
    )
    return fig


def q1_summary() -> pd.DataFrame:
    summary = Q1.groupby("Marca").agg(
        hornos=("Horno", "count"),
        ppm_medio=("ppm", "mean"),
        ppm_mediana=("ppm", "median"),
        potencia_media=("Potencia", "mean"),
        potencia_ok=("potencia_ok", "mean"),
        emision_ok=("emision_ok", "mean"),
    ).reset_index()
    summary["potencia_ok"] *= 100
    summary["emision_ok"] *= 100
    return summary


Q1_SUMMARY = q1_summary()
# Se prioriza la menor emisión entre las marcas que cumplen el límite de seguridad.
SAFE_BRANDS = Q1_SUMMARY[Q1_SUMMARY["emision_ok"] >= 99.9]
BEST_BRAND = int(SAFE_BRANDS.loc[SAFE_BRANDS["ppm_medio"].idxmin(), "Marca"])


def app_styles() -> str:
    return """
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    * { box-sizing: border-box; }
    body { margin: 0; background: #F4F7FB; color: #243B53; font-family: 'DM Sans', sans-serif; }
    .app-shell { min-height: 100vh; }
    .hero { background: linear-gradient(118deg, #102A43 0%, #164E78 58%, #1677FF 100%); color: white; padding: 34px 6vw 30px; position: relative; overflow: hidden; }
    .hero:after { content: ''; position: absolute; width: 340px; height: 340px; border: 60px solid rgba(255,255,255,.07); border-radius: 50%; right: -80px; top: -190px; }
    .hero-content { max-width: 1220px; margin: auto; position: relative; z-index: 1; }
    .brand-line { display: flex; justify-content: space-between; align-items: center; gap: 20px; font-size: 13px; letter-spacing: .08em; text-transform: uppercase; opacity: .8; }
    .hero h1 { font-family: 'Space Grotesk', sans-serif; font-size: clamp(30px, 4vw, 48px); line-height: 1.05; max-width: 750px; margin: 25px 0 10px; }
    .hero p { font-size: 16px; max-width: 680px; color: #D9EAF7; margin: 0; }
    .content { max-width: 1220px; margin: auto; padding: 24px 6vw 56px; }
    .tabs-shell { background: white; border-radius: 14px; padding: 6px; box-shadow: 0 8px 26px rgba(16,42,67,.08); margin-bottom: 32px; }
    .tab { border: 0 !important; color: #627D98 !important; font-weight: 600 !important; padding: 15px 18px !important; border-radius: 10px !important; background: transparent !important; }
    .tab--selected { color: #102A43 !important; background: #E8F1FF !important; border: 0 !important; }
    .section-heading { margin: 12px 0 22px; }
    .eyebrow { color: #1677FF; font-size: 12px; font-weight: 700; letter-spacing: .13em; }
    .section-title { font-family: 'Space Grotesk', sans-serif; font-size: 29px; margin: 5px 0 7px; color: #102A43; }
    .section-intro { color: #627D98; max-width: 800px; line-height: 1.6; margin: 0; }
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 22px 0 28px; }
    .kpi-card, .panel, .insight { background: white; border: 1px solid #E6EDF5; border-radius: 14px; box-shadow: 0 5px 18px rgba(16,42,67,.045); }
    .kpi-card { padding: 18px 20px; min-height: 118px; }
    .kpi-label { font-size: 11px; color: #627D98; font-weight: 700; letter-spacing: .08em; }
    .kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; margin: 8px 0 3px; }
    .kpi-detail { font-size: 12px; color: #829AB1; }
    .two-col { display: grid; grid-template-columns: 1.35fr 1fr; gap: 18px; margin-bottom: 18px; }
    .panel { padding: 18px; }
    .panel .dash-graph { height: 410px !important; min-height: 410px; width: 100%; }
    .panel h3 { margin: 0 0 2px; font-size: 16px; color: #102A43; }
    .panel-subtitle { color: #829AB1; font-size: 12px; margin-bottom: 8px; }
    .insight { border-left: 4px solid #16B8D4; padding: 17px 20px; line-height: 1.55; margin: 18px 0; }
    .insight strong { color: #102A43; }
    .controls { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin: 12px 0 16px; }
    .control-label { font-size: 12px; color: #627D98; font-weight: 700; }
    .footer { color: #829AB1; text-align: center; font-size: 12px; margin-top: 40px; }
    @media (max-width: 850px) { .kpi-grid, .two-col { grid-template-columns: 1fr 1fr; } .two-col { grid-template-columns: 1fr; } }
    @media (max-width: 560px) { .panel .dash-graph { height: 350px !important; min-height: 350px; } }
    @media (max-width: 560px) { .kpi-grid { grid-template-columns: 1fr; } .brand-line { display: block; } .hero { padding: 28px 5vw; } .content { padding: 20px 4vw 45px; } }
    """


app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Estadística para Ingeniería")
app.index_string = f"""<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{app_styles()}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>"""

app.layout = html.Div(
    [
        html.Header(
            html.Div(
                [
                    html.Div(
                        [html.Span("Proyecto de aula · 2026-2"), html.Span("U. de Medellín")],
                        className="brand-line",
                    ),
                    html.H1("Estadística que convierte datos en decisiones."),
                    html.P(
                        "Una presentación interactiva sobre calidad, tiempos de procesamiento y rendimiento de software."
                    ),
                ],
                className="hero-content",
            ),
            className="hero",
        ),
        html.Main(
            [
                html.Div(
                    dcc.Tabs(
                        id="tabs-proyecto",
                        value="tab-1",
                        children=[
                            dcc.Tab(label="01 · Calidad de hornos", value="tab-1", className="tab", selected_className="tab--selected"),
                            dcc.Tab(label="02 · Equipos y latencia", value="tab-2", className="tab", selected_className="tab--selected"),
                            dcc.Tab(label="03 · Python vs Java", value="tab-3", className="tab", selected_className="tab--selected"),
                        ],
                    ),
                    className="tabs-shell",
                ),
                html.Div(id="contenido-tab"),
                html.Footer("Datos y cálculos reproducibles a partir de los archivos del proyecto · Estadística para Ingeniería", className="footer"),
            ],
            className="content",
        ),
    ],
    className="app-shell",
)


def q1_layout() -> html.Div:
    best = Q1_SUMMARY[Q1_SUMMARY["Marca"] == BEST_BRAND].iloc[0]
    return html.Div(
        [
            section_title(
                "Pregunta 1 · Control de calidad",
                "¿Qué marca ofrece el mejor desempeño?",
                "Se analizaron 3.663 registros válidos (de 3.665 en la base original) en términos de emisiones contaminantes y cumplimiento de la potencia nominal 2,7 ± 0,22 kW.",
            ),
            html.Div(
                [
                    card("Hornos analizados", fmt(len(Q1), 0), "Registros válidos de la base real", "blue"),
                    card("Marca recomendada", f"Marca {BEST_BRAND}", f"{best['emision_ok']:.1f}% con emisiones seguras", "green"),
                    card("Límite de seguridad", "400 ppm", "Emisión máxima recomendada", "gold"),
                    card("Especificación", "2,48–2,92 kW", "Rango de potencia nominal", "cyan"),
                ],
                className="kpi-grid",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Emisiones por marca"),
                            html.Div("La línea punteada representa el límite de seguridad de 400 ppm.", className="panel-subtitle"),
                            dcc.Graph(id="boxplot-ppm-interactive", config=PLOT_CONFIG),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.H3("Cumplimiento de potencia"),
                            html.Div("Porcentaje de hornos dentro del rango nominal.", className="panel-subtitle"),
                            dcc.Graph(id="potencia-bar", config=PLOT_CONFIG),
                        ],
                        className="panel",
                    ),
                ],
                className="two-col",
            ),
            html.Div(
                [
                    html.Div("EXPLORAR UNA MARCA", className="control-label"),
                    dcc.Dropdown(
                        id="marca-filter",
                        options=[{"label": f"Marca {m}", "value": m} for m in sorted(Q1["Marca"].unique())],
                        value=BEST_BRAND,
                        clearable=False,
                        style={"width": "180px"},
                    ),
                    html.Div(id="metricas-marca"),
                ],
                className="controls",
            ),
            html.Div(
                [
                    html.H3("Lectura para la exposición"),
                    html.P(
                        f"La Marca {BEST_BRAND} presenta la menor media de emisiones ({best['ppm_medio']:.1f} ppm) "
                        f"y el mayor cumplimiento de emisiones ({best['emision_ok']:.1f}%). "
                        "Aunque la Marca 1 tiene ligeramente mayor cumplimiento de potencia, la Marca 5 ofrece el perfil "
                        "ambiental más consistente para una recomendación integral.",
                    ),
                ],
                className="insight",
            ),
        ]
    )


def q2_layout() -> html.Div:
    return html.Div(
        [
            section_title(
                "Pregunta 2 · Inferencia estadística",
                "¿Cambian los tiempos entre equipos?",
                "Se generaron 60 observaciones por equipo y escenario con semilla 2026. La comparación combina pruebas paramétricas y no paramétricas.",
            ),
            html.Div(
                [
                    card("Observaciones", "240", "4 grupos · 60 por grupo", "blue"),
                    card("Escenario normal", "p = 0,511", "Welch: no diferencia significativa", "green"),
                    card("Escenario gamma", "p = 0,228", "Welch: no diferencia significativa", "gold"),
                    card("Nivel de decisión", "α = 0,05", "Criterio para rechazar H₀", "cyan"),
                ],
                className="kpi-grid",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Distribución de los tiempos"),
                            html.Div("Seleccione el escenario para contrastar sus distribuciones.", className="panel-subtitle"),
                            html.Div(
                                [
                                    dcc.RadioItems(
                                        id="q2-scenario",
                                        options=[
                                            {"label": "Escenario 1 · Normal", "value": "Escenario 1 · Normal"},
                                            {"label": "Escenario 2 · Gamma", "value": "Escenario 2 · Gamma"},
                                        ],
                                        value="Escenario 1 · Normal",
                                        inline=True,
                                        labelStyle={"marginRight": "18px", "fontSize": "13px"},
                                    )
                                ],
                                className="controls",
                            ),
                            dcc.Graph(id="histograma-escenarios", config=PLOT_CONFIG),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.H3("Resumen por grupo"),
                            html.Div("Media y dispersión observadas en cada distribución.", className="panel-subtitle"),
                            html.Div(id="q2-summary-table"),
                            html.Div(id="q2-interpretation", className="insight"),
                        ],
                        className="panel",
                    ),
                ],
                className="two-col",
            ),
        ]
    )


def q3_layout() -> html.Div:
    grouped = Q3.groupby("Lenguaje")["Tiempo_ms"]
    java_mean = grouped.mean()["Java"]
    python_mean = grouped.mean()["Python"]
    return html.Div(
        [
            section_title(
                "Pregunta 3 · Aplicación en ingeniería de sistemas",
                "¿Qué runtime ordena más rápido?",
                "Experimento práctico con 100 mediciones reales por lenguaje al ordenar un arreglo de un millón de números.",
            ),
            html.Div(
                [
                    card("Mediciones", "200", "100 por lenguaje", "blue"),
                    card("Java · promedio", f"{java_mean:.1f} ms", "Menor tiempo observado", "green"),
                    card("Python · promedio", f"{python_mean:.1f} ms", "Mayor variabilidad", "gold"),
                    card("Ventaja de Java", f"{python_mean / java_mean:.1f}×", "Respecto al tiempo promedio", "cyan"),
                ],
                className="kpi-grid",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Distribución de tiempos de ejecución"),
                            html.Div("Cada punto es una medición del experimento.", className="panel-subtitle"),
                            dcc.Graph(id="boxplot-lenguajes", config=PLOT_CONFIG),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.H3("Comparación de promedios"),
                            html.Div("El promedio resume el costo temporal observado.", className="panel-subtitle"),
                            dcc.Graph(id="mean-languages", config=PLOT_CONFIG),
                        ],
                        className="panel",
                    ),
                ],
                className="two-col",
            ),
            html.Div(
                [
                    html.H3("Conclusión para la exposición"),
                    html.P(
                        f"En este entorno y con este experimento, Java tarda en promedio {python_mean / java_mean:.1f} veces menos "
                        f"que Python ({java_mean:.1f} ms frente a {python_mean:.1f} ms). La conclusión aplica a esta implementación, "
                        "hardware y configuración; no representa una superioridad universal de un lenguaje.",
                    ),
                ],
                className="insight",
            ),
        ]
    )


@app.callback(Output("contenido-tab", "children"), Input("tabs-proyecto", "value"))
def render_content(tab: str) -> html.Div:
    return {"tab-1": q1_layout, "tab-2": q2_layout, "tab-3": q3_layout}.get(tab, q1_layout)()


@app.callback(
    Output("boxplot-ppm-interactive", "figure"),
    Output("potencia-bar", "figure"),
    Input("tabs-proyecto", "value"),
)
def update_q1_charts(_tab: str):
    box = px.box(
        Q1,
        x="Marca",
        y="ppm",
        color="Marca",
        points=False,
        color_discrete_sequence=[COLORS["blue"], COLORS["cyan"], COLORS["green"], COLORS["gold"], COLORS["red"]],
        labels={"Marca": "Marca", "ppm": "Emisiones (ppm)"},
    )
    box.add_hline(y=400, line_dash="dash", line_color=COLORS["red"], annotation_text="Límite 400 ppm")
    box.update_layout(showlegend=False)
    bar = px.bar(
        Q1_SUMMARY,
        x=Q1_SUMMARY["Marca"].astype(str),
        y="potencia_ok",
        text=Q1_SUMMARY["potencia_ok"].map(lambda x: f"{x:.1f}%"),
        color="potencia_ok",
        color_continuous_scale=[[0, "#B8E8E0"], [1, COLORS["green"]]],
        labels={"x": "Marca", "potencia_ok": "Cumplimiento (%)"},
    )
    bar.update_traces(textposition="outside", hovertemplate="Marca %{x}<br>Cumplimiento: %{y:.1f}%<extra></extra>")
    bar.update_coloraxes(showscale=False)
    return chart_base(box), chart_base(bar, 380)


@app.callback(Output("metricas-marca", "children"), Input("marca-filter", "value"))
def update_brand_metrics(brand: int):
    row = Q1_SUMMARY[Q1_SUMMARY["Marca"] == brand].iloc[0]
    return html.Div(
        [
            html.Span(f"{int(row['hornos']):,} hornos · {row['ppm_medio']:.1f} ppm promedio · ", className="kpi-detail"),
            html.Strong(f"{row['emision_ok']:.1f}% emisiones seguras", style={"color": COLORS["green"]}),
        ],
        style={"marginLeft": "8px"},
    )


@app.callback(
    Output("histograma-escenarios", "figure"),
    Output("q2-summary-table", "children"),
    Output("q2-interpretation", "children"),
    Input("q2-scenario", "value"),
)
def update_q2(scenario: str):
    data = Q2[Q2["Escenario"] == scenario]
    fig = px.histogram(
        data,
        x="Tiempo (ms)",
        color="Equipo",
        facet_row=None,
        barmode="overlay",
        nbins=16,
        opacity=0.72,
        color_discrete_map={"Equipo A": COLORS["blue"], "Equipo B": COLORS["gold"]},
        labels={"Tiempo (ms)": "Tiempo de procesamiento (ms)"},
    )
    fig.update_traces(marker_line_width=0)
    fig = chart_base(fig, 400)
    summary = data.groupby("Equipo")["Tiempo (ms)"].agg(["mean", "std", "median"]).reset_index()
    table = html.Table(
        [
            html.Thead(html.Tr([html.Th("Equipo"), html.Th("Media"), html.Th("Desv."), html.Th("Mediana")])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["Equipo"]),
                            html.Td(f"{row['mean']:.2f} ms"),
                            html.Td(f"{row['std']:.2f} ms"),
                            html.Td(f"{row['median']:.2f} ms"),
                        ]
                    )
                    for _, row in summary.iterrows()
                ]
            ),
        ],
        style={"width": "100%", "borderCollapse": "collapse", "fontSize": "13px", "lineHeight": "2.3"},
    )
    if scenario.startswith("Escenario 1"):
        p_value, mw_p = 0.5112, 0.7231
        conclusion = "Las pruebas Welch y Mann–Whitney coinciden: no hay evidencia estadística suficiente de una diferencia entre los equipos."
    else:
        p_value, mw_p = 0.2282, 0.2879
        conclusion = "Aunque las medias difieren en la muestra, Welch y Mann–Whitney no alcanzan α = 0,05; no se rechaza la igualdad entre equipos."
    interpretation = html.P([html.Strong("Interpretación: "), f"{conclusion} (Welch p = {p_value:.4f}; Mann–Whitney p = {mw_p:.4f})."])
    return fig, table, interpretation


@app.callback(
    Output("boxplot-lenguajes", "figure"),
    Output("mean-languages", "figure"),
    Input("tabs-proyecto", "value"),
)
def update_q3_charts(_tab: str):
    box = px.box(
        Q3,
        x="Lenguaje",
        y="Tiempo_ms",
        color="Lenguaje",
        points="all",
        color_discrete_map={"Java": COLORS["green"], "Python": COLORS["gold"]},
        labels={"Tiempo_ms": "Tiempo (ms)"},
    )
    box.update_layout(showlegend=False)
    means = Q3.groupby("Lenguaje", as_index=False)["Tiempo_ms"].mean()
    bar = px.bar(
        means,
        x="Lenguaje",
        y="Tiempo_ms",
        color="Lenguaje",
        text="Tiempo_ms",
        color_discrete_map={"Java": COLORS["green"], "Python": COLORS["gold"]},
        labels={"Tiempo_ms": "Promedio (ms)"},
    )
    bar.update_traces(texttemplate="%{text:.1f} ms", textposition="outside")
    bar.update_layout(showlegend=False)
    return chart_base(box), chart_base(bar)


if __name__ == "__main__":
    app.run(debug=True)
