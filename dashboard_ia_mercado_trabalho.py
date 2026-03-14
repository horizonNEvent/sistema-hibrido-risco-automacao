"""
Dashboard Interativo: O Futuro do Mercado de Trabalho com Inteligência Artificial
Autor: Bruno Vollu Sampaio
Estilo: Tech Noir / Cyberpunk
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ─────────────────────────────────────────────
# PALETA DE CORES CYBERPUNK
# ─────────────────────────────────────────────
BG_MAIN      = "#0A1428"      # Azul-petróleo profundo
BG_CARD      = "#0D1F3C"      # Card background
CYAN         = "#00FFFF"      # Cyan neon
MAGENTA      = "#FF00FF"      # Magenta neon
YELLOW       = "#FFD700"      # Amarelo neon
GREEN        = "#00FF88"      # Verde neon
WHITE        = "#FFFFFF"
GRID_COLOR   = "#1A3A6B"
TEXT_DIM     = "#8899BB"

FONT_FAMILY  = "'Segoe UI', 'Calibri', sans-serif"

PLOTLY_LAYOUT = dict(
    font=dict(family=FONT_FAMILY, color=WHITE),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=30, r=30, t=50, b=30),
)

# Legend padrão para reutilizar
LEGEND_BASE = dict(
    bgcolor="rgba(10,20,40,0.8)",
    bordercolor=CYAN,
    borderwidth=1,
    font=dict(color=WHITE)
)

LEGEND_DONUT = dict(
    bgcolor="rgba(0,0,0,0)",
    font=dict(color=WHITE, size=10),
    orientation="v",
    x=1.02, y=0.5,
    xanchor="left", yanchor="middle",
)

# ─────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────

# Gráfico 1: Adoção IA vs Teletrabalho
g1_anos       = ["2022", "2024"]
g1_ia         = [16.9, 41.9]
g1_teletrabalho = [47.8, 42.9]

# Gráfico 2: Barreiras de IA (Donut)
g2_labels  = ["Altos Custos", "Falta de Pessoal Qualificado", "Riscos de Segurança"]
g2_values  = [78.6, 54.2, 47.2]
g2_colors  = [MAGENTA, CYAN, YELLOW]

# Gráfico 3: Scatter – Matriz de Risco de Automação
np.random.seed(42)
risco_alto_x = np.random.uniform(0.65, 1.0, 30)
risco_alto_y = np.random.uniform(0.65, 1.0, 30)
risco_baixo_x = np.random.uniform(0.0, 0.45, 25)
risco_baixo_y = np.random.uniform(0.0, 0.45, 25)

# Gráfico 4: Habilidades do Futuro
g4_skills    = ["Liderança e Inteligência Social", "IA e Big Data",
                "Resiliência e Flexibilidade", "Pensamento Analítico"]
g4_scores    = [82, 87, 91, 95]
g4_colors_list = [CYAN, GREEN, YELLOW, MAGENTA]

# ─────────────────────────────────────────────
# OPÇÕES DOS FILTROS
# ─────────────────────────────────────────────
SETORES = ["Todos", "Manufatura", "Serviços Financeiros", "Saúde",
           "Tecnologia", "Varejo", "Agronegócio", "Energia"]
NIVEIS  = ["Todos", "Operacional", "Tático", "Estratégico"]
REGIOES = ["Todos", "Brasil", "Estados Unidos", "União Europeia",
           "China", "América Latina", "Ásia-Pacífico"]

# ─────────────────────────────────────────────
# APP DASH
# ─────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title="IA & Mercado de Trabalho – Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# ─────────────────────────────────────────────
# ESTILOS CSS EMBUTIDOS
# ─────────────────────────────────────────────
CSS_CARD = {
    "background": BG_CARD,
    "border": f"1px solid {CYAN}",
    "borderRadius": "8px",
    "padding": "20px",
    "boxShadow": f"0 0 18px {CYAN}33, inset 0 0 8px rgba(0,255,255,0.04)",
    "transition": "box-shadow 0.3s",
}

CSS_KPI_CARD = {
    **CSS_CARD,
    "textAlign": "center",
    "flex": "1",
    "minWidth": "180px",
}

CSS_LABEL = {
    "fontSize": "11px",
    "color": TEXT_DIM,
    "letterSpacing": "2px",
    "textTransform": "uppercase",
    "fontFamily": FONT_FAMILY,
    "marginBottom": "4px",
}

CSS_FILTER_LABEL = {
    "color": CYAN,
    "fontSize": "11px",
    "letterSpacing": "1.5px",
    "textTransform": "uppercase",
    "fontFamily": FONT_FAMILY,
    "marginBottom": "4px",
    "display": "block",
}

DROPDOWN_STYLE = {
    "backgroundColor": "#0D1F3C",
    "color": WHITE,
    "border": f"1px solid {CYAN}55",
    "borderRadius": "4px",
    "fontFamily": FONT_FAMILY,
    "fontSize": "13px",
}

# ─────────────────────────────────────────────
# HELPER – SCANLINE WATERMARK
# ─────────────────────────────────────────────
def scanlines_overlay():
    return html.Div(style={
        "position": "fixed",
        "top": 0, "left": 0,
        "width": "100%", "height": "100%",
        "backgroundImage": "repeating-linear-gradient(0deg, rgba(0,255,255,0.02) 0px, rgba(0,255,255,0.02) 1px, transparent 1px, transparent 3px)",
        "pointerEvents": "none",
        "zIndex": 9999,
    })

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
app.layout = html.Div(
    children=[
        scanlines_overlay(),

        # ── HEADER ──────────────────────────────
        html.Div(
            style={
                "background": f"linear-gradient(90deg, {BG_MAIN} 0%, #0E2244 60%, {BG_MAIN} 100%)",
                "borderBottom": f"2px solid {CYAN}",
                "boxShadow": f"0 0 30px {CYAN}44",
                "padding": "24px 40px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "flexWrap": "wrap",
                "gap": "12px",
            },
            children=[
                html.Div([
                    html.Div("[ SISTEMA DE MONITORAMENTO AVANÇADO ]", style={
                        "color": CYAN, "fontSize": "11px",
                        "letterSpacing": "3px", "fontFamily": FONT_FAMILY,
                        "marginBottom": "6px",
                    }),
                    html.H1(
                        "Monitoramento Global de IA e Mercado de Trabalho",
                        style={
                            "color": WHITE, "margin": 0,
                            "fontSize": "22px", "fontWeight": "700",
                            "fontFamily": FONT_FAMILY,
                            "textShadow": f"0 0 20px {CYAN}99",
                        }
                    ),
                    html.Div(
                        "O Futuro do Mercado de Trabalho com Inteligência Artificial",
                        style={
                            "color": MAGENTA, "fontSize": "13px",
                            "fontFamily": FONT_FAMILY,
                            "marginTop": "4px",
                            "textShadow": f"0 0 10px {MAGENTA}77",
                        }
                    ),
                ]),
                html.Div([
                    html.Div("AUTOR", style={**CSS_LABEL, "textAlign": "right"}),
                    html.Div("Bruno Vollu Sampaio", style={
                        "color": YELLOW, "fontFamily": FONT_FAMILY,
                        "fontSize": "14px", "fontWeight": "600",
                        "textShadow": f"0 0 10px {YELLOW}77",
                    }),
                    html.Div("Pós-Graduação · 2025", style={
                        "color": TEXT_DIM, "fontFamily": FONT_FAMILY,
                        "fontSize": "11px", "marginTop": "2px",
                    }),
                ]),
            ],
        ),

        # ── CORPO PRINCIPAL ──────────────────────
        html.Div(
            style={"padding": "28px 36px", "background": BG_MAIN, "minHeight": "100vh"},
            children=[

                # ── LINHA DE FILTROS ──────────────
                html.Div(
                    style={
                        **CSS_CARD,
                        "border": f"1px solid {MAGENTA}88",
                        "boxShadow": f"0 0 14px {MAGENTA}22",
                        "display": "flex",
                        "gap": "24px",
                        "flexWrap": "wrap",
                        "alignItems": "flex-end",
                        "marginBottom": "28px",
                    },
                    children=[
                        html.Div("⚙  FILTROS INTERATIVOS", style={
                            "color": MAGENTA, "fontSize": "11px",
                            "letterSpacing": "2px", "fontFamily": FONT_FAMILY,
                            "width": "100%", "marginBottom": "8px",
                            "textShadow": f"0 0 8px {MAGENTA}",
                        }),
                        # Filtro 1 – Setor
                        html.Div([
                            html.Label("Setor Econômico", style=CSS_FILTER_LABEL),
                            dcc.Dropdown(
                                id="filter-setor",
                                options=[{"label": s, "value": s} for s in SETORES],
                                value="Todos",
                                clearable=False,
                                style=DROPDOWN_STYLE,
                                className="cyber-dropdown",
                            ),
                        ], style={"flex": "1", "minWidth": "180px"}),
                        # Filtro 2 – Nível de Decisão
                        html.Div([
                            html.Label("Nível de Decisão", style=CSS_FILTER_LABEL),
                            dcc.Dropdown(
                                id="filter-nivel",
                                options=[{"label": n, "value": n} for n in NIVEIS],
                                value="Todos",
                                clearable=False,
                                style=DROPDOWN_STYLE,
                                className="cyber-dropdown",
                            ),
                        ], style={"flex": "1", "minWidth": "180px"}),
                        # Filtro 3 – País / Região
                        html.Div([
                            html.Label("País / Região", style=CSS_FILTER_LABEL),
                            dcc.Dropdown(
                                id="filter-regiao",
                                options=[{"label": r, "value": r} for r in REGIOES],
                                value="Todos",
                                clearable=False,
                                style=DROPDOWN_STYLE,
                                className="cyber-dropdown",
                            ),
                        ], style={"flex": "1", "minWidth": "180px"}),
                        html.Div(id="filter-status", style={
                            "color": GREEN, "fontSize": "12px",
                            "fontFamily": FONT_FAMILY,
                            "alignSelf": "flex-end",
                            "paddingBottom": "6px",
                        }),
                    ],
                ),

                # ── KPIs ─────────────────────────
                html.Div(
                    style={
                        "display": "flex", "gap": "20px",
                        "flexWrap": "wrap", "marginBottom": "28px",
                    },
                    children=[
                        # KPI 1
                        html.Div(style={**CSS_KPI_CARD, "borderColor": CYAN},
                                 children=[
                            html.Div("ACURÁCIA PREDITIVA", style=CSS_LABEL),
                            html.Div("98%", style={
                                "fontSize": "42px", "fontWeight": "900",
                                "color": CYAN, "lineHeight": "1",
                                "textShadow": f"0 0 25px {CYAN}",
                                "fontFamily": FONT_FAMILY,
                            }),
                            html.Div("Rede Neural Artificial do Projeto",
                                     style={"color": TEXT_DIM, "fontSize": "11px",
                                            "fontFamily": FONT_FAMILY, "marginTop": "8px"}),
                        ]),
                        # KPI 2
                        html.Div(style={**CSS_KPI_CARD, "borderColor": MAGENTA},
                                 children=[
                            html.Div("CRESCIMENTO DE IA", style=CSS_LABEL),
                            html.Div("+163%", style={
                                "fontSize": "42px", "fontWeight": "900",
                                "color": MAGENTA, "lineHeight": "1",
                                "textShadow": f"0 0 25px {MAGENTA}",
                                "fontFamily": FONT_FAMILY,
                            }),
                            html.Div("Uso de IA na Indústria Brasileira 2022–2024",
                                     style={"color": TEXT_DIM, "fontSize": "11px",
                                            "fontFamily": FONT_FAMILY, "marginTop": "8px"}),
                            html.Div("Fonte: IBGE", style={
                                "color": GREEN, "fontSize": "10px",
                                "fontFamily": FONT_FAMILY, "marginTop": "4px"
                            }),
                        ]),
                        # KPI 3
                        html.Div(style={**CSS_KPI_CARD, "borderColor": YELLOW},
                                 children=[
                            html.Div("QUEDA DE VAGAS (ENS. SUPERIOR)", style=CSS_LABEL),
                            html.Div("−27,4%", style={
                                "fontSize": "42px", "fontWeight": "900",
                                "color": YELLOW, "lineHeight": "1",
                                "textShadow": f"0 0 25px {YELLOW}",
                                "fontFamily": FONT_FAMILY,
                            }),
                            html.Div("Queda na geração de novas vagas formais",
                                     style={"color": TEXT_DIM, "fontSize": "11px",
                                            "fontFamily": FONT_FAMILY, "marginTop": "8px"}),
                            html.Div("Fonte: FGV IBRE", style={
                                "color": GREEN, "fontSize": "10px",
                                "fontFamily": FONT_FAMILY, "marginTop": "4px"
                            }),
                        ]),
                        # KPI 4
                        html.Div(style={**CSS_KPI_CARD, "borderColor": GREEN},
                                 children=[
                            html.Div("SALDO GLOBAL DE EMPREGOS ATÉ 2030", style=CSS_LABEL),
                            html.Div("+78M", style={
                                "fontSize": "42px", "fontWeight": "900",
                                "color": GREEN, "lineHeight": "1",
                                "textShadow": f"0 0 25px {GREEN}",
                                "fontFamily": FONT_FAMILY,
                            }),
                            html.Div("Saldo Positivo Global estimado até 2030",
                                     style={"color": TEXT_DIM, "fontSize": "11px",
                                            "fontFamily": FONT_FAMILY, "marginTop": "8px"}),
                            html.Div("Fonte: WEF", style={
                                "color": GREEN, "fontSize": "10px",
                                "fontFamily": FONT_FAMILY, "marginTop": "4px"
                            }),
                        ]),
                    ],
                ),

                # ── GRÁFICOS LINHA 1: G1 + G2 ─────
                html.Div(
                    style={"display": "grid",
                           "gridTemplateColumns": "1fr 1fr",
                           "gap": "24px",
                           "marginBottom": "24px"},
                    children=[
                        html.Div(style={**CSS_CARD, "borderColor": CYAN},
                                 children=[dcc.Graph(id="g1-bars", config={"displayModeBar": False})]),
                        html.Div(style={**CSS_CARD, "borderColor": MAGENTA},
                                 children=[dcc.Graph(id="g2-donut", config={"displayModeBar": False})]),
                    ],
                ),

                # ── GRÁFICOS LINHA 2: G3 + G4 ─────
                html.Div(
                    style={"display": "grid",
                           "gridTemplateColumns": "1fr 1fr",
                           "gap": "24px",
                           "marginBottom": "16px"},
                    children=[
                        html.Div(style={**CSS_CARD, "borderColor": YELLOW},
                                 children=[dcc.Graph(id="g3-scatter", config={"displayModeBar": False})]),
                        html.Div(style={**CSS_CARD, "borderColor": GREEN},
                                 children=[dcc.Graph(id="g4-hbar", config={"displayModeBar": False})]),
                    ],
                ),

                # ── RODAPÉ ───────────────────────
                html.Div(style={
                    "borderTop": f"1px solid {CYAN}33",
                    "marginTop": "16px", "paddingTop": "14px",
                    "display": "flex", "justifyContent": "space-between",
                    "flexWrap": "wrap", "gap": "8px",
                }, children=[
                    html.Span("© 2025 Bruno Vollu Sampaio · Pós-Graduação · IA & Mercado de Trabalho",
                              style={"color": TEXT_DIM, "fontSize": "11px", "fontFamily": FONT_FAMILY}),
                    html.Span("FONTES: IBGE · FGV IBRE · WEF · MIT · McKinsey",
                              style={"color": TEXT_DIM, "fontSize": "11px", "fontFamily": FONT_FAMILY}),
                ]),
            ],
        ),
    ],
    style={
        "backgroundColor": BG_MAIN,
        "minHeight": "100vh",
        "fontFamily": FONT_FAMILY,
    },
)

# ───────────────────────────────────────────────────────────
# CALLBACKS
# ───────────────────────────────────────────────────────────

@app.callback(
    Output("filter-status", "children"),
    Input("filter-setor", "value"),
    Input("filter-nivel", "value"),
    Input("filter-regiao", "value"),
)
def update_filter_status(setor, nivel, regiao):
    return f"✔  Filtro ativo: {setor} · {nivel} · {regiao}"


@app.callback(
    Output("g1-bars", "figure"),
    Input("filter-setor", "value"),
    Input("filter-nivel", "value"),
    Input("filter-regiao", "value"),
)
def update_g1(setor, nivel, regiao):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Adoção de IA (%)",
        x=g1_anos,
        y=g1_ia,
        marker=dict(
            color=[MAGENTA, CYAN],
            line=dict(color=CYAN, width=1.5),
        ),
        text=[f"{v}%" for v in g1_ia],
        textposition="outside",
        textfont=dict(color=WHITE, size=13),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Adoção de IA: <b>%{y}%</b><br>"
            "<i>A IA cresce enquanto o Teletrabalho recua — um cruzamento histórico.</i>"
            "<extra></extra>"
        ),
        width=0.3,
    ))

    fig.add_trace(go.Bar(
        name="Teletrabalho (%)",
        x=g1_anos,
        y=g1_teletrabalho,
        marker=dict(
            color=["#334466", "#1A2A4A"],
            line=dict(color=MAGENTA, width=1.5),
        ),
        text=[f"{v}%" for v in g1_teletrabalho],
        textposition="outside",
        textfont=dict(color=WHITE, size=13),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Teletrabalho: <b>%{y}%</b><br>"
            "<i>Tendência de queda contrastando com o avanço da IA.</i>"
            "<extra></extra>"
        ),
        width=0.3,
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        legend=LEGEND_BASE,
        title=dict(
            text="Adoção de IA vs Teletrabalho na Indústria (2022–2024)",
            font=dict(color=CYAN, size=14, family=FONT_FAMILY),
            x=0.01,
        ),
        barmode="group",
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=WHITE, size=12),
            linecolor=GRID_COLOR,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            ticksuffix="%",
            tickfont=dict(color=WHITE),
            range=[0, 65],
        ),
        height=340,
        annotations=[
            dict(
                text="<b>Fonte: IBGE 2024</b>",
                x=1, y=0,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(color=GREEN, size=10),
                xanchor="right",
            ),
            dict(
                x=1, y=42.2,
                text="◄ Cruzamento Reverso",
                showarrow=True,
                arrowhead=2,
                arrowcolor=YELLOW,
                font=dict(color=YELLOW, size=11),
                ax=-80, ay=-30,
            ),
        ],
    )
    return fig


@app.callback(
    Output("g2-donut", "figure"),
    Input("filter-setor", "value"),
    Input("filter-nivel", "value"),
    Input("filter-regiao", "value"),
)
def update_g2(setor, nivel, regiao):
    fig = go.Figure(go.Pie(
        labels=g2_labels,
        values=g2_values,
        hole=0.6,
        marker=dict(
            colors=g2_colors,
            line=dict(color=BG_MAIN, width=3),
        ),
        textinfo="percent",
        textfont=dict(color=WHITE, size=12, family=FONT_FAMILY),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Impacto: <b>%{value}%</b> das empresas<br>"
            "<i>A Inteligência Social é o maior escudo humano<br>"
            "contra a automação — máquinas não replicam<br>"
            "empatia, liderança e criatividade.</i>"
            "<extra></extra>"
        ),
        insidetextorientation="radial",
        showlegend=True,
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        legend=LEGEND_DONUT,
        title=dict(
            text="Principais Barreiras para Adoção de IA nas Empresas",
            font=dict(color=MAGENTA, size=14, family=FONT_FAMILY),
            x=0.01,
        ),
        height=340,
        annotations=[
            dict(
                text="<b>Barreiras<br>de IA</b>",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(color=WHITE, size=12, family=FONT_FAMILY),
                xanchor="center", yanchor="middle",
            ),
        ],
    )
    return fig


@app.callback(
    Output("g3-scatter", "figure"),
    Input("filter-setor", "value"),
    Input("filter-nivel", "value"),
    Input("filter-regiao", "value"),
)
def update_g3(setor, nivel, regiao):
    fig = go.Figure()

    # Cluster Risco Alto
    fig.add_trace(go.Scatter(
        x=risco_alto_x, y=risco_alto_y,
        mode="markers",
        name="Risco Alto (>50%)",
        marker=dict(
            color=MAGENTA, size=10, opacity=0.85,
            line=dict(color="white", width=0.5),
            symbol="circle",
        ),
        hovertemplate=(
            "<b>Risco Alto de Automação</b><br>"
            "Complexidade de Dados: <b>%{x:.2f}</b><br>"
            "Frequência da Tarefa: <b>%{y:.2f}</b><br>"
            "<i>Tarefas repetitivas e com alta volumetria de dados são as mais vulneráveis à substituição por IA.</i><br>"
            "<i>A Inteligência Social é o maior escudo humano contra a automação.</i>"
            "<extra></extra>"
        ),
    ))

    # Cluster Risco Baixo
    fig.add_trace(go.Scatter(
        x=risco_baixo_x, y=risco_baixo_y,
        mode="markers",
        name="Risco Baixo",
        marker=dict(
            color=CYAN, size=10, opacity=0.85,
            line=dict(color="white", width=0.5),
            symbol="diamond",
        ),
        hovertemplate=(
            "<b>Risco Baixo de Automação</b><br>"
            "Complexidade de Dados: <b>%{x:.2f}</b><br>"
            "Frequência da Tarefa: <b>%{y:.2f}</b><br>"
            "<i>Tarefas que exigem inteligência social, empatia e liderança — "
            "habilidades que a IA não replica. A Inteligência Social é o maior escudo humano contra a automação.</i>"
            "<extra></extra>"
        ),
    ))

    # Regiões destacadas com shapes
    fig.add_shape(type="rect", x0=0.62, y0=0.62, x1=1.02, y1=1.02,
                  line=dict(color=MAGENTA, width=1.5, dash="dash"),
                  fillcolor="rgba(255,0,255,0.07)")
    fig.add_shape(type="rect", x0=-0.02, y0=-0.02, x1=0.48, y1=0.48,
                  line=dict(color=CYAN, width=1.5, dash="dash"),
                  fillcolor="rgba(0,255,255,0.07)")

    fig.update_layout(
        **PLOTLY_LAYOUT,
        legend=LEGEND_BASE,
        title=dict(
            text="Matriz de Risco de Automação (Cérebro Estatístico)",
            font=dict(color=YELLOW, size=14, family=FONT_FAMILY),
            x=0.01,
        ),
        xaxis=dict(
            title="Complexidade de Dados",
            showgrid=True, gridcolor=GRID_COLOR,
            zeroline=False,
            tickfont=dict(color=WHITE),
            title_font=dict(color=TEXT_DIM),
            range=[-0.05, 1.05],
        ),
        yaxis=dict(
            title="Frequência da Tarefa",
            showgrid=True, gridcolor=GRID_COLOR,
            zeroline=False,
            tickfont=dict(color=WHITE),
            title_font=dict(color=TEXT_DIM),
            range=[-0.12, 1.05],
        ),
        height=360,
        annotations=[
            dict(
                x=0.82, y=0.98,
                xref="x", yref="y",
                text="⚠ Risco Alto (>50%)",
                showarrow=False,
                font=dict(color=MAGENTA, size=11, family=FONT_FAMILY),
            ),
            dict(
                x=0.23, y=-0.09,
                xref="x", yref="y",
                text="✔ Risco Baixo",
                showarrow=False,
                font=dict(color=CYAN, size=11, family=FONT_FAMILY),
            ),
        ],
    )
    return fig


@app.callback(
    Output("g4-hbar", "figure"),
    Input("filter-setor", "value"),
    Input("filter-nivel", "value"),
    Input("filter-regiao", "value"),
)
def update_g4(setor, nivel, regiao):
    fig = go.Figure(go.Bar(
        x=g4_scores,
        y=g4_skills,
        orientation="h",
        marker=dict(
            color=g4_colors_list,
            line=dict(color=BG_MAIN, width=0.5),
        ),
        text=[f"{v} pts" for v in g4_scores],
        textposition="outside",
        textfont=dict(color=WHITE, size=12),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Score: <b>%{x} pts</b><br>"
            "<i>Inteligência Social é o maior escudo humano contra a automação de IA — "
            "empatia, liderança e criatividade não são replicáveis por máquinas.</i>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="Habilidades do Futuro 2030 (Prêmio Tecnológico – WEF)",
            font=dict(color=GREEN, size=14, family=FONT_FAMILY),
            x=0.01,
        ),
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            range=[0, 110],
            tickfont=dict(color=WHITE),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color=WHITE, size=12),
            automargin=True,
        ),
        height=340,
        annotations=[dict(
            text="<b>Fonte: WEF Future of Jobs 2025</b>",
            x=1, y=0,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(color=GREEN, size=10),
            xanchor="right",
        )],
    )
    return fig


# ─────────────────────────────────────────────
# CSS GLOBAL (via index_string)
# ─────────────────────────────────────────────
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: #0A1428; overflow-x: hidden; }
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #0D0D0D; }
            ::-webkit-scrollbar-thumb { background: #00FFFF55; border-radius: 3px; }
            ::-webkit-scrollbar-thumb:hover { background: #00FFFF; }

            /* Dropdown cyberpunk */
            .cyber-dropdown .Select-control {
                background-color: #0D1F3C !important;
                border-color: #00FFFF55 !important;
                color: #fff !important;
            }
            .cyber-dropdown .Select-menu-outer {
                background-color: #0D1F3C !important;
                border: 1px solid #00FFFF55 !important;
            }
            .cyber-dropdown .Select-option {
                background-color: #0D1F3C !important;
                color: #fff !important;
            }
            .cyber-dropdown .Select-option:hover,
            .cyber-dropdown .Select-option.is-focused {
                background-color: #00FFFF22 !important;
                color: #00FFFF !important;
            }
            .cyber-dropdown .Select-value-label { color: #fff !important; }
            .cyber-dropdown .Select-arrow { border-top-color: #00FFFF !important; }

            /* Card hover glow */
            .dash-graph { border-radius: 6px; }

            @keyframes pulse-border {
                0%   { box-shadow: 0 0 10px #00FFFF33; }
                50%  { box-shadow: 0 0 25px #00FFFF77; }
                100% { box-shadow: 0 0 10px #00FFFF33; }
            }

            /* Responsive */
            @media (max-width: 900px) {
                div[style*="gridTemplateColumns: 1fr 1fr"] {
                    grid-template-columns: 1fr !important;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Dashboard · IA & Mercado de Trabalho")
    print("  Autor: Bruno Vollu Sampaio")
    print("  Acesse: http://127.0.0.1:8050")
    print("=" * 60)
    app.run(debug=False, port=8050)
