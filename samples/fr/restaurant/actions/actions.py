from typing import Dict, Text, Any, List, Union, Optional
import logging
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)


class ActionCustom(Action):
   def name(self):
      return "action_custom"

   def run(self, dispatcher, tracker, domain):
      # send utter default response to user with variable {name}
      dispatcher.utter_message(template="utter_custom", name="User")
      # ... other code
      return []


class BookingForm(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "booking_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["cuisine", "num_people", "outdoor_seating", "preferences"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "cuisine": self.from_entity(entity="cuisine"),
            "num_people": self.from_entity(entity="num_people"),
            "outdoor_seating": [
                self.from_entity(entity="seatings"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "preferences": [self.from_text(intent="preferences"), self.from_text()]
        }

    def validate_num_people(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate slot {num_people} value."""

        if self.is_int(value) and  int(value) >= 0:
            return {"num_people": value}
        else:
            #dispatcher.utter_message(template="utter_wrong_num_people")
            return {"num_people": None}

    @staticmethod
    def is_int(value: Text) -> bool:
        try:
            float(value)
        except ValueError:
            return False
        else:
            return float(value).is_integer()

    def validate_outdoor_seating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if isinstance(value, bool):
            return {"outdoor_seating":  "extérieur" if value else "intérieur"}
        return {"outdoor_seating": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []
