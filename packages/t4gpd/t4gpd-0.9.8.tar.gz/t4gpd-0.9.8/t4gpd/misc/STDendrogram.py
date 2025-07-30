'''
Created on 5 janv. 2021

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
from pandas import DataFrame
from scipy.cluster.hierarchy import dendrogram, linkage
from t4gpd.commons.GeoProcess import GeoProcess
from t4gpd.commons.IllegalArgumentTypeException import IllegalArgumentTypeException

import matplotlib.pyplot as plt


class STDendrogram(GeoProcess):
    '''
    classdocs
    '''
    NUMERICS = ["int16", "int32", "int64", "float16", "float32", "float64"]

    def __init__(self, inputGdf, orientation="top", no_plot=False, verbose=True):
        '''
        Constructor
        '''
        if not isinstance(inputGdf, DataFrame):
            raise IllegalArgumentTypeException(inputGdf, "DataFrame")

        self.data = inputGdf.select_dtypes(include=self.NUMERICS)

        _fieldnames = list(self.data.columns)
        if (0 == len(_fieldnames)):
            raise Exception("There are no numeric (float) fields in the GeoDataFrame!")
        if verbose:
            print(f"The following fields are taken into account when processing: {_fieldnames}")

        if not orientation in ("bottom", "left", "right", "top"):
            raise IllegalArgumentTypeException(orientation, '("bottom", "left", "right", "top")')
        self.orientation = orientation

        if not isinstance(no_plot, bool):
            raise IllegalArgumentTypeException(no_plot, "bool")
        self.noPlot = no_plot

    def run(self):
        Z = linkage(self.data, method="ward", metric="euclidean")
        d = dendrogram(Z, orientation=self.orientation, show_contracted=True, no_plot=self.noPlot)
        plt.show()

        nClusters = len(set(d["color_list"])) - 1
        return nClusters
