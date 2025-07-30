from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd  # For generating the summary table
import matplotlib.pyplot as plt  # For plotting
import warnings

@dataclass
class SPTData:
    depth: float  # Depth at which the SPT was conducted (in meters)
    blow_data: Optional[List[int]] = field(default=None)  # Optional list of blow counts for each 15 cm increment
    blow_counts: Optional[int] = None  # Allow user to define blow_counts directly

    def __post_init__(self):
        """Calculate blow_counts as the sum of the last two numbers in blow_data, unless set directly."""
        if self.blow_counts is not None:
            # User provided blow_counts directly; do not calculate from blow_data
            return
        if self.blow_data is not None:
            if len(self.blow_data) < 3:
                warnings.warn(
                    f"SPTData at depth {self.depth}m: blow_data has less than 3 values. "
                    "Standard SPT requires 3 values (for 3x15cm increments)."
                )
            if len(self.blow_data) >= 2:
                self.blow_counts = sum(self.blow_data[-2:])
            else:
                self.blow_counts = 0
        else:
            self.blow_counts = 0

@dataclass
class BoreholeData:
    borehole_id: str  # Unique identifier for the borehole
    total_depth: Optional[float] = None  # Total depth of the borehole (in meters), optional
    spt_data: List[SPTData] = field(default_factory=list)  # List of SPT data entries

    def add_spt_data(self, depth: float, blows: Optional[List[int]] = None, blow_counts: Optional[int] = None):
        """Add SPT data for a specific depth."""
        self.spt_data.append(SPTData(depth=depth, blow_data=blows, blow_counts=blow_counts))

    def generate_spt_summary(self) -> pd.DataFrame:
        """Generate a summary table of SPT results."""
        data = {
            "Depth (m)": [spt.depth for spt in self.spt_data],
            "Blow Data": [spt.blow_data for spt in self.spt_data],
            "Blow Counts": [spt.blow_counts for spt in self.spt_data],
        }
        return pd.DataFrame(data)

    def plot_blow_counts(self):
        """Plot blow counts versus depth as an XY line plot."""
        depths = [spt.depth for spt in self.spt_data]
        blow_counts = [spt.blow_counts for spt in self.spt_data]

        plt.figure(figsize=(8, 6))
        plt.plot(blow_counts, depths, marker="o", linestyle="-", color="b", label="Blow Counts")
        plt.gca().invert_yaxis()  # Invert the Y-axis to show depth increasing downward
        plt.xlabel("Blow Counts")
        plt.ylabel("Depth (m)")
        plt.title(f"SPT Blow Counts vs Depth for Borehole {self.borehole_id}")
        plt.legend()
        plt.grid(True)
        plt.show()