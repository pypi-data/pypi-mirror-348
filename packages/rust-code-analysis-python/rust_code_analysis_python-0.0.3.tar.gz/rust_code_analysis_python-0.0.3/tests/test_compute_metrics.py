import pytest
from copy import deepcopy

from rust_code_analysis_python import compute_metrics

# example extracted from rust-code-analysis-web
example = (
    "test.py",
    "# -*- Mode: Objective-C++; tab-width: 2; indent-tabs-mode: nil;"
    " c-basic-offset: 2 -*-\n\ndef foo():\n    pass\n",
    {
        "kind": "unit",
        "start_line": 1,
        "end_line": 4,
        "metrics": {
            "cyclomatic": {"sum": 2.0, "average": 1.0, "min": 1.0, "max": 1.0},
            "cognitive": {"sum": 0.0, "average": 0.0, "min": 0.0, "max": 0.0},
            "nargs": {
                "total_functions": 0.0,
                "average_functions": 0.0,
                "total_closures": 0.0,
                "average_closures": 0.0,
                "total": 0.0,
                "average": 0.0,
                "closures_max": 0.0,
                "closures_min": 0.0,
                "functions_max": 0.0,
                "functions_min": 0.0,
            },
            "nexits": {"sum": 0.0, "average": 0.0, "min": 0.0, "max": 0.0},
            "halstead": {
                "bugs": 0.000_942_552_557_372_941_4,
                "difficulty": 1.0,
                "effort": 4.754_887_502_163_468,
                "length": 3.0,
                "estimated_program_length": 2.0,
                "purity_ratio": 0.666_666_666_666_666_6,
                "level": 1.0,
                "N2": 1.0,
                "N1": 2.0,
                "vocabulary": 3.0,
                "time": 0.264_160_416_786_859_36,
                "n2": 1.0,
                "n1": 2.0,
                "volume": 4.754_887_502_163_468,
            },
            "loc": {
                "cloc": 1.0,
                "ploc": 2.0,
                "lloc": 1.0,
                "sloc": 4.0,
                "blank": 1.0,
                "cloc_average": 0.5,
                "ploc_average": 1.0,
                "lloc_average": 0.5,
                "sloc_average": 2.0,
                "blank_average": 0.5,
                "cloc_min": 0.0,
                "ploc_min": 2.0,
                "lloc_min": 1.0,
                "sloc_min": 2.0,
                "blank_min": 0.0,
                "cloc_max": 0.0,
                "ploc_max": 2.0,
                "lloc_max": 1.0,
                "sloc_max": 2.0,
                "blank_max": 0.0,
            },
            "nom": {
                "functions": 1.0,
                "closures": 0.0,
                "functions_average": 0.5,
                "closures_average": 0.0,
                "total": 1.0,
                "average": 0.5,
                "closures_min": 0.0,
                "closures_max": 0.0,
                "functions_min": 0.0,
                "functions_max": 1.0,
            },
            "mi": {
                "mi_original": 139.974_331_558_152_1,
                "mi_sei": 161.414_455_240_662_22,
                "mi_visual_studio": 81.856_334_244_533_39,
            },
            "abc": {
                "assignments": 0.0,
                "branches": 0.0,
                "conditions": 0.0,
                "magnitude": 0.0,
                "assignments_average": 0.0,
                "branches_average": 0.0,
                "conditions_average": 0.0,
                "assignments_min": 0.0,
                "assignments_max": 0.0,
                "branches_min": 0.0,
                "branches_max": 0.0,
                "conditions_min": 0.0,
                "conditions_max": 0.0,
            },
        },
        "name": "test.py",
        "spaces": [
            {
                "kind": "function",
                "start_line": 3,
                "end_line": 4,
                "metrics": {
                    "cyclomatic": {"sum": 1.0, "average": 1.0, "min": 1.0, "max": 1.0},
                    "cognitive": {"sum": 0.0, "average": 0.0, "min": 0.0, "max": 0.0},
                    "nargs": {
                        "total_functions": 0.0,
                        "average_functions": 0.0,
                        "total_closures": 0.0,
                        "average_closures": 0.0,
                        "total": 0.0,
                        "average": 0.0,
                        "closures_max": 0.0,
                        "closures_min": 0.0,
                        "functions_max": 0.0,
                        "functions_min": 0.0,
                    },
                    "nexits": {"sum": 0.0, "average": 0.0, "min": 0.0, "max": 0.0},
                    "halstead": {
                        "bugs": 0.000_942_552_557_372_941_4,
                        "difficulty": 1.0,
                        "effort": 4.754_887_502_163_468,
                        "length": 3.0,
                        "estimated_program_length": 2.0,
                        "purity_ratio": 0.666_666_666_666_666_6,
                        "level": 1.0,
                        "N2": 1.0,
                        "N1": 2.0,
                        "vocabulary": 3.0,
                        "time": 0.264_160_416_786_859_36,
                        "n2": 1.0,
                        "n1": 2.0,
                        "volume": 4.754_887_502_163_468,
                    },
                    "loc": {
                        "cloc": 0.0,
                        "ploc": 2.0,
                        "lloc": 1.0,
                        "sloc": 2.0,
                        "blank": 0.0,
                        "cloc_average": 0.0,
                        "ploc_average": 2.0,
                        "lloc_average": 1.0,
                        "sloc_average": 2.0,
                        "blank_average": 0.0,
                        "cloc_min": 0.0,
                        "ploc_min": 2.0,
                        "lloc_min": 1.0,
                        "sloc_min": 2.0,
                        "blank_min": 0.0,
                        "cloc_max": 0.0,
                        "ploc_max": 2.0,
                        "lloc_max": 1.0,
                        "sloc_max": 2.0,
                        "blank_max": 0.0,
                    },
                    "nom": {
                        "functions": 1.0,
                        "closures": 0.0,
                        "functions_average": 1.0,
                        "closures_average": 0.0,
                        "total": 1.0,
                        "average": 1.0,
                        "closures_min": 0.0,
                        "closures_max": 0.0,
                        "functions_min": 1.0,
                        "functions_max": 1.0,
                    },
                    "mi": {
                        "mi_original": 151.433_315_883_223_23,
                        "mi_sei": 142.873_061_717_489_78,
                        "mi_visual_studio": 88.557_494_668_551_6,
                    },
                    "abc": {
                        "assignments": 0.0,
                        "branches": 0.0,
                        "conditions": 0.0,
                        "magnitude": 0.0,
                        "assignments_average": 0.0,
                        "branches_average": 0.0,
                        "conditions_average": 0.0,
                        "assignments_min": 0.0,
                        "assignments_max": 0.0,
                        "branches_min": 0.0,
                        "branches_max": 0.0,
                        "conditions_min": 0.0,
                        "conditions_max": 0.0,
                    },
                },
                "name": "foo",
                "spaces": [],
            }
        ],
    },
)


@pytest.mark.parametrize("filename, code, expected", [example], ids=["py"])
def test_compute_metrics_shallow(filename, code, expected):
    """Should return the code metrics, but only at the topmost level"""
    expected = deepcopy(expected)
    expected["spaces"] = []
    assert compute_metrics(filename, code, True) == expected


@pytest.mark.parametrize("filename, code, expected", [example], ids=["py"])
def test_compute_metrics_deep(filename, code, expected):
    """Should return the metrics of the code"""
    assert compute_metrics(filename, code, False) == expected


@pytest.mark.parametrize(
    "filename", ["foo.html", "foo", ""], ids=["html", "no_extension", "empty"]
)
def test_invalid_language(filename):
    """Should raise an error for filename of unsupported or no language"""
    with pytest.raises(ValueError, match=r"extension"):
        compute_metrics(filename, "foo", True)
