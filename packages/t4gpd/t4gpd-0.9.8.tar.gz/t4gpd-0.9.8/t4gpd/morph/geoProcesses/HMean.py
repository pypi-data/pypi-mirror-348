'''
Created on 28 sept. 2020

@author: tleduc

Copyright 2020 Thomas Leduc

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
from geopandas.geodataframe import GeoDataFrame
from numpy import mean
from t4gpd.commons.IllegalArgumentTypeException import IllegalArgumentTypeException
from t4gpd.commons.RayCasting3Lib import RayCasting3Lib
from t4gpd.morph.geoProcesses.AbstractGeoprocess import AbstractGeoprocess


class HMean(AbstractGeoprocess):
    '''
    classdocs
    '''

    def __init__(self, buildingsGdf, nRays=64, maxRayLen=100.0, elevationFieldname='HAUTEUR',
                 background=False, h0=0.0):
        '''
        Constructor
        '''
        if not isinstance(buildingsGdf, GeoDataFrame):
            raise IllegalArgumentTypeException(buildingsGdf, 'GeoDataFrame')
        self.buildingsGdf = buildingsGdf

        self.shootingDirs = RayCasting3Lib.preparePanopticRays(nRays)
        self.maxRayLen = maxRayLen

        if elevationFieldname not in buildingsGdf:
            raise Exception('%s is not a relevant field name!' % elevationFieldname)
        self.elevationFieldname = elevationFieldname
        self.background = background
        self.h0 = h0

    def runWithArgs(self, row):
        viewPoint = row.geometry.centroid

        _, _, _, hitMasks, _ = RayCasting3Lib.outdoorMultipleRayCast25D(
            self.buildingsGdf, viewPoint, self.shootingDirs,
            self.maxRayLen, self.elevationFieldname, self.background, self.h0)

        hitHeights = [0.0 if f is None else f[self.elevationFieldname] for f in hitMasks]

        return {
            'hmean': float(mean(hitHeights))
            }
