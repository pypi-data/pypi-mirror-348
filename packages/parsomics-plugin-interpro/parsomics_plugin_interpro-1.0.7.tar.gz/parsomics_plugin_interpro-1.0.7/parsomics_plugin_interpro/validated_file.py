from pathlib import Path
from typing import ClassVar

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome


class InterproTsvValidatedFile(ValidatedFileWithGenome):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        "_interpro_out.tsv",
        "_interpro.tsv",
    ]

    @property
    def genome_name(self) -> str:
        file_name: str = Path(self.path).name
        for termination in self._VALID_FILE_TERMINATIONS:
            file_name = file_name.removesuffix(termination)
        return file_name
