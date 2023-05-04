import re

VALIDATE_PATTERN = re.compile(r"/(?P<field_name>\w+)/{(?P=field_name)}")


class StringFormatter:

    def __init__(self, base_string='', sep='/'):
        self._string = base_string
        self._sep = sep
        self._params = VALIDATE_PATTERN.findall(self._string)

    @classmethod
    def from_base(cls, string):
        return cls(base_string=string)

    @property
    def string(self):
        return self._string

    @property
    def params(self):
        return self._params

    def append(self, string_to_append):
        new_string = self._string + self._sep + string_to_append
        return StringFormatter(new_string)

    def put_params(self, **kwargs):
        if self._are_params_present(kwargs.keys()):
            return self._string.format(**kwargs)
        else:
            raise ValueError(f"Keys provided {list(kwargs.keys())} are different from expected {self.params}")

    def _are_params_present(self, keys):
        return set(self.params) == set(keys)

