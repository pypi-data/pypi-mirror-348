import dash
from dash import dcc, html, Output, Input, State
import plotly.graph_objects as go
import numpy as np
from .utils import vector_MAE

class overall_plot():
    def __init__(self, y):
        self.x = np.arange(16)
        self.backend = y["backend"]
        self.y0, self.y1, self.y2 = y["Statevector"], y["noisy_input"], y["Autoencoder"]
        self.trace_a = go.Bar(name="Statevector", x=self.x, y=self.y0, marker_color='rgba(214, 39, 40, 1)')
        self.trace_b = go.Bar(name=y["backend"], x=self.x, y=self.y1, marker_color='rgba(31, 119, 180, 0.8)')
        self.trace_c = go.Bar(name="Autoencoder", x=self.x, y=self.y2, marker_color='rgba(44, 160, 44, 0.5)')
    def plot_result(self):
        def create_bar_chart(show_a=True, show_b=False, show_c=False):
            fig = go.Figure()
            if show_a:
                fig.add_trace(self.trace_a)
            if show_b:
                fig.add_trace(self.trace_b)
            if show_c:
                fig.add_trace(self.trace_c)
        
            fig.add_trace(go.Bar(
                x=self.x,
                y=[0]*len(self.x),
                marker_color='rgba(0,0,0,0)',
                showlegend=False,
                hoverinfo='skip'
            ))
            fig.update_layout(
                title="Probability for each basis vector",
                title_x=0.5,
                barmode="overlay",
                xaxis=dict(title="Basis vector in decimal"),
                yaxis=dict(title="Probability", range=[0, 1]),
                transition=dict(duration=500, easing='cubic-in-out'),
                showlegend=False,
                hovermode="x unified"
            )
            return fig

        def create_noise_fig():
            mae_noisy = vector_MAE(self.y0, self.y1)
            mae_denoised = vector_MAE(self.y0, self.y2)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Unmitigated", "Mitigated"],
                y=[mae_noisy, mae_denoised],
                marker_color="rgba(255, 206, 86, 0.8)"
            ))
            fig.update_layout(
                title="Average Noise-level",
                title_x=0.5,
                yaxis=dict(title="MAE", range=[0, max(mae_noisy, mae_denoised) * 1.2]),
                xaxis=dict(title=""),
                showlegend=False
            )
            return fig
        def button_style():
            return {
                "background": "none",
                "border": "none",
                "color": "black",
                "fontSize": "16px",
                "margin": "0 10px",
                "cursor": "pointer"
            }
            
        app = dash.Dash(__name__)
        app.layout = html.Div([
            html.Div([
                dcc.Graph(id='bar-chart', figure=create_bar_chart(), mathjax=True),
                html.Div([
                    html.Button("🟥 Theorem", id='btn-a', n_clicks=0, style=button_style()),
                    html.Button(f"🟦 {self.backend}", id='btn-b', n_clicks=0, style=button_style()),
                    html.Button("🟩 Autoencoder", id='btn-c', n_clicks=0, style=button_style())
                ], style={"textAlign": "center", "marginBottom": "10px"})
            ], style={"display": "inline-block", "width": "60%", "verticalAlign": "top"}),
        
            html.Div([
                dcc.Graph(id='noise-graph', figure=create_noise_fig())
            ], style={"display": "inline-block", "width": "40%", "verticalAlign": "top"}),
        
            dcc.Store(id='visible-traces', data={'A': True, 'B': False, 'C': False})
        ])
        @app.callback(
            Output('bar-chart', 'figure'),
            Output('visible-traces', 'data'),
            Input('btn-a', 'n_clicks'),
            Input('btn-b', 'n_clicks'),
            Input('btn-c', 'n_clicks'),
            State('visible-traces', 'data'),
            prevent_initial_call=True
        )
        def toggle_traces(n_a, n_b, n_c, visibility):
            ctx = dash.callback_context
            btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if btn_id == 'btn-a':
                visibility['A'] = not visibility['A'] 
            elif btn_id == 'btn-b':
                visibility['B'] = not visibility['B']
            elif btn_id == 'btn-c':
                visibility['C'] = not visibility['C']
            fig = create_bar_chart(
                show_a=visibility['A'],
                show_b=visibility['B'],
                show_c=visibility['C']
            )
            return fig, visibility

        app.run(debug=True)

    def plot_MAE(self, data):
        mae_noisy = vector_MAE(self.y0, self.y1)
        mae_denoised = vector_MAE(self.y0, self.y2)
        mae_data = vector_MAE(self.y0, data)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Unmitigated", "Mitigated(Autoencoder)", "Mitigated(mitigator)"],
            y=[mae_noisy, mae_denoised, mae_data],
            marker_color="rgba(255, 206, 86, 0.8)"
        ))
        fig.update_layout(
            title="Average Noise-level",
            title_x=0.5,
            yaxis=dict(title="MAE", range=[0, max(mae_noisy, mae_denoised, mae_data) * 1.2]),
            xaxis=dict(title=""),
            showlegend=False,
            hovermode="x unified"
        )
        fig.show() 
        
        
