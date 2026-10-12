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

import re
from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceArcGIS, GeoJSON, Load_XY, Conflate, Select, Mapping


# Vehicle units, the paramedic bike team and loaner or spare devices have no fixed place
NOT_FIXED = re.compile(r"vehicle|bike team|spare|loaner", re.IGNORECASE)


class Analyser_Merge_Defibrillators_CA_ON_Guelph(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 140, level = 3, tags = ['merge', 'emergency', 'fix:picture', 'fix:survey'],
            title = T_('Defibrillator not integrated'))

        # Guelph-Wellington Paramedic Service registry, published by the City of Guelph:
        # covers the City and Wellington County.
        # Positions are geocoded to the building's address point, not to the device:
        # a survey is needed to place it, hence the conflation distance.
        self.init(
            "https://www.arcgis.com/home/item.html?id=fff9039d34d1443c8c2be3324798dbba",
            "AED Locations",
            GeoJSON(SourceArcGIS(
                attribution = "City of Guelph",
                url = "https://gismaps.guelph.ca/hosting/rest/services/OpenData/OpenData2/FeatureServer/7")),
            Load_XY("geom_x", "geom_y",
                where = lambda res: not NOT_FIXED.search(res["Placement"] or "")),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                    mapping2 = {"defibrillator:location": lambda res: (res["Placement"] or "").strip() or None},
                    text = lambda tags, fields: {"en": ", ".join(filter(lambda x: x, [fields["Name"], fields["Address3"], (fields["Placement"] or "").strip()]))} )))
