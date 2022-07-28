import utils.ntg_data as ntg_data
import pandas as pd
import plotly.express as px
import utils.ntg_colors as ntg_colors

df = ntg_data.load_data()

for key, it in zip(df, range(len(df))):
    print(it/len(df),
        px.colors.sample_colorscale(ntg_colors.ntg, it/len(df))
    )
