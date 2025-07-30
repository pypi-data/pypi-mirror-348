from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class LabTestData:
    test_type: str = ""  # e.g., "Atterberg Limits", "Triaxial", etc.
    depth: Optional[float] = None  # Depth at which the sample was taken (meters), if applicable
    test_results: Dict[str, Any] = field(default_factory=dict)  # Results as key-value pairs
    test_date: Optional[str] = None  # Date of the test (optional)
    notes: Optional[str] = None      # Any additional notes (optional)

    def add_result(self, key: str, value: Any):
        """Add or update a result in the test_results dictionary."""
        self.test_results[key] = value

    def summary(self) -> str:
        """Return a string summary of the lab test."""
        summary_lines = [
            f"Test Type: {self.test_type}",
            f"Depth: {self.depth} m" if self.depth is not None else "Depth: N/A",
            f"Test Date: {self.test_date}" if self.test_date else "Test Date: N/A",
            f"Notes: {self.notes}" if self.notes else "Notes: N/A",
            "Results:"
        ]
        for k, v in self.test_results.items():
            summary_lines.append(f"  {k}: {v}")
        return "\n".join(summary_lines)