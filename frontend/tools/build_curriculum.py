#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "nctb_curriculum_2026.json"

CLASSES = [
    "Class 6",
    "Class 7",
    "Class 8",
    "Class 9",
    "Class 10",
]

GROUPS = [
    "Science",
    "Commerce",
    "Arts",
]

FOLDER_TO_GRADE = {
    "classsix": "Class 6",
    "classseven": "Class 7",
    "classeight": "Class 8",
    "classnineten": "Class 9-10",
}

SUBJECT_MAP = {
    "Class 6": {
        "agriculture": "কৃষিশিক্ষা",
        "arabic": "সচিত্র আরবি পাঠ",
        "arts_and_crafts": "চারু ও কারুকলা",
        "bangla": "চারুপাঠ",
        "bangla_grammar": "বাংলা ব্যাকরণ ও নির্মিতি",
        "bangla_rapidreader": "আনন্দপাঠ",
        "bgs": "বাংলাদেশ ও বিশ্বপরিচয়",
        "buddhist_religion": "বৌদ্ধধর্ম শিক্ষা",
        "christian_religion": "খ্রীষ্টধর্ম শিক্ষা",
        "english": "English For Today",
        "english_grammar": "English Grammar and Composition",
        "hindu_religion": "হিন্দুধর্ম শিক্ষা",
        "home_science": "গার্হস্থ্যবিজ্ঞান",
        "ict": "তথ্য ও যোগাযোগ প্রযুক্তি",
        "islam": "ইসলাম শিক্ষা",
        "math": "গণিত",
        "music": "সংগীত",
        "pali": "পালি",
        "physical_education": "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "sanskrit": "সংস্কৃত",
        "science": "বিজ্ঞান",
        "work_and_life": "কর্ম ও জীবনমুখী শিক্ষা",
    },
    "Class 7": {
        "agriculture": "কৃষিশিক্ষা",
        "arabic": "সচিত্র আরবি পাঠ",
        "arts_and_crafts": "চারু ও কারুকলা",
        "bangla": "সপ্তবর্ণা",
        "bangla_grammar": "বাংলা ব্যাকরণ ও নির্মিতি",
        "bangla_rapidreader": "আনন্দপাঠ",
        "bgs": "বাংলাদেশ ও বিশ্বপরিচয়",
        "buddhist_religion": "বৌদ্ধধর্ম শিক্ষা",
        "christian_religion": "খ্রীষ্টধর্ম শিক্ষা",
        "english": "English For Today",
        "english_grammar": "English Grammar and Composition",
        "hindu_religion": "হিন্দুধর্ম শিক্ষা",
        "home_science": "গার্হস্থ্যবিজ্ঞান",
        "ict": "তথ্য ও যোগাযোগ প্রযুক্তি",
        "islam": "ইসলাম শিক্ষা",
        "math": "গণিত",
        "music": "সংগীত",
        "pali": "পালি",
        "physical_education": "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "sanskrit": "সংস্কৃত",
        "science": "বিজ্ঞান",
        "work_and_life": "কর্ম ও জীবনমুখী শিক্ষা",
    },
    "Class 8": {
        "agriculture": "কৃষিশিক্ষা",
        "arabic": "সচিত্র আরবি পাঠ",
        "arts_and_crafts": "চারু ও কারুকলা",
        "bangla": "সাহিত্য কণিকা",
        "bangla_grammar": "বাংলা ব্যাকরণ ও নির্মিতি",
        "bangla_rapidreader": "আনন্দপাঠ",
        "bgs": "বাংলাদেশ ও বিশ্বপরিচয়",
        "buddhist_religion": "বৌদ্ধধর্ম শিক্ষা",
        "christian_religion": "খ্রীষ্টধর্ম শিক্ষা",
        "english": "English For Today",
        "english_grammar": "English Grammar and Composition",
        "hindu_religion": "হিন্দুধর্ম শিক্ষা",
        "home_science": "গার্হস্থ্যবিজ্ঞান",
        "ict": "তথ্য ও যোগাযোগ প্রযুক্তি",
        "islam": "ইসলাম শিক্ষা",
        "math": "গণিত",
        "music": "সংগীত",
        "pali": "পালি",
        "physical_education": "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "sanskrit": "সংস্কৃত",
        "science": "বিজ্ঞান",
        "work_and_life": "কর্ম ও জীবনমুখী শিক্ষা",
    },
    "Class 9-10": {
        "accounting": "হিসাববিজ্ঞান",
        "agriculture": "কৃষিশিক্ষা",
        "arabic": "আরবি",
        "arts_and_crafts": "চারু ও কারুকলা",
        "bangla": "বাংলা সাহিত্য",
        "bangla_grammar": "বাংলা ভাষার ব্যাকরণ ও নির্মিতি",
        "bangla_rapidreader": "বাংলা সহপাঠ",
        "bgs": "বাংলাদেশ ও বিশ্বপরিচয়",
        "biology_secondary": "জীববিজ্ঞান",
        "buddhist_religion": "বৌদ্ধধর্ম শিক্ষা",
        "business_entrepreneurship": "ব্যবসায় উদ্যোগ",
        "career_education": "ক্যারিয়ার শিক্ষা",
        "chemistry_secondary": "রসায়ন",
        "christian_religion": "খ্রীষ্টধর্ম শিক্ষা",
        "civics": "পৌরনীতি ও নাগরিকতা",
        "economics": "অর্থনীতি",
        "english": "English For Today",
        "english_grammar": "English Grammar and Composition",
        "finance": "ফিন্যান্স ও ব্যাংকিং",
        "geography": "ভূগোল ও পরিবেশ",
        "higher_math": "উচ্চতর গণিত",
        "hindu_religion": "হিন্দুধর্ম শিক্ষা",
        "history": "বাংলাদেশের ইতিহাস ও বিশ্বসভ্যতা",
        "home_science": "গার্হস্থ্যবিজ্ঞান",
        "ict": "তথ্য ও যোগাযোগ প্রযুক্তি",
        "islam": "ইসলাম শিক্ষা",
        "math": "গণিত",
        "music": "সংগীত",
        "pali": "পালি",
        "physical_education": "শারীরিক শিক্ষা, স্বাস্থ্যবিজ্ঞান ও খেলাধুলা",
        "physics_secondary": "পদার্থবিজ্ঞান",
        "sanskrit": "সংস্কৃত",
        "science": "বিজ্ঞান",
    },
}

SUBJECT_ORDER = {
    "Class 6": [
        "চারুপাঠ",
        "আনন্দপাঠ",
        "বাংলা ব্যাকরণ ও নির্মিতি",
        "English For Today",
        "English Grammar and Composition",
        "গণিত",
        "তথ্য ও যোগাযোগ প্রযুক্তি",
        "বাংলাদেশ ও বিশ্বপরিচয়",
        "বিজ্ঞান",
        "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "কর্ম ও জীবনমুখী শিক্ষা",
        "কৃষিশিক্ষা",
        "গার্হস্থ্যবিজ্ঞান",
        "চারু ও কারুকলা",
        "ইসলাম শিক্ষা",
        "হিন্দুধর্ম শিক্ষা",
        "খ্রীষ্টধর্ম শিক্ষা",
        "বৌদ্ধধর্ম শিক্ষা",
        "সচিত্র আরবি পাঠ",
        "সংস্কৃত",
        "পালি",
        "সংগীত",
    ],
    "Class 7": [
        "সপ্তবর্ণা",
        "আনন্দপাঠ",
        "বাংলা ব্যাকরণ ও নির্মিতি",
        "English For Today",
        "English Grammar and Composition",
        "গণিত",
        "তথ্য ও যোগাযোগ প্রযুক্তি",
        "বাংলাদেশ ও বিশ্বপরিচয়",
        "বিজ্ঞান",
        "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "কর্ম ও জীবনমুখী শিক্ষা",
        "কৃষিশিক্ষা",
        "গার্হস্থ্যবিজ্ঞান",
        "চারু ও কারুকলা",
        "ইসলাম শিক্ষা",
        "হিন্দুধর্ম শিক্ষা",
        "খ্রীষ্টধর্ম শিক্ষা",
        "বৌদ্ধধর্ম শিক্ষা",
        "সচিত্র আরবি পাঠ",
        "সংস্কৃত",
        "পালি",
        "সংগীত",
    ],
    "Class 8": [
        "সাহিত্য কণিকা",
        "আনন্দপাঠ",
        "বাংলা ব্যাকরণ ও নির্মিতি",
        "English For Today",
        "English Grammar and Composition",
        "গণিত",
        "তথ্য ও যোগাযোগ প্রযুক্তি",
        "বাংলাদেশ ও বিশ্বপরিচয়",
        "বিজ্ঞান",
        "শারীরিক শিক্ষা ও স্বাস্থ্য",
        "কর্ম ও জীবনমুখী শিক্ষা",
        "কৃষিশিক্ষা",
        "গার্হস্থ্যবিজ্ঞান",
        "চারু ও কারুকলা",
        "ইসলাম শিক্ষা",
        "হিন্দুধর্ম শিক্ষা",
        "খ্রীষ্টধর্ম শিক্ষা",
        "বৌদ্ধধর্ম শিক্ষা",
        "সচিত্র আরবি পাঠ",
        "সংস্কৃত",
        "পালি",
        "সংগীত",
    ],
}

SSC_COMMON = [
    "বাংলা সাহিত্য",
    "বাংলা সহপাঠ",
    "বাংলা ভাষার ব্যাকরণ ও নির্মিতি",
    "English For Today",
    "English Grammar and Composition",
    "গণিত",
    "তথ্য ও যোগাযোগ প্রযুক্তি",
    "ইসলাম শিক্ষা",
    "হিন্দুধর্ম শিক্ষা",
    "বৌদ্ধধর্ম শিক্ষা",
    "খ্রীষ্টধর্ম শিক্ষা",
    "ক্যারিয়ার শিক্ষা",
    "চারু ও কারুকলা",
    "শারীরিক শিক্ষা, স্বাস্থ্যবিজ্ঞান ও খেলাধুলা",
    "কৃষিশিক্ষা",
    "গার্হস্থ্যবিজ্ঞান",
    "আরবি",
    "সংস্কৃত",
    "পালি",
    "সংগীত",
]

SSC_GROUP_ONLY = {
    "Science": [
        "পদার্থবিজ্ঞান",
        "রসায়ন",
        "জীববিজ্ঞান",
        "উচ্চতর গণিত",
        "বাংলাদেশ ও বিশ্বপরিচয়",
    ],
    "Commerce": [
        "বিজ্ঞান",
        "হিসাববিজ্ঞান",
        "ফিন্যান্স ও ব্যাংকিং",
        "ব্যবসায় উদ্যোগ",
    ],
    "Arts": [
        "বিজ্ঞান",
        "ভূগোল ও পরিবেশ",
        "অর্থনীতি",
        "পৌরনীতি ও নাগরিকতা",
        "বাংলাদেশের ইতিহাস ও বিশ্বসভ্যতা",
    ],
}

EXPECTED_CONFIG_COUNTS = {
    "Class 6": 22,
    "Class 7": 22,
    "Class 8": 22,
    "Class 9-10": 33,
}

SCIENCE_EXPECTED_CHAPTERS = {
    "পদার্থবিজ্ঞান": 12,
    "রসায়ন": 12,
    "জীববিজ্ঞান": 14,
    "উচ্চতর গণিত": 14,
}

CONFIG_PATTERN = re.compile(
    r"/(classSix|classSeven|classEight|classNineTen)/chapters_config_(.+)\.json$",
    flags=re.IGNORECASE,
)


def resolve_project_root() -> Path:
    script_path = Path(__file__).resolve()

    if script_path.parent.name.lower() == "tools":
        return script_path.parent.parent

    return script_path.parent


def read_json(
    archive: zipfile.ZipFile,
    member_name: str,
) -> Any:
    raw = archive.read(member_name)

    return json.loads(
        raw.decode("utf-8-sig")
    )


def parse_chapters(
    data: Any,
    member_name: str,
) -> List[Dict[str, str]]:
    if not isinstance(data, list):
        raise RuntimeError(
            f"Config is not a JSON list: {member_name}"
        )

    chapters: List[Dict[str, str]] = []

    seen_numbers = set()

    for position, item in enumerate(
        data,
        start=1,
    ):
        if not isinstance(item, dict):
            raise RuntimeError(
                f"Invalid chapter record at position {position}: {member_name}"
            )

        raw_number = item.get(
            "chapter_no"
        )

        raw_title = item.get(
            "chapter_title"
        )

        if raw_number is None:
            raise RuntimeError(
                f"Missing chapter_no at position {position}: {member_name}"
            )

        try:
            chapter_number = int(
                str(raw_number).strip()
            )

        except ValueError as exc:
            raise RuntimeError(
                f"Invalid chapter_no {raw_number!r}: {member_name}"
            ) from exc

        chapter_title = str(
            raw_title or ""
        ).strip()

        if not chapter_title:
            raise RuntimeError(
                f"Missing chapter_title for chapter {chapter_number}: {member_name}"
            )

        if chapter_number in seen_numbers:
            raise RuntimeError(
                f"Duplicate chapter number {chapter_number}: {member_name}"
            )

        seen_numbers.add(
            chapter_number
        )

        chapters.append(
            {
                "number": str(
                    chapter_number
                ),
                "title": chapter_title,
            }
        )

    chapters.sort(
        key=lambda row: int(
            row["number"]
        )
    )

    if chapters:
        numbers = [
            int(row["number"])
            for row in chapters
        ]

        expected_numbers = list(
            range(
                1,
                numbers[-1] + 1,
            )
        )

        if numbers != expected_numbers:
            missing = sorted(
                set(expected_numbers)
                - set(numbers)
            )

            raise RuntimeError(
                f"Chapter number gap in {member_name}. Missing: {missing}"
            )

    return chapters


def ordered_subject_map(
    grade: str,
    chapters_by_subject: Dict[
        str,
        List[Dict[str, str]],
    ],
) -> Dict[
    str,
    List[Dict[str, str]],
]:
    output = OrderedDict()

    if grade in SUBJECT_ORDER:
        for subject in SUBJECT_ORDER[
            grade
        ]:
            if subject in chapters_by_subject:
                output[
                    subject
                ] = chapters_by_subject[
                    subject
                ]

    else:
        for slug, subject in SUBJECT_MAP[
            grade
        ].items():
            if (
                subject in chapters_by_subject
                and subject not in output
            ):
                output[
                    subject
                ] = chapters_by_subject[
                    subject
                ]

    for subject, chapters in chapters_by_subject.items():
        if subject not in output:
            output[
                subject
            ] = chapters

    return dict(
        output
    )


def build_curriculum(
    zip_path: Path,
) -> Dict[str, Any]:
    raw_chapters = {
        "Class 6": {},
        "Class 7": {},
        "Class 8": {},
        "Class 9-10": {},
    }

    config_counts = {
        grade: 0
        for grade in raw_chapters
    }

    chapter_counts = {
        grade: 0
        for grade in raw_chapters
    }

    unmapped = []

    with zipfile.ZipFile(
        zip_path,
        "r",
    ) as archive:
        members = [
            name
            for name in archive.namelist()
            if not name.endswith("/")
        ]

        config_members = []

        for name in members:
            normalized = name.replace(
                "\\",
                "/",
            )

            if CONFIG_PATTERN.search(
                normalized
            ):
                config_members.append(
                    name
                )

        print(
            f"Archive files: {len(members)}"
        )

        print(
            f"Chapter config files found: {len(config_members)}"
        )

        if not config_members:
            raise RuntimeError(
                "No Class 6 to Class 10 chapter config files were found in the archive."
            )

        for member_name in sorted(
            config_members
        ):
            normalized = member_name.replace(
                "\\",
                "/",
            )

            match = CONFIG_PATTERN.search(
                normalized
            )

            if match is None:
                continue

            folder_key = match.group(
                1
            ).casefold()

            subject_slug = match.group(
                2
            ).strip().lower()

            grade = FOLDER_TO_GRADE.get(
                folder_key
            )

            if grade is None:
                continue

            subject = SUBJECT_MAP.get(
                grade,
                {},
            ).get(
                subject_slug
            )

            if subject is None:
                unmapped.append(
                    f"{grade}: {subject_slug}"
                )

                continue

            if subject in raw_chapters[
                grade
            ]:
                raise RuntimeError(
                    f"Duplicate subject mapping for {grade}: {subject}"
                )

            config_data = read_json(
                archive,
                member_name,
            )

            chapters = parse_chapters(
                config_data,
                member_name,
            )

            raw_chapters[
                grade
            ][
                subject
            ] = chapters

            config_counts[
                grade
            ] += 1

            chapter_counts[
                grade
            ] += len(
                chapters
            )

    if unmapped:
        raise RuntimeError(
            "Unmapped chapter config subjects:\n  "
            + "\n  ".join(
                unmapped
            )
        )

    for grade, expected_count in EXPECTED_CONFIG_COUNTS.items():
        actual_count = config_counts[
            grade
        ]

        if actual_count != expected_count:
            raise RuntimeError(
                f"{grade} expected {expected_count} subject configs, found {actual_count}."
            )

    chapters_output = {
        grade: ordered_subject_map(
            grade,
            raw_chapters[
                grade
            ],
        )
        for grade in raw_chapters
    }

    for subject, expected_count in SCIENCE_EXPECTED_CHAPTERS.items():
        actual_count = len(
            chapters_output[
                "Class 9-10"
            ].get(
                subject,
                [],
            )
        )

        if actual_count != expected_count:
            raise RuntimeError(
                f"{subject} expected {expected_count} chapters, found {actual_count}."
            )

    subjects_by_class = {
        grade: list(
            chapters_output[
                grade
            ].keys()
        )
        for grade in [
            "Class 6",
            "Class 7",
            "Class 8",
        ]
    }

    ssc_available = set(
        chapters_output[
            "Class 9-10"
        ].keys()
    )

    ssc_subjects_by_group = {}

    for group in GROUPS:
        requested = list(
            OrderedDict.fromkeys(
                SSC_COMMON
                + SSC_GROUP_ONLY[
                    group
                ]
            )
        )

        ssc_subjects_by_group[
            group
        ] = [
            subject
            for subject in requested
            if subject in ssc_available
        ]

    return {
        "year": 2026,

        "classes": CLASSES,

        "groupsByClass": {
            "Class 9": GROUPS,
            "Class 10": GROUPS,
        },

        "subjectsByClass":
            subjects_by_class,

        "sscSubjectsByGroup":
            ssc_subjects_by_group,

        "chapters":
            chapters_output,

        "validation": {
            "subjectConfigCounts":
                config_counts,

            "chapterCounts":
                chapter_counts,

            "scienceChapterCounts": {
                subject: len(
                    chapters_output[
                        "Class 9-10"
                    ][
                        subject
                    ]
                )
                for subject in SCIENCE_EXPECTED_CHAPTERS
            },
        },
    }


def print_summary(
    data: Dict[str, Any],
) -> None:
    print()

    print(
        "Curriculum summary"
    )

    for grade in [
        "Class 6",
        "Class 7",
        "Class 8",
        "Class 9-10",
    ]:
        subject_map = data[
            "chapters"
        ][
            grade
        ]

        total_chapters = sum(
            len(items)
            for items in subject_map.values()
        )

        print(
            f"{grade}: {len(subject_map)} subjects, {total_chapters} chapters"
        )

    print()

    print(
        "SSC Science chapter check"
    )

    for subject in [
        "পদার্থবিজ্ঞান",
        "রসায়ন",
        "জীববিজ্ঞান",
        "উচ্চতর গণিত",
    ]:
        chapters = data[
            "chapters"
        ][
            "Class 9-10"
        ][
            subject
        ]

        print(
            f"{subject}: {len(chapters)} chapters"
        )

    print()

    print(
        "Biology chapters"
    )

    for chapter in data[
        "chapters"
    ][
        "Class 9-10"
    ][
        "জীববিজ্ঞান"
    ]:
        print(
            f"{chapter['number']}. {chapter['title']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build NCTB 2026 curriculum metadata from chapter config JSON files."
        )
    )

    parser.add_argument(
        "--zip",
        dest="zip_path",
        required=True,
        type=Path,
        help=(
            "Path to the downloaded NCTB SchoolText ZIP file."
        ),
    )

    parser.add_argument(
        "--output",
        dest="output_path",
        type=Path,
        default=None,
        help=(
            "Optional output JSON path."
        ),
    )

    args = parser.parse_args()

    zip_path = (
        args
        .zip_path
        .expanduser()
        .resolve()
    )

    project_root = resolve_project_root()

    if args.output_path is not None:
        output_path = (
            args
            .output_path
            .expanduser()
            .resolve()
        )

    else:
        output_path = (
            project_root
            / "data"
            / "nctb_curriculum_2026.json"
        )

    if not zip_path.exists():
        raise RuntimeError(
            f"ZIP file not found: {zip_path}"
        )

    if not zipfile.is_zipfile(
        zip_path
    ):
        raise RuntimeError(
            f"Not a valid ZIP file: {zip_path}"
        )

    print(
        f"Reading: {zip_path}"
    )

    data = build_curriculum(
        zip_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print_summary(
        data
    )

    print()

    print(
        f"Written: {output_path}"
    )

    print(
        "Done."
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(
            main()
        )

    except Exception as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        raise SystemExit(
            1
        )