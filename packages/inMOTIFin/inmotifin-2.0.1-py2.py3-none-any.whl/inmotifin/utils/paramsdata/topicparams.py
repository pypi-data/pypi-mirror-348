""" Data storage for topic parameters """
from typing import List
from dataclasses import dataclass
import math


@dataclass
class TopicParams:
    """ Class for keeping track of parameters for topics"""
    number_of_topics: int
    max_topic_size: int
    topic_size_binom_p: float
    topic_motif_assignment_file: List[str]

    def __post_init__(self):
        if self.number_of_topics is None:
            self.number_of_topics = 1
        if self.max_topic_size is None:
            self.max_topic_size = math.inf
        if self.topic_size_binom_p is None:
            self.topic_size_binom_p = 1
