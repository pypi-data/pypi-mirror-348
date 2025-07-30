"""
Module: natasha_stopwords_remover

This module defines the `NatashaStopwordsRemover` class, which implements
stopword removal and text processing using the Natasha NLP library.

Classes
-------
NatashaStopwordsRemover:
    Handles removal of stopwords, swear words, and specific user-defined words from a given text input.
"""

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)

from ..domain import IStopwordsRemover


class NatashaStopwordsRemover(IStopwordsRemover):
    """
    Implements stopword removal and text processing using Natasha tools.

    This class provides methods to remove stopwords, optional swear words,
    and custom user-defined words from text inputs. It uses the Natasha NLP
    library components such as MorphTagger and Segmenter for preprocessing.

    Note: This class is specific to the russian language.

    Methods
    -------
        add_words_to_stopwords(words):
            Add words to stopwords list.
        add_words_to_swear_words(words):
            Add words to swear words list.
        remove_stopwords(text, remove_swear_words=True, go_few_times=False):
            Remove parasite words from text.
        remove_words(text, removing_words):
            Remove given words from text.

    Example usage:
    --------------
    text_remover = NatashaStopwordsRemover()

    text_remover.add_words_to_stopwords({"ай", "эй"})
    text_without_stopwords = text_remover.remove_stopwords(
        text, remove_swear_words=True, go_few_times=False
        )

    """

    def __init__(self):
        self.__stopwords = {
            'типа', 'короче', 'ну', 'э', 'вообще', 'вообще-то', 'похоже',
            'походу', 'вот', 'блин', 'эм', 'так'
        }
        self.__swear_words = {
            'бля', 'блять', 'пиздец', 'ахуеть',
        }
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._emb = NewsEmbedding()
        self._morph_tagger = NewsMorphTagger(self._emb)
        self._syntax_parser = NewsSyntaxParser(self._emb)

    def add_words_to_stopwords(self, words: list | tuple | set):
        """
        Add words to stopwords list.

        Parameters
        ----------
        words : list or tuple or set
            Words to add to stopwords list.
        """

        self.__stopwords.update(words)

    def add_words_to_swear_words(self, words: list | tuple | set):
        """
        Add words to swear words list.

        Parameters
        ----------
        words : list or tuple or set
            Words to add to swear words list.
        """

        self.__swear_words.update(words)

    def remove_stopwords(
            self,
            text: str,
            remove_swear_words: bool = True,
            go_few_times: bool = False
    ) -> str:
        """
        Removes stopwords and optionally swear words from the given text.

        Basic removing words:
        'типа', 'короче', 'ну', 'э', 'вообще', 'вообще-то', 'похоже',
        'походу', 'вот', 'блин', 'эм', 'так'

        Basic swear words:
        'бля', 'блять', 'пиздец', 'ахуеть'

        Words removed from text by the context.
        If go_few_times and some stopwords weren't removed, try remove them
        one more time. If text haven't changed, it's a final result. This
        flag can delete important words. Be careful.
        Removing of swear words can work incorrect.

        Parameters
        ----------
        text : str
            Input text to clean.
        remove_swear_words : bool, optional
            Whether to remove swear words along with stopwords.
        go_few_times : (bool, optional)
            Whether to remove stopwords one more time if text have changed.

        Returns
        -------
        str
            The cleaned text after removing stopwords and optionally swear words.
        """

        paragraphs = text.split('\n')
        new_paragraphs = []
        restart_flag = True

        while restart_flag:
            restart_flag = False

            for paragraph in paragraphs:
                doc = Doc(paragraph)
                doc.segment(self._segmenter)
                doc.tag_morph(self._morph_tagger)
                doc.parse_syntax(self._syntax_parser)

                new_text = []

                for token in doc.tokens:
                    if not self._is_stopword(doc.tokens, token, remove_swear_words):
                        new_text.append(token)
                    elif go_few_times:
                        restart_flag = True

                new_paragraphs.append(self._restore_text(new_text))

        return '\n'.join(new_paragraphs)[1:] if new_paragraphs else ''

    def remove_words(
            self,
            text: str,
            removing_words: tuple | list
    ) -> str:
        """
        Removes specific words from the given text.

        Parameters
        ----------
        text : str
            Input text to clean.
        removing_words : list of str
            List of words to remove from the text.

        Returns
        -------
        str
            Cleaned text with specified words removed.
        """

        removing_words = set(map(lambda s: s.lower().strip(), removing_words))
        paragraphs = text.split('\n')
        new_paragraphs = []

        for paragraph in paragraphs:
            doc = Doc(paragraph)
            doc.segment(self._segmenter)
            doc.parse_syntax(self._syntax_parser)

            new_text = []

            for token in doc.tokens:
                if token.text.lower() not in removing_words:
                    new_text.append(token)

            new_paragraphs.append(self._restore_text(new_text))

        return '\n'.join(new_paragraphs)[1:] if new_paragraphs else ''

    def _is_stopword(
            self,
            all_tokens,
            target_token,
            remove_swear_words: bool
    ) -> bool:
        """
        Check if given token is stopword.

        If token not in stopwords list return False.
        If token does not contain dependent tokens return True.
        If all token dependent tokens are 'discourse', 'punct', 'ccomp' return True.

        Parameters
        ----------
        all_tokens:
            Token list of paragraph.
        target_token:
            Target token.
        remove_swear_words:
            True to remove swear words.

        Returns
        -------
        bool
            True if token is stopword else False.
        """

        lower_text = target_token.text.lower()
        if (
            remove_swear_words
            and lower_text not in self.__stopwords
            and lower_text not in self.__swear_words
        ):
            return False
        elif not remove_swear_words and lower_text not in self.__stopwords:
            return False

        dependents = [token for token in all_tokens
                      if token.head_id == target_token.id]
        for token in dependents:
            if token.rel not in ['discourse', 'punct', 'ccomp']:
                return False
        return True

    @staticmethod
    def _restore_text(token_list: list) -> str:
        """
        Restore text from token_list.

        Delete spaces before punctuators. Delete extra punctuators.

        Parameters
        ----------
        token_list: list
            Token list of paragraph.

        Returns
        -------
        str
            The restored text.
        """
        restored_text = ''

        for i, token in enumerate(token_list):
            if token.rel == 'punct':
                if i != 0 and token_list[i - 1].rel != 'punct':
                    restored_text += token.text
            else:
                restored_text += ' ' + token.text

        return restored_text
