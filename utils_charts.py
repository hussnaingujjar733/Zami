import plotly.graph_objects as go

def generate_financial_pie(estimated_subsidy, net_cost, t_subsidy, t_charge):
    """Generates the premium dynamic doughnut/pie chart for capital deployment metrics"""
    fig = go.Figure(data=[go.Pie(
        labels=[t_subsidy, t_charge], 
        values=[estimated_subsidy, net_cost], 
        hole=.6, 
        marker=dict(colors=['#22c55e', '#dc2626']), 
        textinfo='percent', 
        hoverinfo='label+value', 
        showlegend=False
    )])
    fig.update_layout(
        height=180, 
        margin=dict(l=10, r=10, t=10, b=10), 
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def generate_five_year_trajectory(active_roi):
    """Calculates non-linear compound trajectories for unrenovated vs renovated assets"""
    years = ["2026", "2027", "2028", "2029", "2030", "2031"]
    base_market_value = 300000
    renovated_curve = [base_market_value * (1 + (active_roi/100) + (i*0.02)) for i in range(6)]
    unrenovated_curve = [base_market_value * (1 - (i * 0.035)) for i in range(6)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=renovated_curve, name="Asset Rénové", line=dict(color='#22c55e', width=4)))
    fig.add_trace(go.Scatter(x=years, y=unrenovated_curve, name="Passoire Non-Rénovée", line=dict(color='#dc2626', width=3, dash='dash')))
    fig.update_layout(
        height=240, 
        margin=dict(l=40, r=20, t=10, b=20), 
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), 
        xaxis=dict(color="#94a3b8"), 
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#94a3b8")
    )
    return fig