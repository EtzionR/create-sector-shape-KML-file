# Create by Etzion Harari
# https://github.com/EtzionR

# Load libraries:
from utm import from_latlon as to_utm, to_latlon as to_geo
from numpy import cos, sin, pi
from simplekml import Kml


def define_zone(x,y):
    """
    define the utm zone and the up/down parameters
    :param x: x coordinates
    :param y: y coordinates
    :return: new up/down & utm-zone fields
    """
    updown, zone = [], []
    for i in range(len(x)):
        updown.append('U') if y[i]>0 else updown.append('D')
        zone.append(31+int(x[i]//6))
    return updown,zone

def data_preparation(data, x_field, y_field):
    """
    define utm & updown fields and convert the x/y coordinates to utm
    :param data: the input pandas dataframe
    :param x_field: x array name
    :param y_field: y array name
    """
    x, y = data[x_field], data[y_field]
    data['up_down'], data['utm_zone'] = define_zone(x, y)
    x_utm, y_utm = [], []
    for i in range(len(x)):
        x_, y_ = to_utm(y[i], x[i], data['utm_zone'][i], data['up_down'][i])[:2]
        y_utm.append(y_)
        x_utm.append(x_)
    data['x_utm'], data['y_utm'] = x_utm, y_utm

def find_edge_xy(x,y,z,u,r=0,d=0):
    """
    find edge point by the input parameters
    and convert it to wgs84 geo dd
    :param x: x coordinates
    :param y: y coordinates
    :param z: utm zone
    :param u: up/down
    :param r: radian
    :param d: distance from the original point
    :return: converted new x&y
    """
    x_new = x + (d*cos(r))
    y_new = y + (d*sin(r))
    return to_geo(x_new, y_new, z, u)[:2][::-1]

def arc_calculator(data, distance, angle, std, points):
    """
    calculate the xy wkt of the sector shape
    :param data: the input pandas dataframe
    :param distance: distance from the sector original coordiantes to the arc
    :param angle: main angle of the sector
    :param std: the size angle of the sector
    :param points: arc resolution
    """
    x, y, u, z = data['x_utm'], data['y_utm'], data['up_down'], data['utm_zone']
    a, s, d, polygons = data[angle], data[std], data[distance], []
    for i in range(len(x)):
        sd = min(180, s[i])
        origin = find_edge_xy(x[i], y[i], z[i], u[i])
        add, tip, arc = (2*sd)/(max(points,2)-1), (180-a[i]+270)-sd, []
        for p in range(points):
            r = ((tip + (p*add)) % 360 * pi) / 180
            arc.append(find_edge_xy(x[i],y[i],z[i],u[i],r,d[i]))
        polygons.append([origin]+arc+[origin])
    data['POLYGON'] = polygons

def create_kml(data,output,names):
    """
    create kml layer  from the input df
    :param data: the input pandas dataframe
    :param output: output name
    :param names: the name field in the dataframe (give each polygon it's name)
    """
    names = list(range(data.shape[0])) if names==None else data[names]
    poly = data['POLYGON']
    file = Kml()
    for p in range(len(poly)):
        single = file.newpolygon(name=str(names[p]),outerboundaryis=poly[p])
        single.style.polystyle.color = '99ff5500'
    file.save(output+'.kml')

def create_sector_kml(data,x_field,y_field,angle,distance,std,points=36,name=None,output=None):
    """
    create sector kml layer from the given dataframe
    :param data: the given pandas dataframe
    :param x_field: x coordiantes field name
    :param y_field: y coordiantes field name
    :param angle: sector main angle field name
    :param distance: distance of the the arc from the origin point field name
    :param std: sector angle size field name
    :param points: the arc resolution (default: 36)
    :param name: row name field name (default: None)
    :param output: name of the output kml file (default: 'OUTPUT_POLYGONS')
    """
    data_preparation(data, x_field, y_field)
    arc_calculator(data, distance, angle, std, points)
    if output!=None: create_kml(data, output, name)


# License
# MIT © Etzion Harari
