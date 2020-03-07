from .mixin import class_mixin
from . import cvss3, cvss2


def make_display_name(str):
    return " ".join(s.capitalize() for s in str.lower().split("_"))


class CVSS2State(class_mixin(cvss2)):
    pass


class CVSS3State(class_mixin(cvss3)):
    pass


class CVSS31State(class_mixin(cvss31)):
    pass


from .vector import parse_vector, calculate_vector
