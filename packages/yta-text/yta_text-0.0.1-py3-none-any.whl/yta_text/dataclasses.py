from yta_validation.parameter import ParameterValidator
from dataclasses import dataclass


@dataclass
class TermFound:
    """
    @dataclass
    A term found in a text, containing the indexes
    in which the term was found.
    """

    def __init__(
        self,
        term: str,
        start_index: int,
        end_index: int
    ) -> 'TermFound':
        ParameterValidator.validate_mandatory_string('term', term, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_int('start_index', start_index, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_int('end_index', end_index, do_include_zero = True)

        self.term: str = term
        """
        The term that has been found.
        """
        self.start_index: int = start_index
        """
        The index (within the text) in which the start
        of the 'term' has been found.
        """
        self.end_index: int = end_index
        """
        The index (within the text) in which the end
        of the 'term' has been found.
        """