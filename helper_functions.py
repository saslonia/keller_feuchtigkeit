from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

def custom_cmap_wall_humidity():
    # Define color segments and corresponding colors with smooth gradient
    # https://www.ausbaupraxis.de/feucht-oder-froehlich-die-feuchtemessung-17112021
    # bis 40 Skalenanteile: trockener Baustoff
    # 40 – 80 Skalenanteile: mäßig feucht (Material-Ausgleichsfeuchte)
    # 80 – 100 Skalenanteile: erhöhte Baustofffeuchte
    # 100 – 150 Skalenanteile: durchfeuchtetes Bauteil
    colors = [
        (0, 'darkgreen'),
        (20/200, 'green'),
        (40/200, 'greenyellow'),
        (50/200, 'yellow'),
        (80/200, 'gold'),
        (90/200, 'orange'),
        (100/200, 'darkorange'),
        (105/200, 'red'),
        (150/200, 'darkred'),
        (1, 'black')
    ]

    # Create colormap
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)

    return cmap

def create_plots_wall(df, room, wall, with_scatter=True, with_x_labels=True):
    # constants
    room_height=250

    # filter df
    df_wall = df[(df["room"] == room) & (df["wall"] == wall)]

    # data for plots
    x = df_wall["wall_x_coord_cm"]
    y = df_wall["wall_y_coord_cm"]
    z_humidity = df_wall["wall_humidity_digits"]
    z_temperature = df_wall["wall_temperature_degC"]

    # Define grid
    xi = np.linspace(x.min(), x.max(), 1000)
    yi = np.linspace(0, room_height, 1000)

    # Perform interpolation
    zi_humidity = griddata((x, y), z_humidity, (xi[None, :], yi[:, None]), method='linear')
    zi_temperature = griddata((x, y), z_temperature, (xi[None, :], yi[:, None]), method='linear')

    # Plot heat map for humidity
    plt.figure(figsize = (x.max()/50, room_height/50))
    plt.imshow(
        zi_humidity,
        extent=(x.min(), x.max() if x.max() - x.min() >= 30 else x.min() + 30, 0, room_height),
        origin='lower',
        cmap=custom_cmap_wall_humidity(),
        aspect='equal',
        vmin=0,
        vmax=200
    )
    plt.colorbar(label="Feuchtigkeit [digits]", shrink=0.8)
    if with_x_labels:
        plt.xlabel('X')
    else:
        plt.xticks([])
    plt.ylabel('Y')
    if with_scatter:
        plt.scatter(x, y, color='grey', marker='x')
    plt.title(f"Feuchtigkeit: {room}, {wall}")
    plt.show()

    # Plot heat map for temperature
    plt.figure(figsize = (x.max()/50, room_height/50))
    plt.imshow(
        zi_temperature,
        extent=(x.min(), x.max() if x.max() - x.min() >= 30 else x.min() + 30, 0, room_height),
        origin='lower',
        cmap='RdBu_r',
        aspect='equal',
        vmin=10,
        vmax=25
    )
    plt.colorbar(label='Temperatur [°C]', shrink=0.8)
    if with_x_labels:
        plt.xlabel('X')
    else:
        plt.xticks([])
    plt.ylabel('Y')
    if with_scatter:
        plt.scatter(x, y, color='grey', marker='x')
    plt.title(f"Temperatur: {room}, {wall}")
    plt.show()