from sector_creator import create_sector_kml
import pandas as pd


# example 1
filename = 'example_greenwich.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'x','y','angle','dis','sd',name='name',output='POLYGONS_GREENWICH')


# example 2
filename = 'example_new_york_harbor.csv'
data = pd.read_csv(filename)
name = 'name'
x_field = 'x'
y_field = 'y'
angle = 'angle'
distance = 'distance'
std = 'sd'
create_sector_kml(data,x_field,y_field,angle,distance,std,name='name',output='POLYGONS_NYH')


# example 3
filename = 'example_paris.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'x_point','y_point','degree','dis','std',name='nickname',output='POLYGONS_PARIS')


# example 4
filename = 'example_Sydney.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'X','Y','degre','dist','sd',name='place',output='POLYGONS_SYDNEY')