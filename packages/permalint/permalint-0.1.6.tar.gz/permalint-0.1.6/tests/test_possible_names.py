from permalint import possible_names
import pytest


@pytest.mark.parametrize(
    "input_name,probable_names",
    [
        (
            "https://taku910.github.io/mecab/",
            [
                "taku910.github.io/mecab",
                "mecab",
                "taku910.github.io",
            ],
        ),
        (
            "https://taku910.github.io/mecab-ipadic/",
            [
                "taku910.github.io/mecab-ipadic",
                "mecab-ipadic",
                "taku910.github.io",
            ],
        ),
        ("mozilla.org/cbindgen", ["mozilla.org/cbindgen", "cbindgen", "mozilla.org"]),
        (
            "poppler.freedesktop.org",
            ["poppler.freedesktop.org", "poppler", "freedesktop.org"],
        ),
        (
            "poppler.freedesktop.org/poppler-data",
            [
                "poppler.freedesktop.org/poppler-data",
                "poppler-data",
                "poppler.freedesktop.org",
            ],
        ),
    ],
)
def test_possible_names(input_name, probable_names):
    assert possible_names(input_name) == probable_names
