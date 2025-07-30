from dataclasses import dataclass, field
from typing import Tuple, List, Optional
from .borehole import BoreholeData
from .labtest import LabTestData
from .groundwater import GroundwaterData

@dataclass
class Point:
    id: str
    coordinates: Tuple[float, float]
    description: str = ""
    borehole_data: Optional[BoreholeData] = field(default=None)
    lab_tests: List[LabTestData] = field(default_factory=list)
    groundwater_data: Optional[GroundwaterData] = field(default=None)