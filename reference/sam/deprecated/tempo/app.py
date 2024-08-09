import streamlit as st
import random
import plotly.express as px
import pandas as pd
#! streamlit compoentns

queue = []
ranges = {
  "danceability": 0.436,
  "energy": 0.536,
  "loudness": -9.377,
  "speechiness": 0.126,
  "acousticness": 0.615,
  "instrumentalness": 0.981,
  "liveness": 0.18,
  "valence": 0.435,
  "tempo": 96.955,
  #"duration_ms": 186804

}

# https://towardsdatascience.com/creating-interactive-radar-charts-with-python-2856d06535f6
def radar_chart(val):  
    df = pd.DataFrame(dict(
    r=[
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val),
       random.randint(0,val)
    ],
    theta=[*ranges]))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    st.write(fig)


if __name__ == '__main__':
    # dan_l = st.slider('Select value',0,10,1)
    for name in [
        # 'dan',
        # 'erg',
        # 'lou',
        # 'spc',
        # 'aco',
        # 'ins',
        # 'liv',
        # 'val',
        'tmp'
    ]:
        globals()[name+'_l'] = st.slider(name+'_l',0,10,1, key=name+'_l')
        globals()[name+'_h'] = st.slider(name+'_h',0,10,1, key=name+'_h')
    # print(*globals)
    # radar_chart(val)
    st.write(globals()[name+'_l'], globals()[name+'_h'])