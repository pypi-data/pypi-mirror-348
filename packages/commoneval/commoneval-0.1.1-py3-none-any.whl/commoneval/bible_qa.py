"""Convert Mike's Bible Q&A TSV to match metadata specs.

>>> from commoneval import bible_qa
>>> rd = bible_qa.Reader()
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
import random


from commoneval import DATAENGPATH
from commoneval.dataset import Dataset
from commoneval.item import Item, Modality

BIBLEQA = Path(__file__).parent.parent.parent / "bible-qa/bible_qa.tsv"
assert BIBLEQA.exists(), f"File not found: {BIBLEQA}"


class Reader(UserDict):
    """Read data from bible_qa.tsv."""

    identifier: str = "bible_qa"
    dataset: Dataset = Dataset(
        identifier=identifier,
        created=date.today(),
        creator="Biblica",
        description="Bible Q&A dataset",
        hasPart=[f"{identifier}.jsonl"],
        source="ACAI: people, groups, and places in the Bible",
        subject="Facts about biblical people and groups",
        contributor="Mike Brinker",
        sourceProcess="Generated from ACAI data by bible_qa/acai_templates.py. ",
    )

    def __init__(self, path: Path = BIBLEQA) -> None:
        self.path = path
        # fieldnames = ["id", "subject", "problem", "answer", "wrong_answers"]
        with self.path.open("r") as f:
            self.reader = csv.DictReader(f, delimiter="\t")
            self.data = {row["id"]: self.map_row(row) for row in self.reader}

    @staticmethod
    def map_row(row: dict, modality: Modality = Modality.SHORTPROSE) -> Item:
        """Map a row to an Item."""
        rowitem: Item = Item(
            identifier=row["id"],
            modality=modality,
            prompt=row["problem"],
            response=row["answer"],
        )
        rowitem._otherargs["subject"] = row["subject"]
        rowitem._otherargs["wrong_answers"] = row["wrong_answers"]
        return rowitem

    def write_dataset(self, basepath: Path = DATAENGPATH) -> None:
        """Write the dataset to a file."""
        datasetdirpath: Path = basepath / f"{self.identifier}"
        datasetdirpath.mkdir(parents=True, exist_ok=True)
        dsyamlpath: Path = datasetdirpath / f"{self.identifier}.yaml"
        # dataset = Dataset(
        #     identifier=identifier,
        #     created=date.today(),
        #     creator="Biblica",
        #     description="Bible Q&A dataset",
        #     hasPart=[f"{identifier}.jsonl"],
        #     source="ACAI: people, groups, and places in the Bible",
        #     subject="Facts about biblical people and groups",
        #     contributor="Mike Brinker",
        #     sourceProcess="Generated from ACAI data by bible_qa/acai_templates.py. ",
        # )
        with dsyamlpath.open("w") as f:
            self.dataset.write_yaml(f)
        with (datasetdirpath / f"{self.identifier}.jsonl").open("w") as f:
            for item in self.data.values():
                item.write_jsonline(f)

    # if item._otherargs["subject"] == "fact.death_place":
    def _death_place_bool(self, item: Item) -> Item:
        """Return a revised Item for an item that prompts about a death place."""
        modality = Modality.BOOLEAN
        wherepos: int = item.prompt.index("where did ")
        phraselen: int = len("where did ")
        prompthead: str = f"Answer only true or false: {item.prompt[:wherepos]}"
        # Randomly select a wrong answer from the list of wrong answers if True
        if random.choice([True, False]):
            answer = random.choice(item._otherargs["wrong_answers"].split("|"))
            # Revise the prompt with the wrong answer and create a
            # new boolean Item whose answer is False
            prompttail: str = f"{item.prompt[wherepos+phraselen:-1]}d at {answer}."
            new_item = Item(
                identifier=item.identifier + "_bool",
                modality=modality,
                prompt=prompthead + prompttail,
                response=False,
            )
        else:
            answer = item.response
            prompttail: str = f"{item.prompt[wherepos+phraselen:-1]}d at {answer}."
            new_item = Item(
                identifier=item.identifier + "_bool",
                modality=modality,
                prompt=prompthead + prompttail,
                response=True,
            )
        return new_item

    def write_death_place_bool_dataset(
        self, basepath: Path = DATAENGPATH, identifier: str = "bible_qa-death-bool"
    ) -> Dataset:
        """Write the dataset to a file."""
        datasetdirpath: Path = basepath / f"{identifier}"
        datasetdirpath.mkdir(parents=True, exist_ok=True)
        dsyamlpath: Path = datasetdirpath / f"{identifier}.yaml"
        dataset = Dataset(
            identifier=identifier,
            created=date.today(),
            creator="Biblica",
            description="Bible Q&A dataset, subset for death place converted to boolean",
            hasPart=[f"{identifier}.jsonl"],
            source="ACAI: people, groups, and places in the Bible",
            subject="Facts about biblical people and where they died",
            contributor="Mike Brinker, Sean Boisen",
            sourceProcess="Subset of bible_qa dataset for fact.death_place, converted to boolean with some wrong answers.",
        )
        with dsyamlpath.open("w") as f:
            dataset.write_yaml(f)
        with (datasetdirpath / f"{identifier}.jsonl").open("w") as f:
            for item in self.data.values():
                if item._otherargs["subject"] == "fact.death_place":
                    newitem = self._death_place_bool(item)
                    newitem.write_jsonline(f)
        return dataset
