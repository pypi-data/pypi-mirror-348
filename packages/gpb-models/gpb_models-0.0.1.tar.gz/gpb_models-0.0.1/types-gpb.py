from enum import Enum

Chromosome = Enum(
    "Chromosome",
    {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "10": "10",
        "11": "11",
        "12": "12",
        "13": "13",
        "14": "14",
        "15": "15",
        "16": "16",
        "17": "17",
        "18": "18",
        "19": "19",
        "20": "20",
        "21": "21",
        "22": "22",
        "X": "X",
        "Y": "Y",
        "XY": "XY",
        "MT": "MT",
    },
)


def __lt__(self, other):
    return int(self) < int(other)


def __int__(self):
    try:
        return int(self.value)
    except ValueError:
        if self.value == "X":
            return 23
        if self.value == "Y":
            return 24
        if self.value == "XY":
            return 25
        if self.value == "MT":
            return 26


Chromosome.__int__ = __int__
Chromosome.__lt__ = __lt__  # type: ignore


Strand = Enum("Strand", {"+": "+", "-": "-"})


class ReferenceGenome(Enum):
    GRCh37 = "GRCh37"
    GRCh38 = "GRCh38"
