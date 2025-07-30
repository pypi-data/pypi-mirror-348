""" Data class for topics """
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Topics:
    """ Class for keeping track of topics

    Class parameters
    ----------------
    topics: Dict[str, List[str]]
        Dictionary of topic IDs and the motifs within each topic
    """
    topics: Dict[str, List[str]]
