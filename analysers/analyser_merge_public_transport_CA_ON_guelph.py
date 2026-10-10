#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights skfd 2026                                                  ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceArcGIS, GeoJSON, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_CA_ON_Guelph(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "Guelph Transit"
        self.def_class_missing_official(item = 8040, id = 161, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 163, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))

        self.init(
            "https://geodatahub-cityofguelph.opendata.arcgis.com/datasets/cityofguelph::bus-stops-1",
            "Bus Stops",
            GeoJSON(SourceArcGIS(
                attribution = "City of Guelph",
                url = "https://gismaps.guelph.ca/hosting/rest/services/OpenData/OpenData1/FeatureServer/33",
                # Stops served only by on-demand transit are pick-up points, not posted stops
                where = "Conv = 'Yes'")),
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                        {"highway": "bus_stop"},
                        {"public_transport": "platform", "bus": "yes"}]),
                osmRef = "ref",
                conflationDistance = 30,
                mapping = Mapping(
                    static1 = {"highway": "bus_stop"},
                    static2 = {
                        "public_transport": "platform",
                        "bus": "yes",
                        "network": place,
                        "source": self.source},
                    mapping1 = {"ref": lambda res: str(int(float(res["StopId"])))},
                    mapping2 = {"name": "StopName"},
                    text = lambda tags, fields: T_("{0} stop of {1}", place, fields["StopName"]) )))
