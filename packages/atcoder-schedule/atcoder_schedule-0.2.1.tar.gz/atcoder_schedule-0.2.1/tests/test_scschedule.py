# tests/test_acschedule.py

from pathlib import Path

import pytest
from requests_mock import Mocker as RequestsMocker

import acschedule


@pytest.fixture
def atcoder_mock(requests_mock: RequestsMocker) -> RequestsMocker:
    content_ja = Path("tests/data/ja.html").read_bytes()
    content_en = Path("tests/data/en.html").read_bytes()
    requests_mock.get("https://atcoder.jp/contests/", content=content_ja)
    requests_mock.get("https://atcoder.jp/contests/?lang=ja", content=content_ja)
    requests_mock.get("https://atcoder.jp/contests/?lang=en", content=content_en)
    return requests_mock


def test_main_ja(atcoder_mock, capsys):
    acschedule.cli(["-l", "ja"])
    assert capsys.readouterr().out == open("tests/data/ja.jsonl").read()


def test_main_en(atcoder_mock, capsys):
    acschedule.cli(["-l", "en", "-z", "UTC"])
    assert capsys.readouterr().out == open("tests/data/en.jsonl").read()
