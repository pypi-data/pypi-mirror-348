from dataclasses import dataclass
from typing import Union

from ML_management.dataset_loader import DatasetLoaderPattern
from ML_management.executor import BaseExecutor
from ML_management.mlmanagement.model_type import ModelType
from ML_management.model import Model


@dataclass
class ObjectMetaInfo:
    name: str
    version: int
    hash_artifacts: str
    model_type: ModelType


@dataclass
class LoadedObject:
    local_path: str
    loaded_class: Union[BaseExecutor, DatasetLoaderPattern, Model]
    metainfo: ObjectMetaInfo
