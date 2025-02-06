from typing import Callable

from . import models


class CouldNotSplitMessage(Exception): ...


def send_html_tag(fn: Callable):
    def wrapper(self, tag, attrs):
        html_tag = models.HTMLTag(name=tag, attrs=attrs)
        return fn(self, html_tag)
    return wrapper
