from typing import NamedTuple

import numpy as np
import numpy.typing as npt

from processing.config.BandConfig import BandConfig
from processing.config.ExtractionConfig import ExtractionConfig
from processing.config.ExtractorConfig import ExtractorConfig
from processing.config.FileConfig import FileConfig
from processing.extractors.Extractor import Extractor
from processing.services.SiteService import SiteWithFiles


class ExtractionData(NamedTuple):
    file: FileConfig
    extractor: ExtractorConfig
    embeddings: np.ndarray
    starts: list[int]  # relative timestamps in ms
    ends: list[int]  # relative timestamps in ms
    astarts: list[int]  # absolute timestamps in ms
    aends: list[int]  # absolute timestamps in ms


class ExtractionIteration(NamedTuple):
    site: SiteWithFiles
    band: BandConfig
    extraction: ExtractionConfig
    extractor: ExtractorConfig
    ex: Extractor


class TimelineSlice(NamedTuple):
    extractor: ExtractorConfig
    file: FileConfig
    embeddings: np.ndarray
    astart: int  # absolute timestamp in ms
    aend: int  # absolute timestamp in ms
    rstart: int  # relative timestamp in ms (to file)
    rend: int  # relative timestamp in ms (to file)


class TimelineAggregate(NamedTuple):
    embeddings: np.ndarray
    slices: list[TimelineSlice]
    start: int  # absolute timestamp in ms
    end: int  # absolute timestamp in ms


class AggregationData(NamedTuple):
    embeddings: np.ndarray
    start: int  # absolute timestamp in ms
    end: int  # absolute timestamp in ms
    files: list[FileConfig]
    extractors: list[ExtractorConfig]


_MetricDataKey = str | tuple[str, str]
MetricData = dict[_MetricDataKey, npt.NDArray[np.float32]]


class Interval(NamedTuple):
    i: int
    aggregated: AggregationData

    joined_site: str  # joined sites if multiple files
    sites: list[str]

    # joined tags are a bit different than tags
    # object keys are tag names
    # object values are the tag uniques
    # the tag uniques are concatenated tag values
    # (this joined string occurs when multiple files populate the same interval)
    joined_tags: dict[str, str]
    tags: dict[str, list[str]]


class TrajectoryData(NamedTuple):
    path: np.ndarray
    timestamps: np.ndarray


class TrajectoryStatistics(NamedTuple):
    median_distances: np.ndarray
    median_timestamps: np.ndarray
    lower_deciles: np.ndarray
    upper_deciles: np.ndarray
