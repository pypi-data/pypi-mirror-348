""" Sample from topic and motif frequencies """
from typing import List
import numpy as np
from inmotifin.utils.baseutils import choice_from_dict
from inmotifin.modules.data.frequencies import Frequencies


class FrequencySampler:
    """ Class to select motif based on its background frequencies

    Class parameters
    ----------------
    frequencies: Frequencies
        Frequencies data class including probabilities of \
        topics and motifs within them
    num_topics_per_seq: int
        Number of topics to select in total
    rng: np.random.Generator
        Random generator for sampling
    """

    def __init__(
            self,
            frequencies: Frequencies,
            num_topics_per_seq: int,
            rng: np.random.Generator):
        """ Constructor

        Parameters
        ----------
        frequencies: Frequencies
            Frequencies data class including probabilities of \
            topics and motifs within them
        num_topics_per_seq: int
            Number of topics to select in total
        rng: np.random.Generator
            Random generator for sampling
        """
        self.frequencies = frequencies
        self.num_topics_per_seq = num_topics_per_seq
        self.rng = rng

    def select_topics(self) -> List[str]:
        """ Select topics based on their frequency and co-occurence \
            probability

        Return
        ------
        selected_ids: List[str]
            List of selected topic ids
        """
        first_topic = self.select_first_topic()
        all_topics = sorted(self.select_rest_of_topics(
            num_topics_rest=self.num_topics_per_seq-1,
            base_topic=first_topic))
        all_topics_str = [str(top) for top in all_topics]
        all_topics_str.append(first_topic)
        return all_topics_str

    def select_first_topic(self) -> str:
        """ Start by selecting the first topic given topic frequencies

        Return
        ------
        selected_topic: str
            ID of the selected topic
        """
        selected_topic = str(choice_from_dict(
            indict=self.frequencies.topic_freq,
            size=1,
            rng=self.rng)[0])
        return selected_topic

    def select_rest_of_topics(
            self,
            num_topics_rest: int,
            base_topic: str) -> np.ndarray:
        """ Select a topic given an already selected topic

        Parameters
        ----------
        num_topics_rest: int
            Number of topics to select after the first one
        base_topic: str
            ID of the already selected topic

        Return
        ------
        selected_ids: np.ndarray
            Array of selected topic ids
        """
        topic_probs = self.frequencies.topic_topic_cooccurence_prob.loc[
            base_topic,]

        selected_ids = choice_from_dict(
            indict=topic_probs,
            size=num_topics_rest,
            rng=self.rng)

        return selected_ids

    def select_motifs_from_topics(
            self,
            topic_ids: List[str],
            num_instances_per_seq: int) -> List[str]:
        """ Select motifs from given topics

        Parameters
        ----------
        topic_ids: List[str]
            List of selected topic ids
        num_instances_per_seq: int
            Number of motifs to select (per sequence)

        Return
        ------
        selected_motifs: List[str]
            List of selected motif IDs
        """
        num_motif_per_topic = int(np.floor(
            num_instances_per_seq / self.num_topics_per_seq))
        all_selected_motifs = []
        for topic in topic_ids:
            prob_series = self.frequencies.motif_freq_per_topic[topic]
            selected_motifs = self.rng.choice(
                a=prob_series.index,
                size=num_motif_per_topic,
                replace=True,
                p=prob_series.tolist())
            all_selected_motifs += list(selected_motifs)
        while len(all_selected_motifs) < num_instances_per_seq:
            # pick one more motif from one topic
            one_more_topic_idx = self.rng.choice(
                a=topic_ids,
                size=1)[0]
            motif_probs = self.frequencies.motif_freq_per_topic[
                one_more_topic_idx]
            one_more_motif = self.rng.choice(
                a=motif_probs.index,
                size=1,
                p=motif_probs.tolist())
            all_selected_motifs.append(one_more_motif[0])
        return all_selected_motifs
