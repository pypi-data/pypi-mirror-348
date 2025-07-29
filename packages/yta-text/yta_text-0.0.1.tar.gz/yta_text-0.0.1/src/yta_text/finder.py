from yta_text.dataclasses import TermFound
from yta_text.handler import TextHandler
from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_constants.text import TextFinderOption
from typing import Union


class TextFinder:
    """
    Class to wrap the functionality related to
    looking for terms in a text.
    """

    @staticmethod
    def find_in_text(
        term: str,
        text: str,
        options: Union[TextFinderOption, list[TextFinderOption]] = []
    ) -> list[TermFound]:
        """
        Find the provided 'term' in the also provided
        'text' and obtain the start and end indexes
        of the 'term' according to that 'text'. The 
        term can be more than once in the 'text'.

        TODO: Add an ilustrative example.

        This method returns an array containing
        TermFound instances including the start and
        end indexes.
        """
        ParameterValidator.validate_mandatory_string('term', term, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)

        # Force 'options' to be an array
        options = (
            [options]
            if not PythonValidator.is_list(options) else
            options
        )
        ParameterValidator.validate_mandatory_list_of_these_instances('options', options, [TextFinderOption, str])
        
        for option in options:
            option = TextFinderOption.to_enum(option)
        
        # Apply the options
        if TextFinderOption.IGNORE_ACCENTS in options:
            term = TextHandler.remove_marks_and_accents(term)
            text = TextHandler.remove_marks_and_accents(text)
        if TextFinderOption.IGNORE_CASE in options:
            term = term.lower()
            text = text.lower()

        # TODO: Please, review and rethink this part:
        # We need to be careful with the periods,
        # question marks, exclamation marks... because
        # 'texto.' will not be detected if looking for
        # 'texto' due to the period '.'
        text = TextHandler.remove_marks_and_accents(text)
        term = TextHandler.remove_marks_and_accents(term)

        text_words = text.split()
        term_words = term.split()
        
        # Store first and last index if found
        return [
            TermFound(
                term = term,
                start_index = i,
                end_index = i + len(term_words) - 1
            )
            for i in range(len(text_words) - len(term_words) + 1)
            if text_words[i:i + len(term_words)] == term_words
        ]