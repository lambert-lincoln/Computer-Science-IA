import plotly.graph_objects as go
import data_fetcher as df
import pandas as pd

class Figure():
    
    def make_fig(self, df: pd.DataFrame):
        colors = ['#A23B72', '#F18F01', '#C73E1D']
        fig = go.Figure()
        
        ratio_col = None
        sma_cols = []
        for col in df.columns:
            if "ratio" in col.lower() and "sma" not in col.lower():
                ratio_col = col
            elif "sma" in col.lower():
                sma_cols.append(col)
            
        if not ratio_col:
            raise ValueError("No ratio to plot")
        
        df_filtered = df.iloc[99:].copy()
        
        fig.add_trace(go.Scatter(
            x=df_filtered.index,
            y=df_filtered[ratio_col],
            name = ratio_col,
            line=dict(color='royalblue', width=2.5),
        ))
        
        for sma_col, color in zip(sma_cols, colors):
            fig.add_trace(go.Scatter(
                x=df_filtered.index,
                y=df_filtered[sma_col],
                name=sma_col,
                line=dict(color=color, width=1.5),
            ))
        
        fig.update_layout(
            title=f"{ratio_col} Over Time",
            xaxis_title="Date",
            yaxis_title=ratio_col,
            template="plotly_white",
            legend_title="Metric",
            hovermode="x unified",
            height=800,
        )
        
        return fig
    
    def plot_chart(self, df: pd.DataFrame):
        
        sma_col = []
        colors = ['#A23B72', '#F18F01', '#C73E1D']
        fig = go.Figure()
        
        if df.columns.empty:
            raise ValueError(f"No data to plot chart")
        
        fig = go.Figure(go.Candlestick(
            x=df.index,
            open=df["Open"],
            close=df["Close"],
            high=df["High"],
            low=df["Low"],
        ))
        
        for col in df.columns:
            if "sma" in col.lower():
                sma_col.append(col)
        
        for col, color in zip(sma_col, colors):
            if "sma" in col.lower():
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=col,
                    line=dict(color=color, width=1.5),
                ))
        
        fig.update_layout(
            title="Price Over Time",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_white",
            hovermode="x unified",
            height=800,
        )
        
        return fig