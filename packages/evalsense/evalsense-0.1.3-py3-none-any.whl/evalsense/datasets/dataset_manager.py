from abc import abstractmethod
from pathlib import Path
import shutil
from typing import Protocol, cast

from datasets import Dataset, DatasetDict, concatenate_datasets, load_from_disk
from pydantic import BaseModel

from evalsense.constants import DEFAULT_VERSION_NAME, DATA_PATH
from evalsense.datasets.dataset_config import DatasetConfig, OnlineSource
from evalsense.utils.files import to_safe_filename, download_file


class DatasetRecord(BaseModel, frozen=True):
    """A record identifying a dataset.

    Attributes:
        name (str): The name of the dataset.
        version (str): The version of the dataset.
        splits (list[str]): The used dataset splits.
    """

    name: str
    version: str
    splits: tuple[str, ...]


class DatasetManager(Protocol):
    """An abstract class for managing datasets.

    Attributes:
        name (str): The name of the dataset.
        config (DatasetConfig): The configuration for the dataset.
        version (str): The used dataset version.
        splits (list[str]): The dataset splits to retrieve.
        priority (int): The priority of the dataset manager.
        data_path (Path): The top-level directory for storing all datasets.
        dataset (Dataset | None): The loaded dataset.
    """

    name: str
    config: DatasetConfig
    version: str
    splits: list[str]
    priority: int
    data_path: Path
    dataset: Dataset | None = None
    dataset_dict: DatasetDict | None = None

    def __init__(
        self,
        name: str,
        version: str = DEFAULT_VERSION_NAME,
        splits: list[str] | None = None,
        priority: int = 10,
        data_dir: str | None = None,
        **kwargs,
    ):
        """Initializes a new DatasetManager.

        Args:
            name (str): The name of the dataset.
            version (str): The dataset version to retrieve.
            splits (list[str], optional): The dataset splits to retrieve.
            priority (int, optional): The priority of the dataset manager when
                choosing between multiple possible managers. Recommended values
                range from 0 to 10, with 10 (the highest) being the default.
            data_dir (str, optional): The top-level directory for storing all
                datasets. Defaults to "datasets" in the user cache directory.
            **kwargs (dict): Additional keyword arguments.
        """
        self.name = name
        self.config = DatasetConfig(name)
        self.version = version
        self.priority = priority
        if data_dir is not None:
            self.data_path = Path(data_dir)
        else:
            self.data_path = DATA_PATH

        if splits is None:
            splits = list(self.config.get_splits(self.version).keys())
        self.splits = sorted(splits)

    @property
    def dataset_path(self) -> Path:
        """The top-level directory for storing this dataset.

        Returns:
            (Path): The dataset directory.
        """
        return self.data_path / to_safe_filename(self.name)

    @property
    def version_path(self) -> Path:
        """The directory for storing a specific version of this dataset.

        Returns:
            (Path): The dataset version directory.
        """
        return self.dataset_path / to_safe_filename(self.version)

    @property
    def main_data_path(self) -> Path:
        """The path for storing the preprocessed dataset files for a specific version.

        Returns:
            (Path): The main dataset directory.
        """
        return self.version_path / "main"

    @property
    def record(self) -> DatasetRecord:
        """Returns a record identifying the dataset.

        Returns:
            (DatasetRecord): The dataset record.
        """
        return DatasetRecord(
            name=self.name,
            version=self.version,
            splits=tuple(self.splits),
        )

    def _retrieve_files(self, **kwargs) -> None:
        """Retrieves  dataset files.

        This method retrieves all the dataset files for the specified splits
        into the `self.version_path` directory.

        Args:
            **kwargs (dict): Additional keyword arguments.
        """
        for filename, file_metadata in self.config.get_files(
            self.version, self.splits
        ).items():
            effective_source = file_metadata.effective_source
            if effective_source is not None and isinstance(
                effective_source, OnlineSource
            ):
                download_file(
                    effective_source.url_template.format(
                        version=self.version, filename=filename
                    ),
                    self.version_path / filename,
                    expected_hash=file_metadata.hash,
                    hash_type=file_metadata.hash_type,
                )

    @abstractmethod
    def _preprocess_files(self, **kwargs) -> None:
        """Preprocesses the downloaded dataset files.

        This method preprocesses the retrieved dataset files and saves them
        as a HuggingFace DatasetDict in the `self.main_data_path` directory.

        Args:
            **kwargs (dict): Additional keyword arguments.
        """
        pass

    def get(self, **kwargs) -> None:
        """Downloads and preprocesses a dataset.

        Args:
            **kwargs (dict): Additional keyword arguments.
        """
        self.version_path.mkdir(parents=True, exist_ok=True)
        self._retrieve_files(**kwargs)
        self._preprocess_files(**kwargs)

    def is_retrieved(self) -> bool:
        """Checks if the dataset at the specific version is already downloaded.

        Returns:
            (bool): True if the dataset exists locally, False otherwise.
        """
        return self.main_data_path.exists()

    def remove(self) -> None:
        """Deletes the dataset at the specific version from disk."""
        if self.version_path.exists():
            shutil.rmtree(self.version_path)

    def load(
        self, retrieve: bool = True, cache: bool = True, force_retrieve: bool = False
    ) -> Dataset:
        """Loads the dataset as a HuggingFace dataset.

        If multiple splits are specified, they are concatenated into a single
        dataset. See the `load_dict` method if you wish to load the dataset as a
        `DatasetDict`.

        Args:
            retrieve (bool, optional): Whether to retrieve the dataset if it
                does not exist locally. Defaults to True.
            cache (bool, optional): Whether to cache the dataset in memory.
                Defaults to True.
            force_retrieve (bool, optional): Whether to force retrieving and
                reloading the dataset even if it is already cached. Overrides
                the `retrieve` flag if set to True. Defaults to False.

        Returns:
            (Dataset): The loaded dataset.
        """
        if self.dataset is not None and not force_retrieve:
            return self.dataset

        if (not self.is_retrieved() and retrieve) or force_retrieve:
            self.get()
        elif not self.is_retrieved():
            raise ValueError(
                f"Dataset {self.name} is not available locally and "
                "retrieve is set to False. Either `get` the dataset first or "
                "set the retrieve flag to True."
            )
        hf_dataset = load_from_disk(self.main_data_path)
        if isinstance(hf_dataset, Dataset) and self.splits is not None:
            raise ValueError(
                f"Cannot load specific splits for an unpartitioned dataset {self.name}."
            )
        if isinstance(hf_dataset, DatasetDict):
            if self.splits is not None:
                hf_dataset = concatenate_datasets([hf_dataset[s] for s in self.splits])
            else:
                hf_dataset = concatenate_datasets(list(hf_dataset.values()))
        if cache:
            self.dataset = hf_dataset
        return hf_dataset

    def unload(self) -> None:
        """Unloads the dataset from memory."""
        self.dataset = None

    def load_dict(
        self, retrieve: bool = True, cache: bool = True, force_retrieve: bool = False
    ) -> DatasetDict:
        """Loads the dataset as a HuggingFace dataset dictionary.

        See the `load` method if you wish to concatenate the splits into
        a single dataset.

        Args:
            retrieve (bool, optional): Whether to retrieve the dataset if it
                does not exist locally. Defaults to True.
            cache (bool, optional): Whether to cache the dataset in memory.
                Defaults to True.
            force_retrieve (bool, optional): Whether to force retrieving and
                reloading the dataset even if it is already cached. Overrides
                the `retrieve` flag if set to True. Defaults to False.

        Returns:
            (DatasetDict): The loaded dataset dictionary.
        """
        if self.dataset_dict is not None and not force_retrieve:
            return self.dataset_dict

        if (not self.is_retrieved() and retrieve) or force_retrieve:
            self.get()
        elif not self.is_retrieved():
            raise ValueError(
                f"Dataset {self.name} is not available locally and "
                "retrieve is set to False. Either `get` the dataset first or "
                "set the retrieve flag to True."
            )
        hf_dataset = load_from_disk(self.main_data_path)
        if isinstance(hf_dataset, Dataset):
            raise ValueError(
                f"Cannot load an unpartitioned dataset {self.name} as dict."
            )
        if self.splits is not None:
            hf_dataset = cast(DatasetDict, hf_dataset[self.splits])
        if cache:
            self.dataset_dict = hf_dataset
        return hf_dataset

    def unload_dict(self) -> None:
        """Unloads the dataset dictionary from memory."""
        self.dataset_dict = None

    @classmethod
    @abstractmethod
    def can_handle(cls, name: str) -> bool:
        """Checks if the DatasetManager can handle the given dataset.

        Args:
            name (str): The name of the dataset.

        Returns:
            (bool): True if the manager can handle the dataset, False otherwise.
        """
        pass
