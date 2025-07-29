from pathlib import Path
import re

import pytest

from ..dandietag import DandiETag, ETagHashlike, Part, PartGenerator, mb, tb


@pytest.mark.parametrize(
    "file_size,initial_part_size,final_part_size,part_count",
    [
        (0, 0, 0, 0),
        (1, 1, 1, 1),
        (mb(64), mb(64), mb(64), 1),
        (mb(50), mb(50), mb(50), 1),
        (mb(70), mb(64), mb(6), 2),
        (mb(140), mb(64), mb(12), 3),
        (mb(640), mb(64), mb(64), 10),
        (tb(5), 549755814, 549754694, 10000),
    ],
)
def test_part_generator(
    file_size: int, initial_part_size: int, final_part_size: int, part_count: int
) -> None:
    pg = PartGenerator.for_file_size(file_size)
    assert pg == PartGenerator(part_count, initial_part_size, final_part_size)
    assert len(pg) == part_count
    parts = list(pg)
    assert [p.number for p in parts] == list(range(1, part_count + 1))
    assert all(p.size == initial_part_size for p in parts[:-1])
    if parts:
        assert parts[-1].size == final_part_size
    offset = 0
    for p in parts:
        assert p.offset == offset
        offset += p.size
    if parts:
        assert pg[1] == Part(1, 0, initial_part_size)
        assert pg[part_count] == Part(
            part_count, initial_part_size * (part_count - 1), final_part_size
        )
    with pytest.raises(IndexError):
        pg[0]
    with pytest.raises(IndexError):
        pg[part_count + 1]
    with pytest.raises(IndexError):
        pg[-1]


def test_part_generator_too_large() -> None:
    with pytest.raises(ValueError) as excinfo:
        PartGenerator.for_file_size(tb(5) + 1)
    assert str(excinfo.value) == "File is larger than the S3 maximum object size."


def test_dandietag_tiny(tmp_path: Path) -> None:
    f = tmp_path / "sample.txt"
    f.write_bytes(b"123")
    s = DandiETag.from_file(f).as_str()
    assert s == "d022646351048ac0ba397d12dfafa304-1"
    assert re.fullmatch(DandiETag.REGEX, s)
    assert len(s) <= DandiETag.MAX_STR_LENGTH


def test_dandietag_null(tmp_path: Path) -> None:
    f = tmp_path / "sample.dat"
    f.write_bytes(b"\0")
    s = DandiETag.from_file(f).as_str()
    assert s == "7e4696ef25d5faececd853ce5e2a233b-1"
    assert re.fullmatch(DandiETag.REGEX, s)
    assert len(s) <= DandiETag.MAX_STR_LENGTH


PART_DIGESTS = [
    b"\x06\x1c\x9a\xee\xac\x02\x0f\xd8\xa1\xd1\xc9\xcbb\x1d'V",
    b"\xd5z\x92\x92\t\xdd\xfbX\xf6\x05\x83\xcb\xcf\x96\xde%",
    b"z\x88\x9e\xe7m\x9a\n{=\x85,\xc2t_\x1e#",
    b"\x84\xc6<M\x1a$%\xac?\x1a\x0bt\xf0|sY",
    b"\xa3\x98\xc1d\xf5e\xdb;\xd0\xe5\x87\x19\x8d\xcd5\xe9",
    b"\xd7\xe1\x0c\xf2\xfa\x985)\xa8\x8a\xa7\x19z%)\x96",
    b"\xfe\x12\x82\xdb^\x0fr|\x9f\xd5\x924\xba?\xd5D",
    b"*~@\xb4\x19:\xa0\xa2\xc0\xa5q\x82\xcdgv@",
    b"\xaf\x89\x88V^\x00\x9f\x8f\xeb\xf8\x1e\x90\x17\xe4\xf7\xf4",
    b"\xf8\t\xb3fn!\x9c\x13\x8e\x1d\x86\xfd}\x91H\xbf",
]

ETAG = "8e5394f58846c6874be226c5a251f780-10"


def test_add_next_digest() -> None:
    etagger = DandiETag(mb(640))
    assert etagger.part_qty == 10
    for i, d in enumerate(PART_DIGESTS):
        assert not etagger.complete
        with pytest.raises(ValueError) as excinfo:
            etagger.as_str()
        assert str(excinfo.value) == "Not all part hashes submitted"
        p = etagger.get_next_part()
        assert p is not None and p.number == i + 1
        assert etagger.get_part_etag(p) is None
        etagger._add_next_digest(d)
        assert etagger.get_part_etag(p) == d.hex()
    assert etagger.complete
    assert etagger.get_next_part() is None
    s = etagger.as_str()
    assert s == ETAG
    assert re.fullmatch(DandiETag.REGEX, s)
    assert len(s) <= DandiETag.MAX_STR_LENGTH


def test_add_digest_reversed() -> None:
    etagger = DandiETag(mb(640))
    assert etagger.part_qty == 10
    assert not etagger.complete
    for p, d in reversed(list(zip(etagger.get_parts(), PART_DIGESTS))):
        assert not etagger.complete
        etagger._add_digest(p, d)
    assert etagger.complete
    assert etagger.as_str() == ETAG  # type: ignore[unreachable]


def test_add_digest_out_of_order() -> None:
    etagger = DandiETag(mb(640))
    assert etagger.part_qty == 10
    assert not etagger.complete
    pieces = list(zip(etagger.get_parts(), PART_DIGESTS))
    for p, d in pieces[::2] + pieces[1::2]:
        assert not etagger.complete
        etagger._add_digest(p, d)
    assert etagger.complete
    assert etagger.as_str() == ETAG  # type: ignore[unreachable]


def test_etaghashlike() -> None:
    sizes = [mb(20), mb(30), mb(75), mb(5)]
    hasher = ETagHashlike(sum(sizes))
    for sz in sizes:
        hasher.update(b"\0" * sz)
    assert hasher.hexdigest() == "4dc80858c50371577551592f20ac0075-3"
