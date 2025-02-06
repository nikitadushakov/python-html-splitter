import typing as tp
from . import splitter


def split_html(html_stream: tp.Iterable[str], message_size: int) -> tp.Generator[None, None, str]:
    parser = splitter.HTMLSplitter(message_size)
    for row in html_stream:
        parser.feed(row)
        while parser.export_ready:
            yield parser.export_ready.popleft()
   
    if (last_fragment := parser.message_fragment):
        yield last_fragment
