from os import sep
from pathlib import Path
from random import randint
from typing import Dict, List

from wowool.document import Document

corpus_root = Path(__file__).parent.resolve() / "corpus"
_description: Dict[str, List[str]] = {}


def _get_directories(fp: Path):
    return (fp for fp in fp.glob("*") if fp.is_dir())


class Corpus(list):
    @staticmethod
    def describe() -> dict[str, List[str]]:
        global _description
        if not _description:
            _description = {
                language: [fp.name for fp in _get_directories(corpus_root / language)]
                for language in map(lambda fn: fn.name, _get_directories(corpus_root))
            }
        return _description

    def __init__(self, id: str = "", language: str = "", name: str = ""):
        if id:
            self.id = id if id.endswith(sep) else f"{id}{sep}"
        else:
            assert language, "'language' required when not using id"
            self.id = f"{language}{sep}"
            if name:
                self.id += f"{name}{sep}"
        documents = [fn for fn in Document.glob(self.path, "**/*.txt")]
        super(Corpus, self).__init__(documents)

    @property
    def language(self) -> str:
        return self.id.split(sep)[0]

    @property
    def name(self) -> str:
        name = self.id.replace(f"{self.language}{sep}", "")
        return name[:-1] if name.endswith(sep) else ""

    @property
    def path(self) -> Path:
        return corpus_root / self.language / self.name

    def random(self, count: int) -> List[Document]:
        """
        Return a random set of the corpus
        """
        N = len(self) - 1
        return [self[randint(0, N)] for n in range(0, N) if n < count]
