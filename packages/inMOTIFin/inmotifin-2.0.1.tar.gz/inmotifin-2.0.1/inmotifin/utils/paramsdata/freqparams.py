""" Data storage for topic and motif frequency parameters """
from dataclasses import dataclass


@dataclass
class FreqParams:
    """ Class for keeping track of parameters for topic and motif frequencies
    """
    topic_frequency_type: str
    topic_frequency_range: int
    motif_frequency_type: str
    motif_frequency_range: int
    topic_topic_type: str
    concentration_factor: float
    topic_freq_file: str
    motif_freq_file: str
    topic_topic_file: str

    def __post_init__(self):
        if self.topic_frequency_type is None:
            self.topic_frequency_type = "uniform"
        if self.motif_frequency_type is None:
            self.motif_frequency_type = "uniform"
        if self.topic_topic_type is None:
            self.topic_topic_type = "uniform"
        if self.concentration_factor is None:
            self.concentration_factor = 1
