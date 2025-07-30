'''
Created on 17 feb. 2022

@author: tleduc

Copyright 2020-2022 Thomas Leduc

This file is part of t4gpd.

t4gpd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

t4gpd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with t4gpd.  If not, see <https://www.gnu.org/licenses/>.
'''
from t4gpd.io.GpkgWriter import GpkgWriter


class AbstractGeoDataFrameDemos(object):
    '''
    classdocs
    '''

    @staticmethod
    def postprocess(sio, crs='epsg:2154'):
        raise Exception('Deprecated!')

    @staticmethod
    def _dump(mapOfGdf, gpkgOutputFile="/tmp/dump.gpkg"):
        if (not mapOfGdf is None) and (0 < len(mapOfGdf)):
            GpkgWriter(mapOfGdf, gpkgOutputFile).run()
