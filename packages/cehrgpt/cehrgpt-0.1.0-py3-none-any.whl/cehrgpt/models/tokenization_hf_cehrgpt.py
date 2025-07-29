import collections
import copy
import json
import os
import pickle
from functools import partial
from itertools import islice
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import scipy.stats as stats
import transformers
from cehrbert.models.hf_models.tokenization_utils import (
    agg_helper,
    agg_statistics,
    load_json_file,
)
from cehrbert.runners.hf_runner_argument_dataclass import DataTrainingArguments
from datasets import Dataset, DatasetDict
from femr.stat_utils import OnlineStatistics, ReservoirSampler
from scipy.interpolate import UnivariateSpline
from tokenizers import AddedToken, Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import WhitespaceSplit
from tokenizers.trainers import WordLevelTrainer
from tqdm import tqdm
from transformers import PreTrainedTokenizer
from transformers.utils import logging

from cehrgpt.gpt_utils import (
    convert_time_interval_to_time_tuple,
    extract_time_interval_in_days,
    is_att_token,
    is_inpatient_att_token,
)
from cehrgpt.models.pretrained_embeddings import PretrainedEmbeddings
from cehrgpt.models.special_tokens import (
    END_TOKEN,
    OUT_OF_VOCABULARY_TOKEN,
    PAD_TOKEN,
    START_TOKEN,
)

NUM_OF_BINS = 10
DEGREE_OF_FREEDOM = 3
SAMPLE_SIZE = 10_000
NA = "N/A"
UNKNOWN_BIN = "BIN:unknown"
NONE_BIN = "BIN:NONE"
TOKENIZER_FILE_NAME = "cehrgpt_tokenizer.json"
VALUE_TOKENIZER_FILE_NAME = "cehrgpt_value_tokenizer.json"
TIME_TOKENIZER_FILE_NAME = "cehrgpt_time_tokenizer.json"
TOKEN_TO_SUB_TIME_TOKEN_MAPPING_FILE_NAME = "token_to_sub_time_token_mapping.json"
LAB_STATS_FILE_NAME = "cehrgpt_lab_stats.pickle"
LEGACY_LAB_STATS_FILE_NAME = "cehrgpt_lab_stats.json"
CONCEPT_MAPPING_FILE_NAME = "concept_name_mapping.json"
LOG = logging.get_logger("transformers")


def truncated_sample(sample, standard_deviation):
    lower_quantile = stats.norm.cdf(-standard_deviation)
    upper_quantile = stats.norm.cdf(standard_deviation)
    lower_bound = np.quantile(sample, lower_quantile)
    upper_bound = np.quantile(sample, upper_quantile)
    return [x for x in sample if lower_bound <= x <= upper_bound]


def is_valid_valid_bin(token: str) -> bool:
    return token.startswith("BIN:")


def create_value_bin(bin_index: int) -> str:
    return "BIN:" + str(bin_index)


def create_sample_from_bins(bins, sample_size: int = 10_000) -> List[float]:
    """
    Generates a specified number of samples from a list of bins, each containing a fitted spline.

    This function iterates over each bin, extracts the spline, and uses it to generate a set of samples
    uniformly distributed along the x-axis defined by the spline's knots. It ensures that the total number
    of samples generated matches the specified sample size by distributing the number of samples evenly
    across the bins.

    Parameters:
        bins (List[Dict[str, UnivariateSpline]]): A list of dictionaries, each containing a 'spline' key
            with a UnivariateSpline object as its value. These splines define the data distribution within
            each bin from which samples are to be generated.
        sample_size (int, optional): The total number of samples to generate from all bins combined.
            Defaults to 10,000.

    Returns:
        List[float]: A list of sampled values, where each value is generated based on the spline functions
            provided in the bins. The total number of samples in the list will be equal to `sample_size`.

    Raises:
        ValueError: If `sample_size` is less than the number of bins, as it would not be possible to generate
            at least one sample per bin.

    Example:
        >>> x = np.linspace(0, 10, 100)
        >>> y = np.sin(x)
        >>> spline = UnivariateSpline(x, y, s=1)
        >>> bins = [{'spline': spline} for _ in range(5)]
        >>> samples = create_sample_from_bins(bins, 1000)
        >>> len(samples)
        1000

    Note:
        The function assumes that each bin's spline has a sufficient range of x-values (knots) to allow for
        meaningful sampling. If the range of x-values is too narrow, the uniformity of the sample distribution
        may be affected.
    """
    sample = []
    num_of_bins = len(bins)
    if num_of_bins > 0:
        sample_per_bin = sample_size // num_of_bins
        for value_bin in bins:
            bin_spline = value_bin["spline"]
            x = np.random.uniform(
                bin_spline.get_knots()[0], bin_spline.get_knots()[-1], sample_per_bin
            )
            y = bin_spline(x)
            sample.extend(y)
    return sample


def create_bins_with_spline(samples, num_bins, d_freedom=3) -> List[Dict[str, Any]]:
    """
    Divides a list of numeric samples into a specified number of bins and fits a spline to the data in each bin.

    This function first sorts the list of samples, then partitions the sorted list into `num_bins` bins. For each bin,
    a UnivariateSpline is fitted to the data within the bin, using the specified degrees of freedom. The function
    handles edge cases by assigning infinity to the bounds of the first and last bins.

    Parameters:
        samples (List[float]): A list of sample data points, which are real numbers.
        num_bins (int): The number of bins to divide the sample data into. It is assumed that there are enough samples to at least fill the bins to the minimum required for spline fitting.
        d_freedom (int, optional): The degree of freedom for the spline. Default is 1, which fits a linear spline.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a bin. Each dictionary contains:
            - 'bin_index' (int): The index of the bin.
            - 'start_val' (float): The starting value of the bin, with the first bin starting at negative infinity.
            - 'end_val' (float): The ending value of the bin, with the last bin ending at positive infinity.
            - 'spline' (UnivariateSpline): The spline object fitted to the data within the bin.

    Raises:
        ValueError: If `num_bins` is less than 1 or if there are insufficient samples to create the specified number of bins with the required minimum data points per bin.

    Example:
        >>> samples = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> bins = create_bins_with_spline(samples, 2)
        >>> for b in bins:
        ...     print(b['bin_index'], b['start_val'], b['end_val'])
        ...
        0 -inf 5.5
        1 5.5 inf

    Note:
        The function assumes that each bin will have at least `d_freedom + 1` samples to fit the spline. If the total number of samples is less than `num_bins * (d_freedom + 1)`, no bins will be created.
    """
    samples.sort()
    bins = []
    if len(samples) >= num_bins * (d_freedom + 1):
        samples_per_bin = len(samples) // num_bins
        for bin_index in range(0, num_bins):
            if bin_index == 0:
                start_val = float("-inf")
            else:
                start_val = samples[bin_index * samples_per_bin]

            if bin_index == num_bins - 1:
                end_val = float("inf")
            else:
                end_val = samples[(bin_index + 1) * samples_per_bin]
            x = range(bin_index * samples_per_bin, (bin_index + 1) * samples_per_bin)
            y = samples[bin_index * samples_per_bin : (bin_index + 1) * samples_per_bin]
            spline = UnivariateSpline(x, y, k=d_freedom)
            bins.append(
                {
                    "bin_index": bin_index,
                    "start_val": start_val,
                    "end_val": end_val,
                    "spline": spline,
                }
            )
    return bins


def map_statistics(batch: Dict[str, Any], size=10_000) -> Dict[str, Any]:
    if "units" in batch:
        batch_value_units = batch["units"]
    else:
        batch_value_units = [[NA for _ in cons] for cons in batch["concept_ids"]]

    if "number_as_values" not in batch:
        batched_number_as_values = [
            [value if isinstance(value, float) else None for value in concept_values]
            for concept_values in batch["concept_values"]
        ]
    else:
        batched_number_as_values = batch["number_as_values"]

    if "concept_as_values" not in batch:
        batched_concept_as_values = [
            [value if isinstance(value, str) else None for value in concept_values]
            for concept_values in batch["concept_values"]
        ]
    else:
        batched_concept_as_values = batch["concept_as_values"]

    numeric_stats_by_lab = collections.defaultdict(partial(ReservoirSampler, size=size))
    categorical_stats_by_lab = collections.defaultdict(int)
    for (
        concept_ids,
        number_as_values,
        concept_as_values,
        concept_value_indicators,
        units,
    ) in zip(
        batch["concept_ids"],
        batched_number_as_values,
        batched_concept_as_values,
        batch["concept_value_masks"],
        batch_value_units,
    ):
        for (
            concept_id,
            number_as_value,
            concept_as_value,
            concept_value_indicator,
            unit,
        ) in zip(
            concept_ids,
            number_as_values,
            concept_as_values,
            concept_value_indicators,
            units,
        ):
            if concept_value_indicator == 1:
                if number_as_value:
                    numeric_stats_by_lab[(concept_id, unit)].add(number_as_value, 1)
                if concept_as_value:
                    categorical_stats_by_lab[(concept_id, concept_as_value)] += 1

    return {
        "numeric_stats_by_lab": numeric_stats_by_lab,
        "categorical_stats_by_lab": categorical_stats_by_lab,
    }


def create_numeric_concept_unit_mapping(
    lab_stats: List[Dict[str, Any]]
) -> Tuple[Dict[str, List[float]], Dict[str, List[str]]]:
    numeric_concept_unit_mapping = collections.defaultdict(list)
    for each_lab_stat in lab_stats:
        numeric_concept_unit_mapping[each_lab_stat["concept_id"]].append(
            (each_lab_stat["count"], each_lab_stat["unit"])
        )

    concept_prob_mapping = dict()
    concept_unit_mapping = dict()
    for concept_id in numeric_concept_unit_mapping.keys():
        counts, units = zip(*numeric_concept_unit_mapping[concept_id])
        total_count = sum(counts)
        probs = [float(c) / total_count for c in counts]
        concept_prob_mapping[concept_id] = probs
        concept_unit_mapping[concept_id] = units
    return concept_prob_mapping, concept_unit_mapping


class NumericEventStatistics:
    def __init__(self, lab_stats: List[Dict[str, Any]]):
        self._lab_stats = lab_stats
        self._lab_stats_mapping = {
            (lab_stat["concept_id"], lab_stat["unit"]): {
                "unit": lab_stat["unit"],
                "mean": lab_stat["mean"],
                "std": lab_stat["std"],
                "value_outlier_std": lab_stat["value_outlier_std"],
                "bins": lab_stat["bins"],
            }
            for lab_stat in lab_stats
        }
        self._concept_prob_mapping, self._concept_unit_mapping = (
            create_numeric_concept_unit_mapping(lab_stats)
        )

    def get_numeric_concept_ids(self) -> List[str]:
        return [_["concept_id"] for _ in self._lab_stats]

    def get_random_unit(self, concept_id: str) -> str:
        if concept_id in self._concept_prob_mapping:
            unit_probs = self._concept_prob_mapping[concept_id]
            return np.random.choice(
                self._concept_unit_mapping[concept_id], p=unit_probs
            )
        return NA

    def normalize(
        self, concept_id: str, unit: str, concept_value: Union[float, str]
    ) -> str:
        if isinstance(concept_value, float):
            if (concept_id, unit) in self._lab_stats_mapping:
                concept_unit_stats = self._lab_stats_mapping[(concept_id, unit)]
                bins = concept_unit_stats["bins"]
                if bins:
                    for each_bin in bins:
                        if (
                            each_bin["start_val"]
                            <= concept_value
                            <= each_bin["end_val"]
                        ):
                            return create_value_bin(each_bin["bin_index"])
        return UNKNOWN_BIN

    def denormalize(
        self, concept_id: str, value_bin: str
    ) -> Tuple[Optional[Union[float, str]], str]:
        unit = self.get_random_unit(concept_id)
        concept_value = value_bin
        if (
            is_valid_valid_bin(value_bin)
            and (concept_id, unit) in self._lab_stats_mapping
        ):
            lab_stats = self._lab_stats_mapping[(concept_id, unit)]
            bin_index = value_bin.split(":")[1]
            if bin_index.isnumeric():
                bin_index = int(bin_index)
                # There are rare cases during sequence generation where bin_index could be out of range
                # when there are no bins for (concept_id, unit) due to the small number of values in the source data
                if len(lab_stats["bins"]) > bin_index:
                    assert bin_index == lab_stats["bins"][bin_index]["bin_index"]
                    bin_spline = lab_stats["bins"][bin_index]["spline"]
                    x = np.random.uniform(
                        bin_spline.get_knots()[0], bin_spline.get_knots()[-1]
                    )
                    concept_value = bin_spline(x).item()
        return concept_value, unit


class CehrGptTokenizer(PreTrainedTokenizer):

    def __init__(
        self,
        tokenizer: Tokenizer,
        value_tokenizer: Tokenizer,
        att_tokenizer: Tokenizer,
        token_to_sub_time_token_mapping: Dict[str, List[str]],
        numeric_lab_stats: List[Dict[str, Any]],
        categorical_lab_stats: Dict[Tuple[str, str], int],
        concept_name_mapping: Dict[str, str],
        pretrained_concept_embedding_model: PretrainedEmbeddings = None,
    ):
        self._tokenizer = tokenizer
        self._value_tokenizer = value_tokenizer
        self._att_tokenizer = att_tokenizer
        self._token_to_sub_time_token_mapping = token_to_sub_time_token_mapping
        self._numeric_lab_stats = numeric_lab_stats
        self._numeric_event_statistics = NumericEventStatistics(numeric_lab_stats)
        self._categorical_lab_stats = categorical_lab_stats
        self._concept_name_mapping = concept_name_mapping
        self._oov_token_id = self._tokenizer.token_to_id(OUT_OF_VOCABULARY_TOKEN)
        self._padding_token_id = self._tokenizer.token_to_id(PAD_TOKEN)
        self._start_token_id = self._tokenizer.token_to_id(START_TOKEN)
        self._end_token_id = self._tokenizer.token_to_id(END_TOKEN)
        self._numeric_concept_ids = (
            self._numeric_event_statistics.get_numeric_concept_ids()
        )
        self._categorical_concept_ids = list(
            {t[0] for t in self._categorical_lab_stats.keys()}
        )
        self._padding_value_token_id = self._value_tokenizer.token_to_id(PAD_TOKEN)
        self._pretrained_concept_embedding_model = (
            pretrained_concept_embedding_model
            if pretrained_concept_embedding_model
            else PretrainedEmbeddings(None)
        )
        self._pretrained_concept_ids = [
            _
            for _ in self.get_vocab().keys()
            if self._pretrained_concept_embedding_model.is_concept_available(_)
        ]

        super().__init__()

    @property
    def pretrained_concept_ids(self):
        return self._pretrained_concept_ids

    @property
    def pretrained_token_ids(self):
        return self.encode(self._pretrained_concept_ids)

    @property
    def pretrained_embeddings(self):
        return np.asarray(
            [
                self._pretrained_concept_embedding_model.get_concept_embeddings(_)
                for _ in self._pretrained_concept_ids
            ]
        )

    @property
    def vocab_size(self) -> int:
        return self._tokenizer.get_vocab_size()

    @property
    def value_vocab_size(self) -> int:
        return self._value_tokenizer.get_vocab_size()

    @property
    def time_token_vocab_size(self) -> int:
        return self._att_tokenizer.get_vocab_size()

    @property
    def pad_value_token_id(self):
        return self._padding_value_token_id

    @property
    def start_token_id(self):
        return self._start_token_id

    @property
    def end_token_id(self):
        return self._end_token_id

    @property
    def end_token(self):
        return END_TOKEN

    @property
    def eos_token(self):
        return END_TOKEN

    @property
    def eos_token_id(self):
        return self._end_token_id

    @property
    def pad_token_id(self):
        return self._padding_token_id

    @property
    def pad_token(self):
        return PAD_TOKEN

    @property
    def numeric_concept_ids(self):
        return self._numeric_concept_ids

    @property
    def categorical_concept_ids(self):
        return self._categorical_concept_ids

    @property
    def lab_token_ids(self):
        reserved_tokens = [START_TOKEN, PAD_TOKEN, END_TOKEN, OUT_OF_VOCABULARY_TOKEN]
        return self.encode(
            [
                concept_id
                for concept_id in self._numeric_concept_ids
                + self._categorical_concept_ids
                if concept_id not in reserved_tokens
            ]
        )

    @property
    def token_to_time_token_mapping(self) -> Dict[int, List[int]]:
        default_mapping = {-1: [0, 0, 0]}
        default_mapping.update(
            {
                self._tokenizer.token_to_id(time_token): list(
                    map(self._att_tokenizer.token_to_id, sub_time_tokens)
                )
                for time_token, sub_time_tokens in self._token_to_sub_time_token_mapping.items()
            }
        )
        return default_mapping

    @property
    def pretrained_concept_embedding_model(self):
        return self._pretrained_concept_embedding_model

    def get_vocab(self) -> Dict[str, int]:
        return self._tokenizer.get_vocab()

    def get_value_vocab(self) -> Dict[str, int]:
        return self._value_tokenizer.get_vocab()

    def encode(self, concept_ids, **kwargs) -> Sequence[int]:
        encoded = self._tokenizer.encode(concept_ids, is_pretokenized=True)
        return encoded.ids

    def decode(
        self, concept_token_ids: List[int], skip_special_tokens: bool = True, **kwargs
    ) -> List[str]:
        return self._tokenizer.decode(
            concept_token_ids, skip_special_tokens=skip_special_tokens
        ).split(" ")

    def encode_value(self, concept_values: Sequence[str]) -> Sequence[int]:
        encoded = self._value_tokenizer.encode(concept_values, is_pretokenized=True)
        return encoded.ids

    def decode_value(
        self, concept_value_token_ids: List[int], skip_special_tokens: bool = True
    ) -> List[str]:
        return self._value_tokenizer.decode(
            concept_value_token_ids, skip_special_tokens=skip_special_tokens
        ).split(" ")

    def _convert_token_to_id(self, token):
        """Converts a token (str) in an id using the vocab."""
        token_id = self._tokenizer.token_to_id(token)
        return token_id if token_id else self._oov_token_id

    def _convert_id_to_token(self, index):
        """Converts an index (integer) in a token (str) using the vocab."""
        token = self._tokenizer.id_to_token(index)
        return token if token else OUT_OF_VOCABULARY_TOKEN

    def convert_tokens_to_string(self, tokens):
        """Converts a sequence of tokens (string) in a single string."""
        out_string = " ".join([self._concept_name_mapping[t] for t in tokens])
        return out_string

    def save_pretrained(
        self,
        save_directory: Union[str, os.PathLike],
        push_to_hub: bool = False,
        **kwargs,
    ):
        """
        Save the Cehrbert tokenizer.

        This method make sure the batch processor can then be re-loaded using the
        .from_pretrained class method.

        Args:
            save_directory (`str` or `os.PathLike`): The path to a directory where the tokenizer will be saved.
            push_to_hub (`bool`, *optional*, defaults to `False`):
                Whether or not to push your model to the Hugging Face model hub after saving it. You can specify the
                repository you want to push to with `repo_id` (will default to the name of `save_directory` in your
                namespace).
            kwargs (`Dict[str, Any]`, *optional*):
                Additional key word arguments passed along to the [`PushToHubMixin.push_to_hub`] method.
        """
        assert not os.path.isfile(
            save_directory
        ), f"Provided path ({save_directory}) should be a directory, not a file"

        os.makedirs(save_directory, exist_ok=True)

        if push_to_hub:
            commit_message = kwargs.pop("commit_message", None)
            repo_id = kwargs.pop("repo_id", str(save_directory).split(os.path.sep)[-1])
            repo_id = self._create_repo(repo_id, **kwargs)
            files_timestamps = self._get_files_timestamps(save_directory)

        self._tokenizer.save(os.path.join(save_directory, TOKENIZER_FILE_NAME))

        self._value_tokenizer.save(
            os.path.join(save_directory, VALUE_TOKENIZER_FILE_NAME)
        )

        self._att_tokenizer.save(os.path.join(save_directory, TIME_TOKENIZER_FILE_NAME))

        with open(
            os.path.join(save_directory, TOKEN_TO_SUB_TIME_TOKEN_MAPPING_FILE_NAME), "w"
        ) as f:
            json.dump(self._token_to_sub_time_token_mapping, f)

        with open(os.path.join(save_directory, LAB_STATS_FILE_NAME), "wb") as f:
            lab_stats = {
                "numeric_lab_stats": self._numeric_lab_stats,
                "categorical_lab_stats": self._categorical_lab_stats,
            }
            pickle.dump(lab_stats, f)

        with open(os.path.join(save_directory, CONCEPT_MAPPING_FILE_NAME), "w") as f:
            json.dump(self._concept_name_mapping, f)

        self._pretrained_concept_embedding_model.save(save_directory)

        if push_to_hub:
            self._upload_modified_files(
                save_directory,
                repo_id,
                files_timestamps,
                commit_message=commit_message,
                token=kwargs.get("token"),
            )

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Union[str, os.PathLike],
        **kwargs,
    ):
        """
        Load the CehrBert tokenizer.

        Parameters:
            pretrained_model_name_or_path (`str` or `os.PathLike`, *optional*):
                Can be either:
                    - A string, the *model id* of a pretrained model hosted inside a model repo on huggingface.co.
                      Valid model ids can be located at the root-level, like `bert-base-uncased`, or namespaced under a
                      user or organization name, like `dbmdz/bert-base-german-cased`.
                    - A path to a *directory* containing tokenization data saved using
                      [`save_pretrained`], e.g., `./my_data_directory/`.
            kwargs: Arguments for loading to pass to transformers.utils.hub.cached_file

        Returns:
            A CehrBert Tokenizer
        """

        is_legacy_tokenizer = CehrGptTokenizer.is_legacy_tokenizer(
            pretrained_model_name_or_path, **kwargs
        )

        # Load the concept tokenizer
        tokenizer_file = transformers.utils.hub.cached_file(
            pretrained_model_name_or_path, TOKENIZER_FILE_NAME, **kwargs
        )
        if not tokenizer_file:
            return None
        tokenizer = Tokenizer.from_file(tokenizer_file)

        # Load the concept_value_tokenizer
        if is_legacy_tokenizer:
            value_tokenizer = Tokenizer(
                WordLevel(unk_token=OUT_OF_VOCABULARY_TOKEN, vocab=dict())
            )
        else:
            value_tokenizer_file = transformers.utils.hub.cached_file(
                pretrained_model_name_or_path, VALUE_TOKENIZER_FILE_NAME, **kwargs
            )
            if not value_tokenizer_file:
                return None
            value_tokenizer = Tokenizer.from_file(value_tokenizer_file)

        # Load the ttt tokenizer
        att_tokenizer_file = transformers.utils.hub.cached_file(
            pretrained_model_name_or_path, TIME_TOKENIZER_FILE_NAME, **kwargs
        )
        if not att_tokenizer_file:
            return None
        att_tokenizer = Tokenizer.from_file(att_tokenizer_file)

        # Load the sub time token json file
        token_to_sub_time_token_mapping_file = transformers.utils.hub.cached_file(
            pretrained_model_name_or_path,
            TOKEN_TO_SUB_TIME_TOKEN_MAPPING_FILE_NAME,
            **kwargs,
        )
        if not token_to_sub_time_token_mapping_file:
            return None
        token_to_sub_time_token_mapping = load_json_file(
            token_to_sub_time_token_mapping_file
        )

        # Load the lab stats pickle file
        if is_legacy_tokenizer:
            legacy_lab_stats_file = transformers.utils.hub.cached_file(
                pretrained_model_name_or_path, LEGACY_LAB_STATS_FILE_NAME, **kwargs
            )
            if not legacy_lab_stats_file:
                return None
            # Support the old version of the numeric lab stats file
            lab_stats = {
                "numeric_lab_stats": load_json_file(legacy_lab_stats_file),
                "categorical_lab_stats": dict(),
            }
        else:
            lab_stats_file = transformers.utils.hub.cached_file(
                pretrained_model_name_or_path, LAB_STATS_FILE_NAME, **kwargs
            )
            if not lab_stats_file:
                return None

            with open(lab_stats_file, "rb") as file:
                lab_stats = pickle.load(file)

        # Load the concept_name json file
        concept_name_mapping_file = transformers.utils.hub.cached_file(
            pretrained_model_name_or_path, CONCEPT_MAPPING_FILE_NAME, **kwargs
        )
        if not concept_name_mapping_file:
            return None
        concept_name_mapping = load_json_file(concept_name_mapping_file)

        pretrained_embedding_model = PretrainedEmbeddings(pretrained_model_name_or_path)

        return CehrGptTokenizer(
            tokenizer,
            value_tokenizer,
            att_tokenizer,
            token_to_sub_time_token_mapping,
            lab_stats["numeric_lab_stats"],
            lab_stats["categorical_lab_stats"],
            concept_name_mapping,
            pretrained_embedding_model,
        )

    @classmethod
    def is_legacy_tokenizer(
        cls, pretrained_model_name_or_path: Union[str, os.PathLike], **kwargs
    ):
        try:
            legacy_lab_stats_file = transformers.utils.hub.cached_file(
                pretrained_model_name_or_path, LEGACY_LAB_STATS_FILE_NAME, **kwargs
            )
            return legacy_lab_stats_file is not None
        except Exception:
            return False

    @classmethod
    def expand_trained_tokenizer(
        cls,
        cehrgpt_tokenizer,
        dataset: Union[Dataset, DatasetDict],
        concept_name_mapping: Dict[str, str],
        data_args: DataTrainingArguments,
        pretrained_concept_embedding_model: PretrainedEmbeddings = None,
    ):
        if not isinstance(cehrgpt_tokenizer, CehrGptTokenizer):
            raise ValueError(
                "The existing cehrgpt must be an instance of CehrGptTokenizer"
            )

        cehrgpt_tokenizer_copy = copy.deepcopy(cehrgpt_tokenizer)

        new_tokenizer = CehrGptTokenizer.train_tokenizer(
            dataset=dataset,
            concept_name_mapping=concept_name_mapping,
            data_args=data_args,
        )

        new_tokens = set(new_tokenizer.get_vocab().keys()) - set(
            cehrgpt_tokenizer_copy.get_vocab().keys()
        )
        new_value_tokens = set(new_tokenizer.get_value_vocab().keys()) - set(
            cehrgpt_tokenizer_copy.get_value_vocab().keys()
        )
        new_att_tokens = set(new_tokenizer._att_tokenizer.get_vocab().keys()) - set(
            cehrgpt_tokenizer_copy._att_tokenizer.get_vocab().keys()
        )
        new_token_to_sub_time_token_mapping = (
            new_tokenizer._token_to_sub_time_token_mapping
        )
        new_numeric_lab_stats = new_tokenizer._numeric_lab_stats
        new_categorical_lab_stats = new_tokenizer._categorical_lab_stats
        new_concept_name_mapping = new_tokenizer._concept_name_mapping

        # Add new tokens to the existing tokenizer
        cehrgpt_tokenizer_copy._tokenizer.add_tokens(
            [
                AddedToken(token, single_word=True, normalized=False)
                for token in new_tokens
            ]
        )
        # Add new tokens to the existing value tokenizer
        cehrgpt_tokenizer_copy._value_tokenizer.add_tokens(
            [
                AddedToken(token, single_word=True, normalized=False)
                for token in new_value_tokens
            ]
        )
        # Add new time tokens to the existing att tokenizer
        cehrgpt_tokenizer_copy._att_tokenizer.add_tokens(
            [
                AddedToken(token, single_word=True, normalized=False)
                for token in new_att_tokens
            ]
        )
        # Merge the time_token -> List[sub_time_tokens] mapping
        for time_token, sub_time_tokens in new_token_to_sub_time_token_mapping.items():
            if (
                time_token
                not in cehrgpt_tokenizer_copy._token_to_sub_time_token_mapping
            ):
                cehrgpt_tokenizer_copy._token_to_sub_time_token_mapping[time_token] = (
                    sub_time_tokens
                )

        # Merge numeric lab_stats
        cehrgpt_tokenizer_copy._numeric_lab_stats = cls.merge_numeric_lab_stats(
            cehrgpt_tokenizer_copy._numeric_lab_stats,
            new_numeric_lab_stats,
        )
        # Merge categorical lab_stats
        cehrgpt_tokenizer_copy._categorical_lab_stats = cls.merge_categorical_lab_stats(
            cehrgpt_tokenizer_copy._categorical_lab_stats,
            new_categorical_lab_stats,
        )

        # Merge concept_name_mapping
        for token, concept_name in new_concept_name_mapping.items():
            if token not in cehrgpt_tokenizer_copy._concept_name_mapping:
                cehrgpt_tokenizer_copy._concept_name_mapping[token] = concept_name

        return CehrGptTokenizer(
            tokenizer=cehrgpt_tokenizer_copy._tokenizer,
            value_tokenizer=cehrgpt_tokenizer_copy._value_tokenizer,
            att_tokenizer=cehrgpt_tokenizer_copy._att_tokenizer,
            token_to_sub_time_token_mapping=cehrgpt_tokenizer_copy._token_to_sub_time_token_mapping,
            numeric_lab_stats=cehrgpt_tokenizer_copy._numeric_lab_stats,
            categorical_lab_stats=cehrgpt_tokenizer_copy._categorical_lab_stats,
            concept_name_mapping=cehrgpt_tokenizer_copy._concept_name_mapping,
            pretrained_concept_embedding_model=pretrained_concept_embedding_model,
        )

    @classmethod
    def merge_numeric_lab_stats(
        cls,
        lab_stats_existing: List[Dict[str, Any]],
        lab_stats_new: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        lab_stats_existing_mapping = {
            (lab_stat["concept_id"], lab_stat["unit"]): lab_stat
            for lab_stat in lab_stats_existing
        }
        for lab_stat in lab_stats_new:
            concept_unit_pair = (lab_stat["concept_id"], lab_stat["unit"])
            if concept_unit_pair in lab_stats_existing_mapping:
                existing = OnlineStatistics()
                existing.count = lab_stats_existing_mapping[concept_unit_pair]["count"]
                existing.current_mean = lab_stats_existing_mapping[concept_unit_pair][
                    "mean"
                ]
                existing.variance = (
                    lab_stats_existing_mapping[concept_unit_pair]["std"] ** 2
                    * existing.count
                )
                new = OnlineStatistics()
                new.count = lab_stat["count"]
                new.current_mean = lab_stat["mean"]
                new.variance = lab_stat["std"] ** 2 * new.count
                existing.combine(new)
                lab_stats_existing_mapping[concept_unit_pair]["mean"] = existing.mean()
                lab_stats_existing_mapping[concept_unit_pair][
                    "std"
                ] = existing.standard_deviation()
                lab_stats_existing_mapping[concept_unit_pair]["count"] = existing.count
                # recreate the bins
                sample = create_sample_from_bins(
                    lab_stats_existing_mapping[concept_unit_pair]["bins"]
                )
                sample.extend(create_sample_from_bins(lab_stat["bins"]))
                lab_stats_existing_mapping[concept_unit_pair]["bins"] = (
                    create_bins_with_spline(sample, NUM_OF_BINS, DEGREE_OF_FREEDOM)
                )

            else:
                if lab_stat["count"] > 0:
                    lab_stats_existing_mapping[concept_unit_pair] = lab_stat

        return list(lab_stats_existing_mapping.values())

    @classmethod
    def merge_categorical_lab_stats(
        cls,
        categorical_lab_stats_existing: Dict[Tuple[str, str], int],
        categorical_lab_stats_new: Dict[Tuple[str, str], int],
    ) -> Dict[Tuple[str, str], int]:
        for (concept_id, concept_as_value), count in categorical_lab_stats_new.items():
            if (concept_id, concept_as_value) not in categorical_lab_stats_new:
                categorical_lab_stats_existing[(concept_id, concept_as_value)] = 0
            categorical_lab_stats_existing[(concept_id, concept_as_value)] += count
        return categorical_lab_stats_existing

    @classmethod
    def train_tokenizer(
        cls,
        dataset: Union[Dataset, DatasetDict],
        concept_name_mapping: Dict[str, str],
        data_args: DataTrainingArguments,
        pretrained_concept_embedding_model: PretrainedEmbeddings = None,
    ):
        """
        Train a huggingface word level tokenizer.

        To use their tokenizer, we need to concatenate all the concepts
        together and treat it as a sequence.
        """

        if isinstance(dataset, DatasetDict):
            dataset = dataset["train"]

        LOG.info("Training the tokenizer for concepts")
        concept_tokenizer = cls.train_concept_tokenizer(
            dataset,
            feature_name="concept_ids",
            special_tokens=[PAD_TOKEN, OUT_OF_VOCABULARY_TOKEN, START_TOKEN, END_TOKEN],
            unk_token=OUT_OF_VOCABULARY_TOKEN,
            data_args=data_args,
        )
        concept_value_column = "concept_as_values"
        for row in dataset:
            if concept_value_column not in row:
                concept_value_column = "concept_values"
            break
        LOG.info("Training the tokenizer for values")
        value_tokenizer = cls.train_concept_tokenizer(
            dataset,
            feature_name=concept_value_column,
            special_tokens=[OUT_OF_VOCABULARY_TOKEN, PAD_TOKEN],
            unk_token=OUT_OF_VOCABULARY_TOKEN,
            data_args=data_args,
        )
        value_tokenizer.add_tokens(
            [
                AddedToken(_, single_word=True, normalized=False)
                for _ in [create_value_bin(_) for _ in range(NUM_OF_BINS)]
                + [UNKNOWN_BIN, NONE_BIN]
            ]
        )

        map_statistics_partial = partial(map_statistics, size=SAMPLE_SIZE)

        if data_args.streaming:
            first_example = next(iter(dataset))
            parts = dataset.map(
                partial(agg_helper, map_func=map_statistics_partial),
                batched=True,
                batch_size=data_args.preprocessing_batch_size,
                remove_columns=first_example.keys(),
            )
        else:
            parts = dataset.map(
                partial(agg_helper, map_func=map_statistics_partial),
                batched=True,
                batch_size=data_args.preprocessing_batch_size,
                remove_columns=dataset.column_names,
                num_proc=data_args.preprocessing_num_workers,
                keep_in_memory=True,
                new_fingerprint="invalid",
            )
        current = None
        for stat in tqdm(parts, desc="Aggregating the lab statistics"):
            fixed_stat = pickle.loads(stat["data"])
            if current is None:
                current = fixed_stat
            else:
                current = agg_statistics(current, fixed_stat)

        numeric_lab_stats = []
        for (concept_id, unit), online_stats in current["numeric_stats_by_lab"].items():
            if len(online_stats.samples) == 0:
                continue
            samples = truncated_sample(
                online_stats.samples, data_args.value_outlier_std
            )
            bins = create_bins_with_spline(samples, NUM_OF_BINS, DEGREE_OF_FREEDOM)
            if len(bins) > 0:
                numeric_lab_stats.append(
                    {
                        "concept_id": concept_id,
                        "unit": unit,
                        "mean": np.mean(samples),
                        "std": np.std(samples),
                        "count": len(online_stats.samples),
                        "value_outlier_std": data_args.value_outlier_std,
                        "bins": bins,
                    }
                )

        categorical_lab_stats = collections.defaultdict(int)
        for (concept_id, value_as_concept), count in current[
            "categorical_stats_by_lab"
        ].items():
            categorical_lab_stats[(concept_id, value_as_concept)] += count

        # We will train a tokenizer specifically for time intervals
        sub_time_token_data = []
        token_to_sub_time_token_mapping = collections.defaultdict(list)
        for token, token_id in concept_tokenizer.get_vocab().items():
            if is_att_token(token):
                time_interval = extract_time_interval_in_days(token)
                time_tuple = convert_time_interval_to_time_tuple(
                    time_interval, is_inpatient_att_token(token)
                )
                token_to_sub_time_token_mapping[token] = list(time_tuple)
                sub_time_token_data.append(" ".join(time_tuple))

        att_tokenizer = Tokenizer(
            WordLevel(unk_token=OUT_OF_VOCABULARY_TOKEN, vocab=dict())
        )
        att_tokenizer.pre_tokenizer = WhitespaceSplit()
        att_trainer = WordLevelTrainer(
            special_tokens=[OUT_OF_VOCABULARY_TOKEN],
            vocab_size=data_args.vocab_size,
            min_frequency=0,
            show_progress=True,
        )
        att_tokenizer.train_from_iterator(sub_time_token_data, trainer=att_trainer)

        return CehrGptTokenizer(
            concept_tokenizer,
            value_tokenizer,
            att_tokenizer,
            token_to_sub_time_token_mapping,
            numeric_lab_stats,
            categorical_lab_stats,
            concept_name_mapping,
            pretrained_concept_embedding_model,
        )

    @classmethod
    def train_concept_tokenizer(
        cls,
        dataset,
        feature_name,
        special_tokens: List[str],
        unk_token,
        data_args,
    ):
        # Use the Fast Tokenizer from the Huggingface tokenizers Rust implementation.
        # https://github.com/huggingface/tokenizers
        concept_tokenizer = Tokenizer(WordLevel(unk_token=unk_token, vocab=dict()))
        concept_tokenizer.pre_tokenizer = WhitespaceSplit()
        concept_trainer = WordLevelTrainer(
            special_tokens=special_tokens,
            vocab_size=data_args.vocab_size,
            min_frequency=data_args.min_frequency,
            show_progress=True,
        )
        batch_concat_concepts_partial_func = partial(
            cls.batch_concat_concepts, feature_name=feature_name
        )
        if data_args.streaming:
            concatenated_features = dataset.map(
                batch_concat_concepts_partial_func,
                batched=True,
                batch_size=data_args.preprocessing_batch_size,
            )

            def batched_generator():
                iterator = iter(concatenated_features)
                while True:
                    batch = list(islice(iterator, data_args.preprocessing_batch_size))
                    if not batch:
                        break
                    yield [example[feature_name] for example in batch]

            # We pass a generator of list of texts (concatenated concept_ids) to train_from_iterator
            # for efficient training
            generator = batched_generator()
        else:
            concatenated_features = dataset.map(
                batch_concat_concepts_partial_func,
                num_proc=data_args.preprocessing_num_workers,
                batched=True,
                batch_size=data_args.preprocessing_batch_size,
                remove_columns=dataset.column_names,
            )
            generator = concatenated_features[feature_name]
        concept_tokenizer.train_from_iterator(generator, trainer=concept_trainer)
        return concept_tokenizer

    def normalize(self, concept_id: str, unit: str, concept_value: float) -> str:
        return self._numeric_event_statistics.normalize(concept_id, unit, concept_value)

    def denormalize(self, concept_id: str, value_bin: str) -> Tuple[float, str]:
        return self._numeric_event_statistics.denormalize(concept_id, value_bin)

    @classmethod
    def batch_concat_concepts(
        cls, records: Dict[str, List], feature_name
    ) -> Dict[str, List]:
        return {
            feature_name: [
                " ".join(
                    [token for token in tokens if token and isinstance(token, str)]
                )
                for tokens in records[feature_name]
            ]
        }
