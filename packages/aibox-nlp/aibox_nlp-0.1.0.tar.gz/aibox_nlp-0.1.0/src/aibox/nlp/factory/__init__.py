"""Arquivo de inicialização."""

from .class_registry import (
    available_datasets,
    available_extractors,
    available_metrics,
    available_vectorizers,
)
from .dataset import get_dataset
from .feature_extractor import get_extractor
from .metric import get_metric
from .pipeline import get_pipeline, make_pipeline
from .vectorizer import get_vectorizer
