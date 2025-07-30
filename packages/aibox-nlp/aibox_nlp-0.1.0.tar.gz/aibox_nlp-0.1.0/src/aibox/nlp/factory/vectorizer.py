"""Módulo para obtenção de vetorizadores
através de um nome.
"""

from aibox.nlp.core import Vectorizer

from .class_registry import get_class


def get_vectorizer(vectorizer: str, **config) -> Vectorizer:
    """Obtém um vetorizador dado um nome.

    Args:
        vectorizer (str): nome do vetorizador.
        config: configurações desse vetorizador.

    Returns:
        Vectorizer: vetorizador.
    """
    vectorizer = get_class(vectorizer)
    assert issubclass(
        vectorizer, Vectorizer
    ), "Esse nome não corresponde à um vetorizador."
    return vectorizer(**config)
