# Copyright 2025, BRGM
# 
# This file is part of Rameau.
# 
# Rameau is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# 
# Rameau is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# Rameau. If not, see <https://www.gnu.org/licenses/>.
#
"""
Groundwater parameters.
"""

from __future__ import annotations
import numpy as np
from typing import Union, Optional

from rameau.wrapper import CGroundwater

from rameau.core.parameter import Parameter
from rameau.core.groundwater import StorageParameters, GroundwaterReservoir
from rameau.core._abstract_wrapper import AbstractWrapper

from rameau._typing import ParameterType
from rameau.core._utils import _build_type, _build_parameter
from rameau.core._descriptor import (
    _DerivedTypeDecriptor,
    _FloatDescriptor,
    _IntDescriptor,
    _VectorDescriptor,
    _VectorDerivedTypeDescriptor
)

class GroundwaterParameters(AbstractWrapper):
    """Groundwater parameters.
    
    Parameters
    ----------
    reservoirs: `list`, optional
        List of `GroundwaterReservoir`.
    
    storage: `dict` or `StorageParameters`, optional
        Parameters linked to the storage coefficient calculation.
    
    base_level: `dict` or `Parameter`, optional
        Groundwater base level (m NGF).

    weight: `float`, optional
        Weight given to groundwater level during the model optimisation.
        A value of zero means no groundwater level optimisation.

    obslim: `[float, float]`, optional
        Bounds applied to the observed groundwater level during the
        model optimisation.

    observed_reservoir: `int`, optional
        Reservoir index for which reservoir level in mm will be converted
        to piezometer head in m NGF. Index starts from 1 from the upper
        to the deeper groundwater reservoir.
    
    Returns
    -------
    `GroundwaterParameters`
    """
    _computed_attributes = (
        "storage", "base_level", "weight", "obslim",
        "observed_reservoir", "reservoirs"
    )
    _c_class = CGroundwater

    reservoirs: list[GroundwaterReservoir] = _VectorDerivedTypeDescriptor(
        0, GroundwaterReservoir
    ) #type: ignore
    storage: StorageParameters = _DerivedTypeDecriptor(0, StorageParameters) #type: ignore
    base_level: Parameter = _DerivedTypeDecriptor(0, Parameter) #type: ignore
    weight: float = _FloatDescriptor(0)  #type: ignore
    obslim: list[float] = _VectorDescriptor(0, float) #type: ignore
    observed_reservoir: int = _IntDescriptor(0) #type: ignore

    def __init__(
        self,
        reservoirs: Optional[list[GroundwaterReservoir]] = None,
        storage:  Optional[Union[dict, StorageParameters]]= None,
        base_level: ParameterType = None,
        weight: float = 0.0,
        obslim: list = [0.0, 0.0],
        observed_reservoir: int = 1,
    ) -> None: 
        self._init_c()

        if storage is not None:
            self.storage = _build_type(storage, StorageParameters)
        if base_level is not None:
            self.base_level = _build_parameter(base_level)
        
        self.weight = weight
        self.obslim = obslim
        self.observed_reservoir = observed_reservoir

        if reservoirs is None:
            reservoirs = [GroundwaterReservoir()]

        tmp = []
        if isinstance(reservoirs, list):
            if not bool(reservoirs):
                raise ValueError("Empty list not allowed.")
        elif isinstance(reservoirs, np.ndarray):
            if reservoirs.size == 0:
                raise ValueError("Empty numpy.ndarray not allowed.")
        else:
            raise TypeError(f"Type {type(reservoirs)} not allowed.")


        for res in reservoirs:
            if isinstance(res, dict):
                tmp.append(GroundwaterReservoir(**res))
            else:
                tmp.append(res)

        self.reservoirs = tmp