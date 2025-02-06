import dataclasses

from . import config

@dataclasses.dataclass(slots=True)
class HTMLTag:
    name: str
    attrs: list[tuple[str, str]]
    content: str = ''

    @property
    def start_tag(self) -> str:
        return f"<{self.name}{''.join(f' {name}="{value}"' for name, value in self.attrs)}>"

    @property
    def end_tag(self) -> str:
        return f"</{self.name}>"

    def __len__(self) -> int:
        return len(self.start_tag + self.content + self.end_tag)

    def __str__(self) -> str:
        return f"{self.start_tag}{self.content}{self.end_tag}"

    @property
    def can_be_splitted(self):
        return self.name in config.BLOCK_TAGS
