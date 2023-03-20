import os
import mysql.connector
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objects as go

spectral_colors = {
    'O': 'rgb(156, 176, 255)',
    'B': 'rgb(162, 185, 255)',
    'A': 'rgb(248, 247, 255)',
    'F': 'rgb(255, 243, 236)',
    'G': 'rgb(255, 227, 180)',
    'K': 'rgb(255, 190, 111)',
    'M': 'rgb(255, 103, 15)',
}

def connect_to_database():
    cnx = mysql.connector.connect(user=os.environ['mysql_username'],
                                  password=os.environ['mysql_password'],
                                  host=os.environ['mysql_host'],
                                  database=os.environ['mysql_db'])
    return cnx

def read_star_data(cnx):
    query = "SELECT x, y, z, iauname, altname, bf, gl, absmag, dist, spect FROM hyg WHERE dist < 35"
    df = pd.read_sql(query, cnx)
    return df

def create_3d_star_map(df):
    fig = go.Figure()

    # Fill missing values in 'spect' column with an empty string
    df['spect'] = df['spect'].fillna('')

    for spectral_type, color in spectral_colors.items():
        star_mask = df['spect'].str.startswith(spectral_type)
        star_data = df[star_mask]

        if star_data.empty:
            continue

        marker_sizes = normalize_marker_size(star_data['absmag'])
        marker_sizes = np.nan_to_num(marker_sizes, nan=2)

        scatter = go.Scatter3d(x=star_data['x'],
                               y=star_data['y'],
                               z=star_data['z'],
                               mode='markers+text',
                               marker=dict(size=marker_sizes, color=color),
                               name=spectral_type,
                               textposition="top center")

        # Add text labels for bright stars
        scatter.text = star_data.apply(lambda row: row['name']
                                       if row['absmag'] < 8.0 else '',
                                       axis=1)

        fig.add_trace(scatter)

    fig.update_layout(scene=dict(xaxis_title='X (light years)',
                                 xaxis=dict(backgroundcolor='black', gridcolor='grey', showbackground=True),
                                 yaxis_title='Y (light years)',
                                 yaxis=dict(backgroundcolor='black', gridcolor='grey', showbackground=True),
                                 zaxis_title='Z (light years)',
                                 zaxis=dict(backgroundcolor='black', gridcolor='grey', showbackground=True)),
                      plot_bgcolor='black')

    return fig




def save_plot(fig):
    plot_file = 'output/star_map.html'
    pyo.plot(fig, filename=plot_file, auto_open=True)

def normalize_marker_size(sizes):
    sizes_no_nan = sizes.dropna()
    min_val, max_val = min(sizes_no_nan), max(sizes_no_nan)
    min_marker_size, max_marker_size = 2, 12
    normalized_sizes = (sizes - min_val) / (max_val - min_val) * (max_marker_size - min_marker_size) + min_marker_size
    normalized_sizes = max_marker_size - normalized_sizes + min_marker_size
    return normalized_sizes


# Helper function to get the combined name from the available columns
def get_combined_name(row):
  for col in ['iauname', 'altname', 'bf', 'gl']:
    if not pd.isna(row[col]):
      return row[col]
  return ''
  
def main():
    cnx = connect_to_database()
    df = read_star_data(cnx)
    cnx.close()
  
    df = df.assign(name=df.apply(get_combined_name, axis=1))
    fig = create_3d_star_map(df)
    save_plot(fig)

if __name__ == "__main__":
    main()
