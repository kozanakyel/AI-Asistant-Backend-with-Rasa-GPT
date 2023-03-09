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

location_db = {
    'shopping': 'For the Shopping Center you can follow The square will turn to the first left and stay on the right when you move forward a little.',
    'bowling': 'For playing Bowling. When you enter the first left of the square, there is a bowling alley in the new building standing right across it. enjoy.',
    'sport': 'for going to Sport Center You should have to turn back from here and enter right from where the street ends. good luck'
}


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
        print(f'tracker: {tracker.sender_id}')
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
    
    
class ChooseAddress(Action):
    def name(self) -> Text:
        return "choose_address"
    
    def run(self, 
            dispatcher: CollectingDispatcher,  #send msg to user
            tracker: Tracker,   # fetch info/intent/entities
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        print("Custom code goes here!")
        
        current_place = next(tracker.get_latest_entity_values("address_loc"), None)
        
        #if not current_place:
            #msg = f'can you give a addres for directions'
            #dispatcher.utter_message(text=msg)
            #return []
        if current_place:
            print(f'current place: {current_place}')
            dispatcher.utter_message(text=location_db[current_place])
            return []
        
        return []
