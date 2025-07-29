from yta_text.utils.spanish_numbers import unit_to_string, ten_to_string, hundred_to_string
from yta_text.dataclasses import TermFound
from yta_validation.parameter import ParameterValidator
from yta_constants.text import TextFinderOption
from typing import Union

import unicodedata
import re


class TextHandler:
    """
    Class to encapsulate all the functionality related
    to manipulating texts: finding strings in texts,
    modifying the texts, etc.
    """

    @staticmethod
    def remove_accents(
        text: str
    ) -> str:
        """
        Get the provided 'text' with the accents removed.
        This means turning 'hóla qué pàsa' to 'hola que
        pasa'.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)

        return ''.join(
            char
            for char in unicodedata.normalize('NFD', text)
            if unicodedata.category(char) != 'Mn'
        )
    
    @staticmethod
    def remove_marks(
        text: str
    ) -> str:
        """
        Get the provided 'text' without any quotation mark, parenthesis,
        full stops, commas, etc.
        
        Marks that are being removed:
        - '?', '¿', ',', '.', '¡', '!', '(', ')'

        # The normal slash below must be a backslash but it is
        # giving a warning
        TODO: This below could work eliminating no white spaces.
        pattern = re.compile('[/W_]+')
        return pattern.sub('', s)
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        # TODO: Try with a 're' implementation maybe (?)
        MARKS_TO_REMOVE = ['?', '¿', ',', '.', '¡', '!', '(', ')']

        for mark in MARKS_TO_REMOVE:
            text = text.replace(mark, '')

        return text
    
    @staticmethod
    def remove_marks_and_accents(
        text: str
    ) -> str:
        """
        Get the provided 'text' without accents and marks.
        """
        ParameterValidator.validate_mandatory_string('text', text)
        
        return TextHandler.remove_accents(TextHandler.remove_marks(text))
    
    @staticmethod
    def remove_non_ascii_characters(
        text: str,
        do_remove_accents: bool = True
    ) -> str:
        """
        Removes any non-ascii character from the provided
        'text' and returns it modified.

        Example of non-ascii characters:
        é, à, ö, ñ, ©, ®, €, £, µ, ¥, 漢, こんにち
        """
        ParameterValidator.validate_mandatory_string('text', text)
        
        s = (
            list(TextHandler.remove_accents(text))
            if do_remove_accents else
            list(text)
        )

        index = 0
        while index < len(s):
            char = s[index]
            if not char.isascii():
                del s[index]
            else:
                index += 1

        return ''.join(s)

    @staticmethod
    def fix_ellipsis(
        text: str
    ) -> str:
        """
        This method fixes the provided 'text' by removing the
        existing ellipsis (...) that is the sequence of three
        or more dots. This will remove '...' but also '.....'.
        """
        ParameterValidator.validate_mandatory_string('text', text)
        
        text = re.sub(r'\.\.\.+', '', text)

        return text
    
    @staticmethod
    def fix_unseparated_periods(
        text: str
    ) -> str:
        """
        This method fixes the provided 'text' by applying
        a space after any period without it. This will 
        turn 'Esto es así.¿Vale?' to 'Esto es así. ¿Vale?'.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        return re.sub(r'(?<!\.)\.(?!\.|\d)(?! )', '. ', text)
    
    @staticmethod
    def fix_separated_parenthesis(
        text: str
    ) -> str:
        """
        This method remove the spaces that are found before or/and
        after any parenthesis. For example, '( esto es de prueba )'
        will become '(esto es de prueba)'.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        def fix_match(match):
            opening, content, closure = match.groups()
            if content:
                # Remove the whitespaces
                without_whitespaces = re.sub(r'\s+', ' ', content.strip())
                return f'{opening}{without_whitespaces}{closure}'
            
            return match.group(0)
        
        return re.sub(r'(\()([^\(\)]+?)(\))', fix_match, text)
        
    @staticmethod
    def fix_separated_square_brackets(
        text: str
    ) -> str:
        """
        This method removes the spaces that are found before or/and
        after any square bracket. For example, '[  shortcode ]' will
        become '[shortcode]'
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        def fix_match(match):
            opening, content, closure = match.groups()
            if content:
                # Remove the whitespaces
                without_whitespaces = re.sub(r'\s+', ' ', content.strip())
                return f'{opening}{without_whitespaces}{closure}'
            
            return match.group(0)
        
        return re.sub(r'(\[)([^\[\]]+?)(\])', fix_match, text)
    
    @staticmethod
    def add_missing_spaces_before_and_after_parenthesis(
        text: str
    ) -> str:
        """
        This method adds the missing spaces before and after any 
        parenthesis in the provided 'text'. For example, 'hola(nueve)siete'
        will become 'hola (nueve) siete'.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        text = re.sub(r'(?<!\s)\((?!\s)', ' (', text)

        return re.sub(r'\)(?!\s)', ') ', text)
    
    @staticmethod
    def add_missing_spaces_before_and_after_square_brackets(
        text: str
    ) -> str:
        """
        This method adds the missing spaces before and after any 
        square bracket in the provided 'text'. For example, 
        'hola[nueve]siete' will become 'hola [nueve] siete'.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        text = re.sub(r'(?<!\s)\[(?!\s)', ' [', text)

        return re.sub(r'\](?!\s)', '] ', text)
    
    @staticmethod
    def fix_excesive_blank_spaces(
        text: str
    ) -> str:
        """
        Checks the provided 'text' and removes the extra blank spaces.
        This means that any sentence with more than one blank space 
        will be replaced by only one blank space.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        # TODO: Is this better (?)
        return re.sub(r'\s+', ' ', text)
        
        # TODO: Ok, why am I using not the 'repl' param in re.search?
        # I'm applying it in the new method below, please check if
        # valid to avoid the while, thank you
        filtered = re.search('[ ]{2,}', text)
        while filtered:
            index_to_replace = filtered.end() - 1
            s = list(text)
            s[index_to_replace] = ''
            text = ''.join(s)
            filtered = re.search('[ ]{2,}', text)

        return text
    
    @staticmethod
    def strip(
        text: str
    ) -> str:
        """
        An enhanced version of the python's '.strip()' method
        that only allows one blank space, removing any 
        consecutive blank spaces group (even in the middle of
        a sentence). Of course, this method will remove any
        blank space at the begining or at the end of the 
        provided 'text' as the original '.strip()' method would
        do.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        return TextHandler.fix_excesive_blank_spaces(text).strip()
    
    # TODO: This method below has been created to ensure
    # the number is received correctly (isolated) because
    # the '_numbers_to_text' method is not detecting the
    # number well always (for example when 9.123.456).
    @staticmethod
    def number_to_text(
        number: Union[int, float]
    ) -> str:
        ParameterValidator.validate_mandatory_number('number', number)

        return TextHandler._numbers_to_text(str(number))

    # TODO: Maybe move this to another class that is more
    # specific about numbers to strings
    # TODO: Refactor this method to make it work correctly
    @staticmethod
    def _numbers_to_text(
        text: str
    ) -> str:
        """
        This method receives a text that could contain numbers
        and turns those numbers into text, which is useful to
        let narration software work with just text and avoid
        numbers problems.

        This method gives the result in Spanish language.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        
        words = str(text).split(' ')
        # TODO: What about the '0' by itself? should be 'cero'
        # but not when '240' 'doscientos cuarenta y zero'

        SPECIAL_CHARS = ['¡', '!', ',', '.', '¿', '?', ':', '"', '\'', '#', '@']
        new_words = []
        # Iterate over each word to turn numbers into words
        for word in words:
            begining = ''
            ending = ''

            # We need to remove special chars at the begining or at the ending
            # to be able to work well with the important part of the word, but
            # we cannot simply delete ',' or '.' because could be in the middle
            # of a word
            if word[0] in SPECIAL_CHARS:
                begining = word[0]
                word = word[1:]
            if word[len(word) - 1] in SPECIAL_CHARS:
                ending = word[len(word) - 1]
                word = word[:1]

            try:
                word = float(word)
                # If here, it is a number, lets change its name
                # TODO: Implement logic here, so word will be the text, not the number
                #print('Processing number: ' + str(word))
                accumulated_text = ''
                # We receive 123.456.789
                is_million = False
                is_one = False
                is_thousand = False
                is_ten = False
                divisor = 1_000_000_000
                res = int(word / divisor)  # 1 . 000 . 000 . 000
                if res >= 1:
                    is_million = True
                    is_thousand = True
                    accumulated_text += unit_to_string(res)
                    word -= divisor * res

                if is_thousand:
                    accumulated_text += ' mil'
                    is_thousand = False

                divisor = 100_000_000
                res = int(word / divisor)  # 100 . 000 . 000
                if res >= 1:
                    is_million = True
                    if res == 1:
                        is_one = True
                    accumulated_text += hundred_to_string(res)
                    word -= divisor * res

                divisor = 10_000_000
                res = int(word / divisor) # 10 . 000 . 000
                if res >= 1:
                    is_million = True
                    is_ten = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one = False
                    accumulated_text += ten_to_string(res)
                    word -= divisor * res

                divisor = 1_000_000
                res = int(word / divisor) # 1 . 000 . 000
                if res >= 1:
                    is_million = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one: False
                    if is_ten:
                        accumulated_text += ' y '
                        is_ten = False
                    accumulated_text += unit_to_string(res)
                    word -= divisor * res

                if is_million:
                    accumulated_text += ' millones'
                    is_million = False

                divisor = 100_000
                res = int(word / divisor) # 100 . 000
                if res >= 1:
                    is_thousand = True
                    if res == 1:
                        is_one = True
                    accumulated_text += hundred_to_string(res)
                    word -= divisor * res

                divisor = 10_000
                res = int(word / divisor) # 10 . 000
                if res >= 1:
                    is_thousand = True
                    is_ten = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one = False
                    accumulated_text += ten_to_string(res)
                    word -= divisor * res

                divisor = 1_000
                res = int(word / divisor) # 1 . 000
                if res >= 1:
                    is_thousand = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one = False
                    if is_ten:
                        accumulated_text += ' y '
                        is_ten = False
                    accumulated_text += unit_to_string(res)
                    word -= divisor * res

                if is_thousand:
                    accumulated_text += ' mil'
                    is_thousand = False

                divisor = 100
                res = int(word / divisor) # 100
                if res >= 1:
                    is_thousand = True
                    if res == 1:
                        is_one = True
                    accumulated_text += hundred_to_string(res)
                    word -= divisor * res

                divisor = 10
                res = int(word / divisor) # 10
                if res >= 1:
                    is_thousand = True
                    is_ten = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one = False
                    accumulated_text += ten_to_string(res)
                    word -= divisor * res

                divisor = 1
                res = int(word / divisor) # 1
                if res >= 1:
                    is_thousand = True
                    if is_one:
                        accumulated_text += 'to'
                        is_one = False
                    if is_ten:
                        accumulated_text += ' y '
                        is_ten = False
                    accumulated_text += unit_to_string(res)
                    word -= divisor * res

                accumulated_text = accumulated_text.replace('  ', ' ').strip()
                # We need to replace in special cases
                accumulated_text = accumulated_text.replace('veinte y nueve', 'veintinueve')
                accumulated_text = accumulated_text.replace('veinte y ocho', 'veintiocho')
                accumulated_text = accumulated_text.replace('veinte y siete', 'veintisiete')
                accumulated_text = accumulated_text.replace('veinte y seis', 'veintiséis')
                accumulated_text = accumulated_text.replace('veinte y cinco', 'veinticinco')
                accumulated_text = accumulated_text.replace('veinte y cuatro', 'veinticuatro')
                accumulated_text = accumulated_text.replace('veinte y tres', 'veintitrés')
                accumulated_text = accumulated_text.replace('veinte y dos', 'veintidós')
                accumulated_text = accumulated_text.replace('veinte y uno', 'veintiuno')
                accumulated_text = accumulated_text.replace('diez y nueve', 'diecinueve')
                accumulated_text = accumulated_text.replace('diez y ocho', 'dieciocho')
                accumulated_text = accumulated_text.replace('diez y siete', 'diecisiete')
                accumulated_text = accumulated_text.replace('diez y seis', 'dieciséis')
                accumulated_text = accumulated_text.replace('diez y cinco', 'quince')
                accumulated_text = accumulated_text.replace('diez y cuatro', 'catorce')
                accumulated_text = accumulated_text.replace('diez y tres', 'trece')
                accumulated_text = accumulated_text.replace('diez y dos', 'doce')
                accumulated_text = accumulated_text.replace('diez y uno', 'once')

                word = accumulated_text
            except:
                pass

            new_words.append(begining + str(word) + ending)

        # We have the same size in 'words' and 'new_words', so lets build it
        final_text = " ".join(new_words)
        
        return final_text