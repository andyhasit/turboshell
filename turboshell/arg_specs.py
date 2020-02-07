"""
Validators can be used as argument texts.
"""
from .exceptions import CmdArgException, CmdSpecificationException


class BaseArgSpec(object):
    """
    The base class from which other arg specs inherit.
    """
    def __init__(self, name, required, default=None):
        self.name = name
        self.required = required
        self.value = None

    def fulfilled(self):
        """
        Returns false if required and no value extracted.
        """
        if self.required:
            return self.value is not None
        return True


class TextArgSpec(BaseArgSpec):
    """
    The default ArgSpec which strings are converted to.

    String must be of these formats:

        age         # expect a string, allow null
        age!        # expect a string, must be supplied
        int:age     # expect an int, allow null
        int:age!    # expect an int, must be supplied

    So far just int, but will allow bool, float, time measures etc...

    """
    CONVERTERS = {
        'bool': bool,
        'float': float,
        'int': int,
        'str': lambda x: x,
    }

    def __init__(self, text):
        if ':' in text:
            self.type, name = text.split(':')
        else:
            self.type = 'str'
            name = text
        if self.type not in self.CONVERTERS:
            allowed_types = ', '.join(self.CONVERTERS)
            raise CmdSpecificationException(
                '{} is not an allowed type. Use one of: {}'.format(self.type, allowed_types)
            )
        required = name.endswith('!')
        if required:
            name = name[:-1]
        super(TextArgSpec, self).__init__(name, required)

    def validate(self, value):
        convert_fn = self.CONVERTERS[self.type]
        try:
            self.value = convert_fn(value)
        except ValueError:
            raise CmdArgException('Argument {} cannot be converted to {}'.format(self.name, self.type))
