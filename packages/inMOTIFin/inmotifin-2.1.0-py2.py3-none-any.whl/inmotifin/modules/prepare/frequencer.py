""" Class to generate motif and topic background frequencies """
from typing import List, Dict
import numpy as np
import pandas as pd
from inmotifin.utils import mathutils
from inmotifin.utils.paramsdata.freqparams import FreqParams
from inmotifin.modules.data.frequencies import Frequencies
from inmotifin.modules.data.topics import Topics
from inmotifin.utils.fileops.reader import Reader
from inmotifin.utils.fileops.writer import Writer


class Frequencer:
    """Class to generate motif and topic background frequencies, \
    that is the selection probability for each topic and motif within

    Class parameters
    ----------------
    title: str
        Title of the analysis
    params: FreqParams
        Dataclass storing topic_frequency_type, topic_frequency_range, \
        motif_frequency_type, motif_frequency_range, topic_freq_file and \
        motif_freq_file
    topics: Topics
        The topics with ids and assigned motifs
    num_topics: int
        Number of topics
    reader: Reader
        File reader class to read in sequences if necessary
    writer: Writer
        instance of the writer class
    frequencies: Frequencies
        Data class for frequencies
    rng: np.random.Generator
        Random generator for random frequency sampling
    """

    def __init__(
            self,
            params: FreqParams,
            topics: Topics,
            reader: Reader,
            writer: Writer,
            rng: np.random.Generator) -> None:
        """ Constructor

        Parameters
        ----------
        params: FreqParams
            Dataclass storing topic_frequency_type, topic_frequency_range, \
            motif_frequency_type, motif_frequency_range, topic_freq_file and \
            motif_freq_file
        topics: Topics
            The topics with ids and assigned motifs
        reader: Reader
            File reader class to read in sequences if necessary
        writer: Writer
            instance of the writer class
        rng: np.random.Generator
            Random generator for random frequency sampling
        """
        self.title = writer.get_title()
        self.rng = rng
        self.params = params
        self.topics = topics
        self.reader = reader
        self.writer = writer
        self.num_topics = len(self.topics.topics)
        self.frequencies = None

    def get_frequencies(self) -> Frequencies:
        """ Getter for topic and motif frequencies

        Return
        -------
        frequencies: Frequencies
            Data class for frequencies
        """
        return self.frequencies

    def assign_frequencies(self) -> None:
        """ Read in or simulate topic and motif frequencies """
        if self.params.motif_freq_file is not None:
            motif_freq_per_topic = self.read_motif_freq_per_topic()
        else:
            motif_freq_per_topic = self.assign_motif_frequencies()
            self.writer.pandas_to_tsv(
                dataframe=motif_freq_per_topic,
                filename="motif_freq_per_topic")
        if self.params.topic_freq_file is not None:
            topic_freq = self.read_topic_freq()
        else:
            topic_freq = self.assign_topic_frequencies()
            self.writer.dict_to_tsv(
                data_dict=topic_freq,
                filename="topic_frequency")
        if self.params.topic_topic_file is not None:
            topic_topic_cooccurence_prob = self.read_topic_topic_cooc()
        else:
            topic_topic_cooccurence_prob = self.assign_topic_topic_cooc_probs()
            self.writer.pandas_to_tsv(
                dataframe=topic_topic_cooccurence_prob,
                filename="topic_topic_cooccurence_probabilities")

        self.frequencies = Frequencies(
            topic_freq=topic_freq,
            motif_freq_per_topic=motif_freq_per_topic,
            topic_topic_cooccurence_prob=topic_topic_cooccurence_prob)

    def read_motif_freq_per_topic(self) -> pd.DataFrame:
        """ Read in motif frequencies

        Return
        ------
        motif_freq: pd.DataFrame
            Motif frequencies per topic from file
        """
        return self.reader.read_tsv_to_pandas(
            pandas_dftsv_path=self.params.motif_freq_file)

    def read_topic_freq(self) -> Dict[str, float]:
        """ Read in topic frequencies

        Return
        ------
        topic_freq: Dict[str, float]
            Dictionary of topic IDs and their expected occurrence \
            frequencies
        """
        topic_freq_raw = self.reader.read_twocolumn_tsv(
            twocolumns_tsv_path=self.params.topic_freq_file)
        topic_freq = {}
        for topic_id, topic_p in topic_freq_raw.items():
            topic_freq[topic_id] = float(topic_p[0])
        return topic_freq

    def read_topic_topic_cooc(self) -> pd.DataFrame:
        """ Read in topic topic cooccurences

        Return
        ------
        topic_topic: pd.DataFrame
            Pandas dataframe of co-occurrences of topic pairs
        """
        return self.reader.read_tsv_to_pandas(
            pandas_dftsv_path=self.params.topic_topic_file)

    def assign_topic_frequencies(self) -> Dict[str, float]:
        """ Simulate topic frequencies

        Return
        ------
        topic_freq: Dict[str, float]
            Dictionary of topic IDs and their expected occurrence \
            frequencies
        """
        topic_freq = self.simulate_background_freq(
            freq_type=self.params.topic_frequency_type,
            freq_range=self.params.topic_frequency_range,
            ids=sorted(self.topics.topics.keys()))
        return topic_freq

    def assign_motif_frequencies(self) -> pd.DataFrame:
        """ Simulate motif frequencies within topics

        Return
        ------
        motif_topic_df: pd.DataFrame
            Pandas dataframe of motif frequencies per topic
        """
        motif_freq_per_topic = {}
        for topic_key, topic_value in self.topics.topics.items():
            motif_freq_per_topic[topic_key] = \
                self.simulate_background_freq(
                    freq_type=self.params.motif_frequency_type,
                    freq_range=self.params.motif_frequency_range,
                    ids=topic_value)
        motif_topic_df = pd.DataFrame.from_dict(
            motif_freq_per_topic,
            orient="columns")
        motif_topic_df.fillna(value=0, inplace=True)
        return motif_topic_df

    def assign_topic_topic_cooc_probs(self) -> pd.DataFrame:
        """ Simulate the probability of selecting topicX given \
            previously selected topicY

        Return
        ------
        topic_topic_cooccurence_prob: pd.DataFrame
            Pandas dataframe of co-occurrences of topic pairs
        """
        topic_ids = sorted(self.topics.topics.keys())
        remaining_prob = 1 - self.params.concentration_factor
        if self.params.topic_topic_type.lower() == "random":
            topic_topic_matrix = self.pairs_random(
                remaining_prob=remaining_prob)
        elif self.params.topic_topic_type.lower() == "uniform":
            topic_topic_matrix = self.symmetric_pairs_uniform(
                remaining_prob=remaining_prob)
        else:
            raise ValueError("only random and uniform types are supported")
        topic_topic_cooccurence_prob = pd.DataFrame(
            topic_topic_matrix,
            columns=topic_ids,
            index=topic_ids)
        return topic_topic_cooccurence_prob

    def symmetric_pairs_uniform(
            self,
            remaining_prob: float) -> np.ndarray:
        """ Creating a matrix of topic-topic and their co-occurence \
            probability: off-diagonals are uniform

        Parameters
        ----------
        remaining_prob: float
            The probability remaining after assigning self co-occurence

        Return
        ------
        topic_prob_arr: np.ndarray
            Array containing probabilities for topic co-occurence
        """
        if self.num_topics == 1:
            off_diag_prob = 0
        else:
            off_diag_prob = remaining_prob/(self.num_topics-1)
        topic_prob_arr = np.zeros(
            (self.num_topics, self.num_topics),
            dtype=float)
        np.fill_diagonal(topic_prob_arr, self.params.concentration_factor)
        topic_prob_arr[np.triu_indices(self.num_topics, k=1)] = off_diag_prob
        topic_prob_arr[np.tril_indices(self.num_topics, k=-1)] = off_diag_prob
        return topic_prob_arr

    def pairs_random(
            self,
            remaining_prob: float) -> np.ndarray:
        """ Creating a matrix of topic-topic and their co-occurence \
            probability: off-diagonals are random but rows sum to 1

        Parameters
        ----------
        remaining_prob: float
            The probability remaining after assigning self co-occurence

        Return
        ------
        topic_prob_arr: np.ndarray
            Array containing probabilities for topic co-occurence
        """
        nt = self.num_topics
        topic_prob_arr = np.zeros((nt, nt), dtype=float)
        # fill in the rest of the matrix with random values
        # in a symmetric fashion and all rows sum to 1
        for rowidx in range(0, nt):
            rest_of_prob = remaining_prob
            for colidx in range(0, nt):
                if rowidx == colidx:
                    # fill diagonal with fix values
                    topic_prob_arr[rowidx, colidx] = \
                        self.params.concentration_factor
                elif colidx == nt-1:
                    # ensure that rows sum to 1
                    topic_prob_arr[rowidx, colidx] = rest_of_prob
                elif (rowidx == nt-1) and (colidx == nt-2):
                    # ensure that rows sum to 1
                    topic_prob_arr[rowidx, colidx] = rest_of_prob
                else:
                    # otherwise, sample random value below sum(1)
                    topic_prob_arr[rowidx, colidx] = self.rng.uniform(
                        low=0.0,
                        high=rest_of_prob)
                    rest_of_prob -= topic_prob_arr[rowidx, colidx]
        return topic_prob_arr

    def simulate_background_freq(
            self,
            freq_type: str,
            freq_range: int,
            ids: List[str]) -> Dict[str, float]:
        """ Simulate background frequencies

        Parameters
        ----------
        freq_type: str
            Way to generate frequencies. Currently random and uniform are \
            supported. Random refers to random sampling from a range of \
            probabilities given freq_range. Uniform refers to assigning \
            equal probabilities to all items.
        freq_range: int
            The expected max difference between an unlikely and a likely event\
            . E.g. if set to 100, a low probability event can be 100x less \
            likely than a high probability one
        ids: List[str]
            The IDs of the items to assign frequency to

        Return
        ------
        background_freq: Dict[str, float]
            Probability assigned to each element of the given ids
        """
        if freq_type.lower() == "random":
            background_freq = self.simulate_background_freq_random(
                difference_width=freq_range,
                ids=ids)
        elif freq_type.lower() == "uniform":
            background_freq = self.simulate_background_freq_uniform(
                ids=ids)
        else:
            raise ValueError("only random and uniform types are supported")
        return background_freq

    def simulate_background_freq_random(
            self,
            difference_width: int,
            ids: List[str]) -> Dict[str, float]:
        """ Simulate background frequencies random uniform

        Parameters
        ----------
        difference_width: int
            The expected max difference between an unlikely and a likely event\
            . E.g. if set to 100, a low probability event can be 100x less \
            likely than a high probability one
        ids: List[str]
            The IDs of the items to assign frequency to

        Return
        ------
        background_freq: Dict[str, float]
            Probability assigned to each element of the given ids
        """
        background_freq = self.rng.integers(
            low=difference_width,
            size=len(ids))
        norm_background_freq = mathutils.normalize_array(
            my_array=background_freq)
        background_freq = dict(zip(ids, norm_background_freq))
        return background_freq

    def simulate_background_freq_uniform(
            self,
            ids: List[str]) -> Dict[str, float]:
        """ Simulate equal background frequencies for all items

        Parameters
        ----------
        ids: List[str]
            The IDs of the items to assign frequency to

        Return
        ------
        background_freq: Dict[str, float]
            Probability assigned to each element of the given ids
        """
        uniform_background_freq = [1/len(ids) for _ in range(len(ids))]
        background_freq = dict(zip(ids, uniform_background_freq))
        return background_freq
