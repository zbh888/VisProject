import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import webbrowser
import os
from shapely.geometry import Polygon
import sys
from argparse import ArgumentParser
from gooey import Gooey
from gooey import GooeyParser
pd.options.mode.chained_assignment = None  # default='warn'

# Define functions
def read(file):
    new = {}
    fout = file
    fo = open(fout, "r")

    for row in fo:
        if len(row.strip()) == 0:
            continue
        r = row.split('>>>')
        key = r[0].strip()
        value = r[1].strip()
        new[key] = float(value)
    fo.close()
    return new

def gen_color(grade, single_color):
    norm = plt.Normalize(grade.min(), grade.max())
    norm_grade = norm(grade)
    
    
    interval = np.hstack([np.linspace(0, 0.43), np.linspace(0.57, 1)])
    colors = plt.cm.bwr_r(interval)
    if single_color:
        interval = np.hstack([np.linspace(0.2, 1)])
        colors = plt.cm.Greens(interval)
    cmap = LinearSegmentedColormap.from_list('name', colors)
    
    color = cmap(norm_grade)
    return [rgb2hex(x) for x in color]

def gen_map(area_name="world", absolute_analysis_mode=False, single_color=False, which_grade = "Plain Grade"):
    world = prepare_world(which_grade)
    area = world.copy()
    # Parameter 1, Select Area
    if area_name == "Asia":
        area = world.query('continent.isin(["Asia"])')
    if area_name == "Europe":
        area = world.query('continent.isin(["Europe"])')
    if area_name == "South America":
        area = world.query('continent.isin(["South America"])')
    if area_name == "North America":
        area = world.query('continent.isin(["North America"])')
        
    area_ranked = area[area['grade'] > 0.01]
    area_not_ranked = area[area['grade'] < 0.01]
    rank = area_ranked['grade'].rank(method='min', ascending=False)
    area_ranked['rank'] = rank
    t = 'Stamen Watercolor'
    if absolute_analysis_mode:
        t = 'CartoDB dark_matter'
    w = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    m = w.explore(
        min_zoom = 2,
        max_zoom = 5,
        zoom_start = 2,
        tooltip = False,
        highlight = False,
        tiles=t,
        color = 'black'
    )
    
    
    m = area_ranked.explore(
        m = m,
        min_zoom = 2,
        max_zoom = 5,
        zoom_start = 2,
        tiles=t,
        color=gen_color(area_ranked['grade'].to_numpy(), single_color),
        tooltip = ['continent', 'rank', 'name', 'grade'],
        style_kwds={
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.9
        },
        highlight_kwds={
            'fillColor': 'gold',
            'fillOpacity': 0.8
        }
    )
    
    m = area_not_ranked.explore(
        min_zoom = 2,
        max_zoom = 5,
        zoom_start = 2,
        tiles=t,
        color='grey',
        tooltip = ['continent', 'name'],
        style_kwds={
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.9
        },
        m = m,
        highlight_kwds={
            'fillColor': 'gold',
            'fillOpacity': 0.8
        }
    )
    m.save('MyMap.html')
    webbrowser.open_new_tab('file://' + os.path.realpath("MyMap.html"))
    return m

def prepare_world(which_grade):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    l = 0.6
    lon_point_list = [105-l, 105-l, 105+l, 105+l] #x
    lat_point_list = [0.5-l, 0.5+l, 0.5+l, 0.5-l] #y

    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
    polygon = gpd.GeoDataFrame(index=[0], geometry=[polygon_geom]) 
    world.loc[177] = [56860000.0,'Asia','Singapore','SGP',0,polygon_geom]

    lon_point_list = [15-l, 15-l, 15+l, 15+l] #x
    lat_point_list = [35-l, 35+l, 35+l, 35-l] #y

    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
    polygon = gpd.GeoDataFrame(index=[0], geometry=[polygon_geom]) 
    world.loc[178] = [525285.0,'Europe','Malta','MLT',0,polygon_geom]
    
    c2g = read('grade.txt')
    if which_grade == "Grade relative to research GDP":
        c2g = read('grade_rgdp.txt')
    if which_grade == "Grade relative to population":
        c2g = read('grade_pop.txt')
    n = len(world['name'])
    grade_column = np.array([0.0] * n)
    world['grade'] = grade_column
    for i in world.index:
        c_name = world['name'].iloc[i]
        if c_name in c2g:
            world.at[i, 'grade'] = c2g[c_name]
    return world

@Gooey(return_to_config= True)
def main():
    parser = GooeyParser()
    gooey_options={'show_border': True,
                   'columns': 1-10 }
    search_group = parser.add_argument_group("Continent Options",
                                             gooey_options=gooey_options)
    search_group.add_argument(
        "-c",
        "--contigent_name",
        metavar='Choose one area for ranking',
        choices=['The World', 'Asia', 'Europe', 'South America', 'North America'],
        type = str,
        required=True,
        help="Focus on one continent"
    )
    search_group2 = parser.add_argument_group("Grade Options",
                                             gooey_options=gooey_options)
    search_group2.add_argument(
        "-g",
        "--grade_type",
        metavar='Choose one type of grade for ranking',
        choices=['Plain Grade', 'Grade relative to research GDP', 'Grade relative to population'],
        type = str,
        required=True,
        help="Focus on one type of grade"
    )
    parser.add_argument(
        "-d",
        "--dark_mode",
        metavar='Dark Mode',
        widget='CheckBox',
        action='store_true',
        required=False,
        help="Turn on the dark backgroud mode"
    )
    parser.add_argument(
        "-s",
        "--single_color",
        metavar='Single Color',
        widget='CheckBox',
        action='store_true',
        required=False,
        help="Turn on the single color mode"
    )
    args = parser.parse_args()
    gen_map(args.contigent_name, args.dark_mode, args.single_color, args.grade_type)

if __name__ == "__main__":
    main()
