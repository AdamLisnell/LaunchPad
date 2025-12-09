import pytest
from core.domain.requirement import Requirement, Choice


def test_choice_creation():
    choice = Choice(id="choice1", text="Yes", value="yes")
    assert choice.id == "choice1"
    assert choice.text == "Yes"
    assert choice.value == "yes"


def test_question_creation():
    # Test Requirement creation with minimal parameters
    Requirement = Requirement()
    assert Requirement.id is None
    assert Requirement.text == ""
    assert Requirement.type == "text"
    assert Requirement.choices == []
    assert Requirement.depends_on is None
    assert Requirement.order == 0

    # Test Requirement creation with parameters
    choices = [
        Choice(id="choice1", text="Yes", value="yes"),
        Choice(id="choice2", text="No", value="no"),
    ]
    Requirement = Requirement(
        id="q1",
        text="Do you agree?",
        type="single_choice",
        choices=choices,
        depends_on={"q0": "yes"},
        order=2,
    )
    assert Requirement.id == "q1"
    assert Requirement.text == "Do you agree?"
    assert Requirement.type == "single_choice"
    assert len(Requirement.choices) == 2
    assert Requirement.choices[0].id == "choice1"
    assert Requirement.choices[1].id == "choice2"
    assert Requirement.depends_on == {"q0": "yes"}
    assert Requirement.order == 2
