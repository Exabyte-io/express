import re
import __builtin__


class BaseTXTParser(object):
    """
    Base text parser class.

    Args:
        work_dir (str): path to the working directory.
    """

    def __init__(self, work_dir):
        self.work_dir = work_dir

    def _general_output_parser(self, text, regex, output_type, start_flag=None, occurrences=0, match_groups=[]):
        """
        General function for extracting data from a text output. It extracts basic values using regex patterns. Based
        on the input regex pattern, this function uses re.findall method to find every instance of the pattern inside
        the text.

        Args:
            text (str): text to search
            regex (str): regex pattern.
            output_type (str): output type.
            start_flag (str): a symbol in the output file to be used as the starting point (for speedup and accuracy).
            occurrences (int): number of desired line counts to be processed. If negative, last occurrences is extracted:
                                - N < 0: extract the last N instance(s). Forms a list if |N| > 1
                                - N = 0: extract all of of the occurred instances and forms a list.
                                - N > 0: extract the first N instance(s). Forms a list if |N| > 1
            match_groups (list): list of match groups to be used for the regex.

        Return:
            any
        """
        start_index = text.rfind(start_flag) if start_flag else 0
        pattern = re.compile(regex, re.I | re.MULTILINE)
        cast = getattr(__builtin__, output_type)
        # output type depends on the number of values required. List or single number.
        result = [] if len(match_groups) > 1 or abs(occurrences) > 1 or occurrences == 0 else None

        match = pattern.findall(text[start_index:])
        if match:
            occurrences = len(match) if occurrences == 0 else occurrences
            match = match[occurrences:] if occurrences < 0 else match[:occurrences]
            if isinstance(result, list):
                for m in match:
                    result.append([cast(m[i - 1]) for i in match_groups]) if match_groups else result.append(cast(m))
            else:
                result = cast(match[0][0]) if isinstance(match[0], tuple) else cast(match[0])
        return result
