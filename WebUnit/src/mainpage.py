#
# Main page (handler) extends base handler
#
import urllib2;
from basehandler import BaseHandler;
from xml.dom import minidom;
from urllib2 import URLError

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&";
GMAPS_D_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&maptype=roadmap&markers=size:mid%7Ccolor:red%7CSan+Francisco,CA%7COakland,CA%7CSan+Jose,CA&sensor=false";
def gmaps_img(points):
    m = '&'.join("markers=%s,%s" % (p[0], p[1]) for p in points);
    return GMAPS_URL + m;

HOSTIP_INFO_API_URL = 'http://api.hostip.info/?ip=%s';
def get_coordinates(ip):
    url = HOSTIP_INFO_API_URL % str(ip);
    content = None;
    try:
        content = urllib2.urlopen(url).read();
    except URLError:
        return None;

    if content:
        coords_xml = minidom.parseString(content);
        oo = coords_xml.getElementsByTagName("gml:coordinates");
        if oo and oo[0].firstChild:
            coords = (oo[0].firstChild.nodeValue).split(',');
            if len(coords) == 2:
                lon, lat = coords[0], coords[1];  
                return [(lat, lon)];
    return None;

'''
Main page handler
'''
class MainPage(BaseHandler):
    def get(self):
        image_url = None;
        points = get_coordinates(self.request.remote_addr);        
        if points:
            image_url = gmaps_img(points);
        else:
            image_url = GMAPS_D_URL;
        self.render("front.html", image_url = image_url);