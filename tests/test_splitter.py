import pytest
import msg_split
import tests.expected


@pytest.mark.parametrize("max_len", ["4296", "4396"])
@pytest.mark.parametrize("file_path", ["./source.html"])
def test_splitter(max_len: int, file_path: str):
    print(max_len, file_path)
    fragments = msg_split.split_html_file(max_len=int(max_len), file_path=file_path)
    assert list(fragments) == tests.expected.expected_results[max_len]

