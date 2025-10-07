import plotly.graph_objects as go
import data_fetcher as df
import pandas as pd

class Figure():
    
    def make_fig(self, df: pd.DataFrame):
        fig = go.Figure()
        
        cols = df.column.to_list()
        
        fig.add_trace(go.Scatter(
            x=df[cols[0]].iloc[99:],
            y=df[cols[1]].iloc[99:],
            name = cols[1],
            line=dict(color='#2E86AB', width=2),
        ))
        