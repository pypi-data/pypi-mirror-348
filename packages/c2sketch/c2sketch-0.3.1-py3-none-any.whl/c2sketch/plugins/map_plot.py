from c2sketch.app.plugins import InformationSpaceUI
from c2sketch.models import *
from c2sketch.app.ui import *
import math

class MapView(Editor):
    def __init__(self, basemap:str, center:tuple[float,float],zoom:int = 8):
        self.basemap = basemap
        self.center = center
        self.zoom = zoom

    def generate_ui(self, name='v'):
        
        markers = list()
        if self._raw is not None and self._raw:
           
            for object in self._raw:

                identifier = None
                if 'identifier' in object:
                    identifier = int(object['identifier'])
                #Compute position
                position = None
                if 'position' in object and object['position'] is not None:
                    latlng = object['position'].split()
                    position = (float(latlng[0]),float(latlng[1]))
                    if 'offset' in object and object['offset'] is not None:
                        offset = object['offset'].split()
                        position = add_position_offset(position,float(offset[1]),float(offset[0]))
                
                #We can't plot items without identifier or position
                if position is None:
                    continue
                   
                altitude = 0
                if 'altitude' in object and object['altitude'] is not None:
                    altitude = float(object['altitude'])
                    if 'offset' in object and object['offset'] is not None:
                        altitude += float(object['offset'].split()[2])

                velocity = None
                if 'velocity' in object:
                    velocity = object['velocity']

                orientation = None
                if 'orientation' in object:
                    orientation = object['orientation']

                if 'name' in object:
                    label = object['name']
                elif 'classification' in object:
                    label = object['classification']
                else:
                    label = 'unknown'
            
                colors = {'unknown':'#ffff33','friendly':'#6666ff','hostile':'#ff3333','neutral':'#33ff33','destroyed':'#000000'}
                color = colors[object.get('classification','unknown')]
                
                attributes = {
                        'identifier':str(identifier),
                        'label': label,
                        'lat':str(position[0]),
                        'lng':str(position[1]),
                        'color': color,
                    }
                if orientation is not None:
                    attributes['heading'] = orientation[0]
                elif velocity is not None:
                    attributes['heading'] = heading_from_velocity(velocity)
                
                attribute_html = ' '.join(f'{key}="{value}"' for key,value in attributes.items())
                markers.append(f'<map-marker {attribute_html}></map-marker>')

        return f'''
        <map-view base="{self.basemap}" lat="{self.center[0]}" lng="{self.center[1]}" zoom="{self.zoom}" style="height: 100vh">
        {"".join(markers)}
        </map-view>
        '''

def config_type():
    config_type = RecordType(None,[],'map_plot_config')
    config_type.fields.append(RecordTypeField(config_type,[], 'basemap', 'string'))# Base map url
    config_type.fields.append(RecordTypeField(config_type,[],'center', 'latlng')) # Center
    config_type.fields.append(RecordTypeField(config_type,[],'zoom', 'integer')) #Zoom level
   
    return config_type


def create_editor(op_type, config = None):
    if config is not None:
        basemap = config['basemap']
        [lat,lng] = config['center'].split()
        center = (float(lat),float(lng))
        zoom = int(config['zoom'])
    else:
        basemap = ''
        center = (0.0,0.0)
        zoom = 8
    
    return MapView(basemap,center,zoom)

def control_ui(rsource,wsource,type,config):
    return view_information(rsource,editor=create_editor(type,config))

def add_position_offset(position,lat_offset=0,lng_offset=0):
    earth_radius = 6371000.0
    radpermeter_lat = 1.0 / earth_radius
    radpermeter_lng = lambda lat: 1.0 / (earth_radius * math.cos(lat))

    latr = math.radians(position[0]) + (lat_offset * radpermeter_lat)
    lat = math.degrees(latr)
    lng = position[1] + math.degrees(radpermeter_lng(latr) * lng_offset)
    return (lat,lng)

def heading_from_velocity(velocity):
    """Calculate a heading in degrees (wrt north) from a velocity vector"""
    return int(math.degrees(math.atan2(*velocity[0:2])))

#Define plugin
map_plot = InformationSpaceUI (
    title = 'Map plot',
    description = 'Plot markers, lines and area\'s on a map',
    config_type = config_type(),
    control_ui = control_ui,
    js_requirements = [
        '/static/node_modules/leaflet/dist/leaflet.js',
        '/static/map_plot.js']
)