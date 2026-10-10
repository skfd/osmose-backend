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


class Analyser_Merge_Hydrants_CA_ON_Guelph(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8090, id = 21, level = 3, tags = ['merge', 'emergency', 'fix:imagery', 'fix:picture', 'fix:survey'],
            title = T_('Fire hydrant not integrated'))

        # No ref: the City's HYDRANTID is an asset number, not painted on the hydrant.
        self.init(
            "https://geodatahub-cityofguelph.opendata.arcgis.com/datasets/cityofguelph::hydrants",
            "Hydrants",
            GeoJSON(SourceArcGIS(
                attribution = "City of Guelph",
                url = "https://gismaps.guelph.ca/hosting/rest/services/OpenData/OpenData2/FeatureServer/3")),
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "fire_hydrant"}),
                conflationDistance = 30,
                mapping = Mapping(
                    static1 = {"emergency": "fire_hydrant"},
                    static2 = {"source": self.source} )))
