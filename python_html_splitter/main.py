from collections import deque
import dataclasses
from typing import Callable
from typing import Deque

from html.parser import HTMLParser

max_len = 30


class CouldNotSplitMessage(Exception): ...


def send_html_tag(fn: Callable):
    def wrapper(self, tag, attrs):
        html_tag = HTMLTag(name=tag, attrs=attrs)
        return fn(self, html_tag)
    return wrapper


@dataclasses.dataclass(slots=True)
class HTMLTag:
    name: str
    attrs: list[tuple[str, str]]
    content: str = ''

    def __len__(self) -> int:
        return len(self.start_tag + self.content + self.end_tag)

    @property
    def start_tag(self) -> str:
        return f"<{self.name}{''.join(f' {name}="{value}"' for name, value in self.attrs)}>"

    @property
    def end_tag(self) -> str:
        return f"</{self.name}>"

    def __str__(self) -> str:
        return f"{self.start_tag}{self.content}{self.end_tag}"


class MyHTMLParser(HTMLParser):
    def __init__(self, max_length: int):
        super().__init__()
        self.max_length: int = max_length
        self.message_offset: int = max_length
        self.tags_stack: list[HTMLTag] = list()  # unclosed tags
        self.export_ready_id: int | None = None
        self.export_ready: Deque[str] = deque()

    def maybe_split_message(self, len_of_new_content: int) -> None:
        if (self.message_offset - len_of_new_content) < 0:
            try:
                self.cut()
            except AssertionError:
                raise CouldNotSplitMessage(f'Невозможно сформировать сообщение размером не более {self.max_length} символов')
                
        self.message_offset -= len_of_new_content

    @send_html_tag
    def handle_starttag(self, tag: HTMLTag):
        self.tags_stack.append(tag)
        self.maybe_split_message(len(tag))

    def add_content_to_last_tag(self, content: str) -> None:
        self.tags_stack[-1].content += content
        self.export_ready_id = len(self.tags_stack) - 1

    def handle_endtag(self, tag):
        self.ends_tag = self.tags_stack.pop()
        if not self.tags_stack:
            self.export_ready.append(str(self.ends_tag))
            return
        self.add_content_to_last_tag(str(self.ends_tag))

    def handle_data(self, data):
        self.maybe_split_message(len(data))
        self.add_content_to_last_tag(data)

    def cut(self):
        assert self.export_ready_id is not None

        export_ready_tag = self.tags_stack[self.export_ready_id]
        yielded_message = export_ready_tag.content

        for tag in self.tags_stack[self.export_ready_id::-1]:
            yielded_message = f"{tag.start_tag}{yielded_message}{tag.end_tag}"

        self.export_ready.append(yielded_message)
        self.message_offset += len(export_ready_tag.content)
        export_ready_tag.content = ''
        self.export_ready_id = None


def html_generate_messages():
    ...

parser = MyHTMLParser(max_length=len('<div><ul><li>a2</li></ul></div>'))
parser.feed('<div><ul><li>a1</li><li>a2</li><br></br></ul></div>')
