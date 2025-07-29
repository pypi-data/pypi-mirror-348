from enum import Enum


class LaunchJsonDocumentsImportSegmentationPolicy(str, Enum):
    ALWAYS_RECOMPUTE = "always_recompute"
    COMPUTE_IF_MISSING = "compute_if_missing"
    DOCUMENTS_AS_SEGMENTS = "documents_as_segments"
    NO_SEGMENTATION = "no_segmentation"

    def __str__(self) -> str:
        return str(self.value)
