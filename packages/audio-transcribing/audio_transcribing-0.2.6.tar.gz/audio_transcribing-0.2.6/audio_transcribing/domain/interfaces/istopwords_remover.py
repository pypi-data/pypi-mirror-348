"""
Module: istopwords_remover

This module defines the interface for removing stopwords and unwanted words from text.

Classes
-------
IStopwordsRemover:
    Abstract interface for removing stopwords from text.
"""

from abc import ABC, abstractmethod


class IStopwordsRemover(ABC):
    """
    Interface for removing unwanted words, including stopwords, from text.

    This interface defines the contract for any stopwords removal mechanism.
    Any class implementing this interface must provide methods to remove stopwords
    or other specified words from the given text.

    Methods
    -------
    remove_stopwords(text, remove_swear_words):
        Removes stopwords and optionally swear words from the text.
    remove_words(text, removing_words):
        Removes specific user-defined words from text.
    """

    @abstractmethod
    def remove_stopwords(
            self,
            text: str,
            remove_swear_words: bool = True
    ) -> str:
        """
        Removes stopwords and optionally swear words from the given text.

        Parameters
        ----------
        text : str
            The input text from which stopwords will be removed.
        remove_swear_words : bool
            Whether to also remove swear words from the text.

        Returns
        -------
        str
            The cleaned text with stopwords removed.
        """
        pass

    @abstractmethod
    def remove_words(
            self,
            text: str,
            removing_words: tuple | list
    ) -> str:
        """
        Removes specific words from the text.

        Parameters
        ----------
        text : str
            The input text to process.
        removing_words : tuple or list
            A list or tuple of words to remove from the text.

        Returns
        -------
        str
            The cleaned text with the specified words removed.
        """
        pass
