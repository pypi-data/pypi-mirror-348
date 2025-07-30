""" Data class for frequencies """
from typing import Dict
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Frequencies:
    """ Class for keeping track of frequencies

    Class parameters
    ----------------
    num_topics: int
        Number of topics
    topic_freq: Dict[str, float]
        Dictionary of topic IDs and their expected occurrence frequencies
    motif_freq_per_topic: pd.DataFrame
        Dataframe of expected frequencies of motifs per topic
    topic_topic_cooccurence_prob: pd.DataFrame
        Dataframe of expected co-occurrence probability of topic pairs
    """
    num_topics: int = field(init=False)
    topic_freq: Dict[str, float]
    motif_freq_per_topic: pd.DataFrame
    topic_topic_cooccurence_prob: pd.DataFrame

    def __post_init__(self):
        """ Calculate and store number of topics """
        self.num_topics = len(self.topic_freq.keys())
