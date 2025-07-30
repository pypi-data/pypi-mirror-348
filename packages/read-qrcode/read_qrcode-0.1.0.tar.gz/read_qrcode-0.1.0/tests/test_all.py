import pytest

from read_qrcode import read_qrcode


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("tests/data/rqrr.gif", "rqrr"),
        ("tests/data/github.gif", "https://github.com/WanzenBug/rqrr"),
        ("tests/data/number.gif", "1234567891011121314151617181920"),
        ("tests/data/rqrr_incomplete.gif", "rqrr"),
        (
            "tests/data/errors/io_error.png",
            "For testing the IoError, even a valid QR code will do -- the code "
            "being tested is completely independent of the QR code, as long as "
            "it has any content at all. However, for consistency, it's better "
            "to have a separate QR code for this case.\n"
            "Also, you're reading into the library's code! You're awesome! We "
            "hope it's been useful for you!\n"
        ),
        ("tests/data/errors/should-not-panic-1.jpg", "http://m.liantu.com/"),
        ("tests/data/full/superlong.gif", "superlongdata" * 26),
    ],
)
def test_read_qr_success(filename: str, expected: str) -> None:
    result = read_qrcode(filename)
    assert result == expected


@pytest.mark.parametrize(
    "filename",
    [
        "tests/data/errors/data_ecc.png",
        "tests/data/errors/format_ecc.png",
        "tests/data/errors/invalid_version.gif",
        "tests/data/errors/should-not-panic-2.jpg",
        "tests/data/full/gogh.jpg",
        "tests/data/full/multiple.png",
        "tests/data/full/multiple_rotated.png",
    ],
)
def test_read_qr_error(filename: str) -> None:
    with pytest.raises(ValueError):
        read_qrcode(filename)
