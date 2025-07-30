# groundwater.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class GroundwaterData:
    water_table_depth: Optional[float] = None
    measurement_date: Optional[str] = None
    notes: Optional[str] = None