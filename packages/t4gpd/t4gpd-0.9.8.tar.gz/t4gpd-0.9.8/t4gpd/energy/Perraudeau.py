'''
Created on 25 aug. 2020

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
from numpy import exp, pi
from t4gpd.commons.AngleLib import AngleLib


class Perraudeau(object):
    '''
    classdocs
    d'apres (Miguet, 2000; p. 170)
    '''

    @staticmethod
    def directNormalIrradiance(solarAltitudeAngle):
        assert (0 <= solarAltitudeAngle <= (pi / 2)), 'solarAltitudeAngle in radians!'

        return 1000.0 * (1.0 - exp(-0.055 * AngleLib.toDegrees(solarAltitudeAngle)))
