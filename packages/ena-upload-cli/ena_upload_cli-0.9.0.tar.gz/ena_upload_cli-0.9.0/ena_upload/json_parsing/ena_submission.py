from typing import List, Dict

from pandas import DataFrame
from ena_upload.json_parsing.characteristic import IsaBase
from ena_upload.json_parsing.ena_experiment import (
    EnaExperiment,
    export_experiments_to_dataframe,
)
from ena_upload.json_parsing.ena_run import EnaRun, export_runs_to_dataframe
from ena_upload.json_parsing.ena_sample import EnaSample, export_samples_to_dataframe
from ena_upload.json_parsing.ena_std_lib import (
    fetch_assay_streams,
    fetch_study_comment_by_name,
    study_publication_ids,
)

from ena_upload.json_parsing.ena_study import EnaStudy, export_studies_to_dataframe


def fetch_assay(assay, required_assays):
    for ra in required_assays:
        for key, value in ra.items():
            for assay_comment in assay["comments"]:
                if assay_comment["name"] == key and assay_comment["value"] == value:
                    return assay


def filter_assays(
    isa_json: Dict[str, str], required_assays: List[Dict[str, str]]
) -> Dict[str, str]:
    new_studies = []
    new_isa_json = isa_json
    studies = new_isa_json.pop("studies")
    for study in studies:
        assays = study.pop("assays")
        filtered_assays = [
            fetch_assay(assay, required_assays)
            for assay in assays
            if fetch_assay(assay, required_assays) is not None
        ]
        if len(filtered_assays) > 0:
            study["assays"] = filtered_assays
            new_studies.append(study)
    new_isa_json["studies"] = new_studies
    return new_isa_json


def validate_isa_json(isa_json: Dict[str, str]):
    IsaBase.validate_json(isa_json, EnaSubmission.investigation_schema)


class EnaSubmission(IsaBase):
    """
    Wrapper objects, holding studies
    """

    investigation_schema = "investigation_schema.json"

    def __init__(
        self,
        studies: List[EnaStudy] = [],
        samples: List[EnaSample] = [],
        experiments: List[EnaExperiment] = [],
        runs: List[EnaRun] = [],
    ) -> None:
        super().__init__()
        self.studies = studies
        self.samples = samples
        self.experiments = experiments
        self.runs = runs

    def to_dict(self) -> Dict:
        return {
            "study": [study.to_dict() for study in self.studies],
            "sample": [sample.to_dict() for sample in self.samples],
            "experiment": [experiment.to_dict() for experiment in self.experiments],
            "run": [run.to_dict() for run in self.runs],
        }


    def from_isa_json(
        isa_json: Dict[str, str], required_assays: List[Dict[str, str]]
    ) -> None:
        """Generates an EnaSubmission from a ISA JSON dictionary.

        Args:
            isa_json (Dict[str, str]): ISA JSON dictionary

        Returns:
            EnaSubmission: resulting EnaSubmission
        """
        validate_isa_json(isa_json)

        filtered_isa_json: Dict[str, str] = filter_assays(isa_json, required_assays)
        samples = []
        studies = []
        experiments = []
        runs = []
        
        assay_stream_names = [a_stream['assay_stream'] for a_stream in required_assays]
        
        if filtered_isa_json["studies"] == []:
            raise ValueError(f"No studies found with isa_assay_stream {assay_stream_names}")
        
        for study in filtered_isa_json["studies"]:
            [samples.append(sample) for sample in EnaSample.from_study_dict(study)]

            pubmed_ids = study_publication_ids(
                publication_isa_json=study["publications"]
            )
            current_study_protocols_dict = study["protocols"]
            assay_streams = fetch_assay_streams(study)
            ena_sample_alias_prefix = fetch_study_comment_by_name(
                study, EnaSample.prefix
            )["value"]
            for assay_stream in assay_streams:
                study = EnaStudy.from_assay_stream(assay_stream, pubmed_ids)
                studies.append(study)

                [
                    experiments.append(experiment)
                    for experiment in EnaExperiment.from_assay_stream(
                        assay_stream,
                        study.alias,
                        ena_sample_alias_prefix,
                        current_study_protocols_dict,
                    )
                ]

                [runs.append(run) for run in EnaRun.from_assay_stream(assay_stream)]

        ena_submission = EnaSubmission(
            studies=studies, samples=samples, experiments=experiments, runs=runs
        )
        ena_submission.sanitize_samples()
        return ena_submission

    def sanitize_samples(self):
        unused_samples = []

        for sample in self.samples:
            experiment_sample_aliases = [
                experiment.sample_alias for experiment in self.experiments
            ]
            if sample.alias not in experiment_sample_aliases:
                unused_samples.append(sample.alias)

        self.samples = [
            sample for sample in self.samples if sample.alias not in unused_samples
        ]

    def generate_dataframes(self) -> Dict[str, DataFrame]:
        """Generates all necessary DataFrames for the ENA Upload tool
        and returns them in a dictionary.

        Returns:
            Dict[str, DataFrame]: resulting dictionary of DataFrames
        """
        return {
            "study": export_studies_to_dataframe(self.studies).fillna(""),
            "sample": export_samples_to_dataframe(self.samples).fillna(""),
            "experiment": export_experiments_to_dataframe(self.experiments).fillna(""),
            "run": export_runs_to_dataframe(self.runs).fillna(""),
        }
