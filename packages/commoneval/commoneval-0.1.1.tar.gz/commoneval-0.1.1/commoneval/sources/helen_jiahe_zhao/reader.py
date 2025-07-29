"""Convert CSV data to match metadata specs.

>>> from commoneval.sources.helen_jiahe_zhao import reader
>>> rd = reader.Reader()


>>> len(rd)
4913
>>> rd["jrAVhksgdnWA"]
<Item('jrAVhksgdnWA', shortprose): 'In the Bible, whe...'->'Egypt'>
>>> from sys import stdout
>>> rd["jrAVhksgdnWA"].write_jsonline(stdout)
{"identifier": "jrAVhksgdnWA", "modality": "shortprose", "prompt": "In the Bible, where was Aaron born?", "response": "Egypt"}
>>>

"""

from collections import UserDict
import csv
from datetime import date
from pathlib import Path
import re
from typing import Optional

from commoneval import DATAENGPATH
from commoneval.dataset import Dataset
from commoneval.item import Item, Modality

BIBLEQA = Path(__file__).parent / "1001-new.csv"
assert BIBLEQA.exists(), f"File not found: {BIBLEQA}"


class Reader(UserDict):
    """Read data from bible_qa.tsv."""

    identifier: str = "hjz_bible_qa"
    dataset: Dataset = Dataset(
        identifier=identifier,
        created=date.fromisoformat("2017-10-29"),
        creator="Helen Jiahe Zhao",
        description="Bible Q&A dataset. See https://arxiv.org/abs/1810.12118 'Finding Answers from the Word of God: Domain Adaptation for Neural Networks in Biblical Question Answering'.",
        hasPart=[f"{identifier}.jsonl"],
        source="The author says 'We used a freely available set of 1001 trivia questions from the Bible as the basis for the dataset.' and references https://biblequizzes.org.uk (which now redirects to https://bibletrivia.co.uk/).",
        subject="Miscellaneous Bible trivia. ",
        contributor="Sean Boisen",
        license="Copyrighted",
        licenseNotes="The previous version of the source webpage (https://web.archive.org/web/20161023225831/http://biblequizzes.org.uk/faq.php#1_1) says 'All quizzes and puzzles on this site are copyrighted, but they may be used freely in printed publications as long as this website (www.biblequizzes.org.uk) is credited alongside each item as the source, and that the quizzes or puzzles are distributed on a non-profit basis. Any other use, including online publication, requires written permission.'. Based on this original statement, this adaptation of the data may be considered under copyright protection.",
        sourceProcess="Reformatted from original CSV file. ",
    )

    def __init__(self, path: Path = BIBLEQA) -> None:
        self.path = path
        with self.path.open("r", encoding="utf-8-sig", newline="") as f:
            self.reader = csv.DictReader(f)
            self.data = {
                mappedrow.identifier: mappedrow
                for row in self.reader
                if (mappedrow := self.map_row(row))
            }

    @staticmethod
    def map_row(row: dict, modality: Modality = Modality.SHORTPROSE) -> Item:
        """Map a row to an Item."""
        question = row["Questions"]
        qmatch = re.match(r"^(?P<identifier>\d+). ?(?P<prompt>.+)", question)
        identifier = qmatch.group("identifier")
        assert qmatch, f"Invalid question format: {question!r}"
        answer = row["ANSWERS"]
        # ansmatch = re.match(
        #     r"^(?P<ansidentifier>\d+). (?P<response>[^()]+) ?(?P<reference>[^)])",
        #     answer,
        # )
        ansmatch = re.match(
            r"^(?P<ansidentifier>\d+). (?P<rest>.+)",
            answer,
        )
        assert ansmatch, f"Invalid answer format: {answer!r}"
        assert identifier == ansmatch.group(
            "ansidentifier"
        ), "Identifier mismatch: {identifier} != {ansmatch.group('ansidentifier')}"
        refpos = ansmatch.group("rest").rindex("(")
        response = ansmatch.group("rest")[: refpos - 1]
        support = ansmatch.group("rest")[refpos + 1 : -1]
        rowitem: Item = Item(
            identifier=identifier,
            modality=modality,
            prompt=qmatch.group("prompt"),
            response=response,
            support=support,
        )
        return rowitem

    def write_dataset(self, basepath: Path = DATAENGPATH) -> None:
        """Write the dataset to a file."""
        datasetdirpath: Path = basepath / f"{self.identifier}"
        datasetdirpath.mkdir(parents=True, exist_ok=True)
        dsyamlpath: Path = datasetdirpath / f"{self.identifier}.yaml"
        with dsyamlpath.open("w") as f:
            self.dataset.write_yaml(f)
        with (datasetdirpath / f"{self.identifier}.jsonl").open("w") as f:
            for item in self.data.values():
                item.write_jsonline(f)
