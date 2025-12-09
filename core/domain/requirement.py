from typing import List, Dict, Optional


class Choice:
    """Requirement choice entity."""

    def __init__(self, id: Optional[str] = None, text: str = "", value: str = ""):
        self.id = id
        self.text = text
        self.value = value


class Requirement:
    """Requirement entity for user candidates."""

    def __init__(
        self,
        id: Optional[str] = None,
        text: str = "",
        type: str = "text",
        choices: Optional[List[Choice]] = None,
        depends_on: Optional[Dict[str, str]] = None,
        order: int = 0,
    ):
        self.id = id
        self.text = text
        self.type = type  # text, single_choice, multiple_choice, etc.
        self.choices = choices or []
        self.depends_on = depends_on  # e.g., {"question_id": "answer_value"}
        self.order = order
