"""Módulo para obtenção de métricas
através de um nome.
"""

from aibox.nlp.core import Metric

from .class_registry import get_class


def get_metric(metric: str, **config) -> Metric:
    """Obtém uma métrica dado o nome.

    Args:
        metric (str): nome da métrica.
        config: configurações dessa métrica.

    Returns:
        Metric: métrica.
    """
    metric = get_class(metric)
    assert issubclass(metric, Metric), "Esse nome não corresponde à uma métrica."
    return metric(**config)
