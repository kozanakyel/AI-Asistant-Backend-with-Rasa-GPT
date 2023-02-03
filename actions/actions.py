# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_TSHIRT_SIZES = ["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_TSHIRT_COLOR = ["red", "blue", "yellow", "orange", "pink"]

class ValidateSimpleTshirtForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_tshirt_form"

    def validate_tshirt_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `tshirt_size` value."""

        if slot_value.lower() not in ALLOWED_TSHIRT_SIZES:
            dispatcher.utter_message(text=f"We only accept tshirt sizes: s/m/l/xl.")
            return {"tshirt_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} tshirt.")
        return {"tshirt_size": slot_value}

    def validate_tshirt_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `tshirt_type` value."""

        if slot_value not in ALLOWED_TSHIRT_COLOR:
            dispatcher.utter_message(text=f"I don't recognize that tshirt. We serve {'/'.join(ALLOWED_TSHIRT_COLOR)}.")
            return {"tshirt_color": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} tshirt.")
        return {"tshirt_color": slot_value}
