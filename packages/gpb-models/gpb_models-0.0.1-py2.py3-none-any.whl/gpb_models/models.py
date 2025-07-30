import logging
import os
from datetime import date
from itertools import chain
from pathlib import Path
from typing import Generator

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from .types import Chromosome, Strand

logger = logging.getLogger(__name__)


class RegionRecord(BaseModel):
    ref_genome: str
    chromosome: Chromosome
    start: int
    end: int
    name: str
    inheritance: str
    strand: Strand

    model_config = ConfigDict(frozen=True)

    def as_bed(self) -> str:
        return "\t".join(
            map(
                str,
                map(
                    lambda x: "" if x is None else x,
                    [
                        self.chromosome.value,
                        self.start,
                        self.end,
                        self.name,
                        "0.0",
                        self.strand.value,
                    ],
                ),
            )
        )


class TranscriptRecord(BaseModel):
    ref_genome: str
    chromosome: Chromosome
    start: int
    end: int
    name: str
    strand: Strand
    tags: tuple[str, ...]
    hgnc_id: int
    hgnc_symbol: str
    inheritance: str
    coding_start: int | None
    coding_end: int | None
    exon_starts: tuple[int, ...] = Field(default_factory=tuple)
    exon_ends: tuple[int, ...] = Field(default_factory=tuple)
    metadata: str = "{}"

    model_config = ConfigDict(frozen=True)

    @property
    def exons(self) -> Generator[tuple[int, int], None, None]:
        if self.strand == Strand("+"):
            return zip(self.exon_starts, self.exon_ends)
        elif self.strand == Strand("-"):
            return zip(self.exon_starts[::-1], self.exon_ends[::-1])

    @property
    def regions(self) -> Generator[RegionRecord, None, None]:
        for i, (start, end) in enumerate(self.exons):
            if self.coding_start is not None and end < self.coding_start:
                continue
            if self.coding_end is not None and start > self.coding_end:
                continue
            yield RegionRecord(
                ref_genome=self.ref_genome,
                chromosome=self.chromosome,
                start=max(start, self.coding_start or -float("inf")),
                end=min(end, self.coding_end or float("inf")),
                inheritance=self.inheritance,
                name=f"{self.hgnc_symbol}__{self.hgnc_id}__{self.name}__exon{i+1}",
                strand=self.strand,
            )

    def as_tsv(self) -> str:
        f = "\t".join(
            map(
                str,
                map(
                    lambda x: "" if x is None else x,
                    [
                        self.chromosome.value,
                        self.start,
                        self.end,
                        self.name,
                        "0.0",
                        self.strand.value,
                        ",".join(self.tags),
                        self.hgnc_id,
                        self.hgnc_symbol,
                        self.inheritance,
                        self.coding_start,
                        self.coding_end,
                        ",".join(map(str, self.exon_starts)),
                        ",".join(map(str, self.exon_ends)),
                        self.metadata,
                    ],
                ),
            )
        )
        return f


class GeneRecord(BaseModel):
    hgnc_id: int
    hgnc_symbol: str
    inheritance: str
    transcripts: tuple[TranscriptRecord, ...]

    model_config = ConfigDict(frozen=True)


class PhenotypeRecord(BaseModel):
    hgnc_id: int
    hgnc_symbol: str
    inheritance: str | None
    mim_number: int
    phenotype: str
    pmid: int | None
    inheritance_info: str | None
    comment: str | None

    model_config = ConfigDict(frozen=True)


class ExportedGenePanel(BaseModel):
    name: str = Field(..., description="Name of the gene panel")
    shortname: str = Field(..., description="Short name of the gene panel")
    version: str = Field(..., description="Version of the gene panel")
    description: str = Field(..., description="Description of the gene panel")
    exported_date: date = Field(
        default_factory=date.today, description="Date of export"
    )
    regions: tuple[RegionRecord, ...]
    genes: tuple[GeneRecord, ...]
    phenotypes: tuple[PhenotypeRecord, ...]
    _reference_genome: str

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def validate_genome_reference(self):
        genome_references = {
            *{tx.ref_genome for gene in self.genes for tx in gene.transcripts},
            *{region.ref_genome for region in self.regions},
        }
        assert len(genome_references) == 1, (
            "Expected exactly one reference genome across all regions and transcripts, got "
            f"{len(genome_references)}: '{genome_references}'"
        )
        self._reference_genome = genome_references.pop()
        return self

    @computed_field
    @property
    def ref_genome(self) -> str:
        return self._reference_genome

    @computed_field
    @property
    def report_config(self) -> str:
        return (
            "[DEFAULT]\n"
            "# Used in attachment sent to doctor and internal web\n"
            f"  title={self.name}\n"
            f"  version=v{self.version}\n"
            "  coverage_threshold=100\n"
            "  coverage_description=\n"
            "\n"
            "[Web publishing - table]\n"
            "# The values (not the keys) are printed line by line before the gene table.\n"
            "  legend = [\n"
            "        ]\n"
        )

    @property
    def transcript_records(self) -> list[TranscriptRecord]:
        return list({tx for gene in self.genes for tx in gene.transcripts})

    @property
    def all_regions(self) -> list[RegionRecord]:
        return sorted(
            chain(self.regions, *[tx.regions for tx in self.transcript_records]),
            # all_regions,
            key=lambda region: (
                region.chromosome,
                region.start,
                region.end,
                region.name,
            ),
        )

    def genes_transcripts_tsv_contents(self) -> Generator[str, None, None]:
        header = (
            f"# Gene panel: {self.name}-v{self.version} -- Date: {self.exported_date}",
            "\t".join(
                [
                    "#chromosome",
                    "read start",
                    "read end",
                    "name",
                    "score",
                    "strand",
                    "tags",
                    "HGNC id",
                    "HGNC symbol",
                    "inheritance",
                    "coding start",
                    "coding end",
                    "exon starts",
                    "exon ends",
                    "metadata",
                ]
            ),
        )
        yield from header
        regions_as_transcript_records = [
            TranscriptRecord.model_construct(
                exon_ends=(),
                exon_starts=(),
                hgnc_id=-1,
                hgnc_symbol="N/A",
                coding_start=None,
                coding_end=None,
                tags=("Custom region",),
                **region.model_dump(),
            )
            for region in self.regions
        ]
        for tx in sorted(
            chain(self.transcript_records, regions_as_transcript_records),
            key=lambda tx: (tx.chromosome, tx.start, tx.end, tx.name),
        ):
            yield tx.as_tsv()

    def regions_bed_contents(self) -> Generator[str, None, None]:
        header = (
            f"# Gene panel: {self.name}-v{self.version} -- Date: {self.exported_date}",
            "\t".join(
                ["#chromosome", "read start", "read end", "name", "score", "strand"]
            ),
        )
        yield from header
        for region in self.all_regions:
            yield region.as_bed()

    def phenotypes_tsv_contents(self) -> Generator[str, None, None]:
        header = (
            f"# Gene panel: {self.name}-v{self.version} -- Date: {self.exported_date}",
            "\t".join(
                [
                    "HGNC id",
                    "HGNC symbol",
                    "inheritance",
                    "phenotype MIM number",
                    "phenotype",
                    "PMID",
                    "inheritance info",
                    "comment",
                ]
            ),
        )
        yield from header
        for phenotype in sorted(
            self.phenotypes,
            key=lambda p: (
                str(p.hgnc_id),
                p.inheritance or "",
                str(p.mim_number),
                p.phenotype,
            ),
        ):
            yield "\t".join(
                map(
                    str,
                    map(
                        lambda x: "" if x is None else x,
                        [
                            phenotype.hgnc_id,
                            phenotype.hgnc_symbol,
                            phenotype.inheritance,
                            phenotype.mim_number,
                            phenotype.phenotype,
                            phenotype.pmid,
                            "",
                            phenotype.comment,
                        ],
                    ),
                )
            )

    @classmethod
    def from_folder(cls, folder: Path) -> "ExportedGenePanel":
        genes_transcripts = next(folder.glob("*genes_transcripts.tsv"))
        regions = next(folder.glob("*regions.bed"))
        phenotypes = next(folder.glob("*phenotypes.tsv"))

        common_prefix = os.path.commonprefix(
            [genes_transcripts.name, regions.name, phenotypes.name]
        )
        shortname = common_prefix.split("_")[0]
        version = common_prefix.split("_")[1].lstrip("v")

        def _str_to_int_or_none(val: str):
            try:
                return int(val)
            except ValueError as e:
                logger.warning(f"Can't cast '{val}' to integer: {e}")
                return None

        with genes_transcripts.open() as f:
            # Skip the first line
            f.readline()

            # Read the header
            keys = f.readline().rstrip().split("\t")

            gene_records: dict[int, GeneRecord] = {}
            region_records: list[RegionRecord] = []

            for line in f:
                d = dict(zip(keys, line.rstrip().split("\t")))

                if d["HGNC id"] != "":
                    transcript_record = TranscriptRecord(
                        ref_genome="GRCh37",
                        chromosome=Chromosome(d["#chromosome"]),
                        start=int(d["read start"]),
                        end=int(d["read end"]),
                        name=d["name"],
                        strand=Strand(d["strand"]),
                        tags=d["tags"].split(","),
                        hgnc_id=int(d["HGNC id"]),
                        hgnc_symbol=d["HGNC symbol"],
                        inheritance=d["inheritance"],
                        coding_start=_str_to_int_or_none(d["coding start"]),
                        coding_end=_str_to_int_or_none(d["coding end"]),
                        exon_starts=tuple(
                            map(
                                int,
                                d["exon starts"].split(",") if d["exon starts"] else [],
                            )
                        ),
                        exon_ends=tuple(
                            map(
                                int, d["exon ends"].split(",") if d["exon ends"] else []
                            )
                        ),
                        metadata=d["metadata"],
                    )
                    if transcript_record.hgnc_id not in gene_records:
                        gene_records[transcript_record.hgnc_id] = GeneRecord(
                            hgnc_id=transcript_record.hgnc_id,
                            hgnc_symbol=transcript_record.hgnc_symbol,
                            inheritance=transcript_record.inheritance,
                            transcripts=[],
                        )

                    gene_records[transcript_record.hgnc_id] = GeneRecord(
                        **gene_records[transcript_record.hgnc_id].model_dump(
                            exclude={"transcripts"}
                        ),
                        transcripts=list(
                            gene_records[transcript_record.hgnc_id].transcripts
                        )
                        + [transcript_record],
                    )
                else:
                    region_records.append(
                        RegionRecord(
                            ref_genome="GRCh37",
                            chromosome=Chromosome(d["#chromosome"]),
                            start=int(d["read start"]),
                            end=int(d["read end"]),
                            name=d["name"],
                            inheritance=d["inheritance"],
                            strand=Strand(d["strand"]),
                        )
                    )
                    pass

        phenotype_records: list[PhenotypeRecord] = []
        with phenotypes.open() as f:
            # Get name and date from the header
            header = f.readline().split(" -- ")
            name = header[0].split(": ")[1]
            exported_date = header[1].split(": ")[1].rstrip()
            name = name[: name.index(f"-v{version}")]

            keys = f.readline().rstrip().split("\t")

            for line in f:
                d = dict(zip(keys, line.rstrip().split("\t")))
                phenotype_records.append(
                    PhenotypeRecord(
                        hgnc_id=int(d["HGNC id"]),
                        hgnc_symbol=d["HGNC symbol"],
                        inheritance=d["inheritance"],
                        mim_number=int(d["phenotype MIM number"]),
                        phenotype=d["phenotype"],
                        pmid=None,
                        inheritance_info=None,
                        comment=None,
                    )
                )

        return ExportedGenePanel(
            name=name,
            shortname=shortname,
            version=version,
            description="",
            exported_date=exported_date,
            regions=region_records,
            genes=list(gene_records.values()),
            phenotypes=phenotype_records,
        )
