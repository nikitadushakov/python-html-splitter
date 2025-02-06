import typing as tp
import collections
import html.parser

from . import models
from . import utils

class HTMLSplitter(html.parser.HTMLParser):
    def __init__(self, max_length: int):
        super().__init__()
        self.max_length: int = max_length
        self.message_offset: int = max_length
        self.tags_stack: list[models.HTMLTag] = list()  # unclosed tags
        self.export_ready: tp.Deque = collections.deque()
        self._message_fragment: str = ''

    def maybe_split_message(self, len_of_new_content: int) -> None:
        if (self.message_offset - len_of_new_content) < 0:
            try:
                self.cut()
            except AssertionError:
                if self.tags_stack:
                    self.tags_stack.pop()
                raise utils.CouldNotSplitMessage(f'Невозможно сформировать сообщение размером не более {self.max_length} символов')
                
        self.message_offset -= len_of_new_content

    @utils.send_html_tag
    def handle_starttag(self, tag: models.HTMLTag):
        self.maybe_split_message(len(tag))
        self.tags_stack.append(tag)
        

    def add_content_to_last_tag(self, content: str) -> None:
        if self.tags_stack: 
            self.tags_stack[-1].content += content
        else:
            self._message_fragment += content

    def handle_endtag(self, tag: str) -> None:
        self.ends_tag = self.tags_stack.pop()        
        self.add_content_to_last_tag(str(self.ends_tag))

    def handle_data(self, data: str) -> None:
        self.maybe_split_message(len(data))
        self.add_content_to_last_tag(data)

    def can_we_split_here(self) -> bool:
        return bool(self._message_fragment) or (
            self.tags_stack 
            and self.tags_stack[-1].content 
            and all(tag.can_be_splitted for tag in self.tags_stack)
        )

    @property
    def message_fragment(self) -> str:
        export_tag_content = ''
        if self.tags_stack:
            export_tag_content = self.tags_stack[-1].content
            for tag in self.tags_stack[::-1]:
                export_tag_content = tag.start_tag + export_tag_content + tag.end_tag
        return self._message_fragment + export_tag_content

    def cut(self) -> None:
        assert self.can_we_split_here()
        yielded_message = self.message_fragment
        self.export_ready.append(yielded_message)
        self.message_offset += (len(self._message_fragment))
       
        if self.tags_stack:
            self.message_offset += len(self.tags_stack[-1].content)
            for tag in self.tags_stack: 
                tag.content = ''
        self._message_fragment = ''
