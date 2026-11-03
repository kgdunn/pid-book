"""The echoed-output check treats a zero's sign as noise, and nothing else."""

import pytest
from check_code_blocks import output_mismatches


@pytest.mark.parametrize(
    ("echo", "printed"),
    [
        ("O-PLS orthogonal 0.0", "O-PLS orthogonal -0.0"),
        ("O-PLS orthogonal -0.0", "O-PLS orthogonal 0.0"),
        ("{'logP': 0.5, 'Solubility': 0.0}", "{'logP': 0.5, 'Solubility': -0.0}"),
        ("[ 0.   1.2]", "[-0.   1.2]"),
        ("-0.000", "0.000"),
    ],
)
def test_a_signed_zero_matches_an_unsigned_one(echo: str, printed: str) -> None:
    assert output_mismatches(f"print(x)\n# {echo}", printed + "\n") == []


@pytest.mark.parametrize(
    ("echo", "printed"),
    [
        ("-0.05", "0.05"),
        ("-0.5", "0.5"),
        ("-1.0", "1.0"),
        ("1e-05", "1e05"),
    ],
)
def test_a_signed_nonzero_still_has_to_match(echo: str, printed: str) -> None:
    assert output_mismatches(f"print(x)\n# {echo}", printed + "\n") == [echo]
