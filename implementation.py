from sector_creator import create_sector_kml
import pandas as pd


# example 1
filename = 'Examples\example_greenwich.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'x','y','angle','dis','sd',name='name',output='Outputs\POLYGONS_GREENWICH')


# example 2
filename = 'Examples\example_new_york_harbor.csv'
data = pd.read_csv(filename)
name = 'name'
x_field = 'x'
y_field = 'y'
angle = 'angle'
distance = 'distance'
std = 'sd'
create_sector_kml(data,x_field,y_field,angle,distance,std,name='name',output='Outputs\POLYGONS_NYH')


# example 3
filename = 'Examples\example_paris.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'x_point','y_point','degree','dis','std',name='nickname',output='Outputs\POLYGONS_PARIS')


# example 4
filename = 'Examples\example_Sydney.csv'
data = pd.read_csv(filename)
create_sector_kml(data,'X','Y','degre','dist','sd',name='place',output='Outputs\POLYGONS_SYDNEY')
