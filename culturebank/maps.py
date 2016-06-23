from clld.web.maps import Map, Layer, ParameterMap, LanguageMap

class HighZoomParameterMap (ParameterMap):
    def get_options(self):
        return {'max_zoom': 10, 'icon_size': 20}

class HighZoomLanguageMap (LanguageMap):
    def get_options(self):
        return {'max_zoom': 10, 'icon_size': 20}
    
class HighZoomMap (Map):
    def get_options(self):
        return {'max_zoom': 10, 'icon_size': 20}

class DeepFamilyMap(Map):
    def __init__(self, ctx, req, eid='map', icon_map=None):
        super(DeepFamilyMap, self).__init__(ctx, req, eid=eid)
        self.icon_map = icon_map or {} #TODO make this point to a URL with a .png
        self.deepfamid = ctx.id
        self.deepfamname = ctx.id
        self.protolanguages = ([(ctx.family1_pk, ctx.family1.name, ctx.family1_longitude, ctx.family1_latitude, ctx.family1.name)] if ctx.family1_latitude else []) + ([(ctx.family2_pk, ctx.family2.name, ctx.family2_longitude, ctx.family2_latitude, ctx.family2.name)] if ctx.family2_latitude else [])
              
    def get_layers(self):
        properties = {"layer": "deepfamily"} #self.deepfamid, "name": self.deepfamname}
        features = [{"type": "Feature", "geometry": {'type': 'Point', 'coordinates': (lon, lat)}, "properties": {'name': name, 'icon': self.icon_map[pk], "id": id_}, "pk": pk, "description": None, "longitude": lon, "latitude": lat, "markup_description": None, "jsondata": {}} for (pk, name, lon, lat, id_) in self.protolanguages]
        #yield Layer(self.id, self.name, {"type": "FeatureCollection", "properties": properties, "features": features})
        #print self.id
        #print features
        yield Layer("deepfamily", self.deepfamname,
            {
                "type": "FeatureCollection",
                "properties": properties,
                "features": features
            })
    
    def get_options(self):
        res = {'max_zoom': 12}
        res['sidebar'] = True
        res['zoom'] = 6
        res['no_link'] = True
        res['no_popup'] = True
        return res


def includeme(config):
    config.register_map('deepfamily', DeepFamilyMap)
    config.register_map('parameter', HighZoomParameterMap)
    config.register_map('language', HighZoomLanguageMap)
    config.register_map('languages', HighZoomMap)
