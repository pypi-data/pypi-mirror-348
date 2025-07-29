import pytest
from finesse.script.containers import KatScript, KatElement, KatKwarg
from testutils.tokens import SPACE, NAME, NUMBER, EQUALS


@pytest.mark.parametrize(
    "script,element",
    (
        (
            # Element with no arguments.
            "fake_element el1",
            KatElement(
                directive=NAME(1, 1, "fake_element"),
                name=NAME(1, 14, "el1"),
                arguments=[],
                extra=[SPACE(1, 13)],
            ),
        ),
        (
            # Element with 4 positional arguments.
            "fake_element el1 1 2 3 4",
            KatElement(
                directive=NAME(1, 1, "fake_element"),
                name=NAME(1, 14, "el1"),
                arguments=[
                    NUMBER(1, 18, "1"),
                    NUMBER(1, 20, "2"),
                    NUMBER(1, 22, "3"),
                    NUMBER(1, 24, "4"),
                ],
                extra=[
                    SPACE(1, 13),
                    SPACE(1, 17),
                    SPACE(1, 19),
                    SPACE(1, 21),
                    SPACE(1, 23),
                ],
            ),
        ),
        (
            # Element with 2 positional arguments and 2 keyword arguments.
            "fake_element el1 1 2 c=3 d=4",
            KatElement(
                directive=NAME(1, 1, "fake_element"),
                name=NAME(1, 14, "el1"),
                arguments=[
                    NUMBER(1, 18, "1"),
                    NUMBER(1, 20, "2"),
                    KatKwarg(
                        key=NAME(1, 22, "c"),
                        equals=EQUALS(1, 23),
                        value=NUMBER(1, 24, "3"),
                    ),
                    KatKwarg(
                        key=NAME(1, 26, "d"),
                        equals=EQUALS(1, 27),
                        value=NUMBER(1, 28, "4"),
                    ),
                ],
                extra=[
                    SPACE(1, 13),
                    SPACE(1, 17),
                    SPACE(1, 19),
                    SPACE(1, 21),
                    SPACE(1, 25),
                ],
            ),
        ),
        (
            # Element with 4 keyword arguments.
            "fake_element el1 a=1 b=2 c=3 d=4",
            KatElement(
                directive=NAME(1, 1, "fake_element"),
                name=NAME(1, 14, "el1"),
                arguments=[
                    KatKwarg(
                        key=NAME(1, 18, "a"),
                        equals=EQUALS(1, 19),
                        value=NUMBER(1, 20, "1"),
                    ),
                    KatKwarg(
                        key=NAME(1, 22, "b"),
                        equals=EQUALS(1, 23),
                        value=NUMBER(1, 24, "2"),
                    ),
                    KatKwarg(
                        key=NAME(1, 26, "c"),
                        equals=EQUALS(1, 27),
                        value=NUMBER(1, 28, "3"),
                    ),
                    KatKwarg(
                        key=NAME(1, 30, "d"),
                        equals=EQUALS(1, 31),
                        value=NUMBER(1, 32, "4"),
                    ),
                ],
                extra=[
                    SPACE(1, 13),
                    SPACE(1, 17),
                    SPACE(1, 21),
                    SPACE(1, 25),
                    SPACE(1, 29),
                ],
            ),
        ),
    ),
)
def test_element(parser, script, element):
    assert parser.parse(script) == KatScript(arguments=[element], extra=[])
