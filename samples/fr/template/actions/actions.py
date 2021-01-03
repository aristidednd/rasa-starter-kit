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
      dispatcher.utter_message(template="utter_hello_world", name="User")
      # ... other code
      return []


class CustomForm(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "custom_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "cuisine": self.from_entity(entity="cuisine", not_intent="chitchat"),
            "num_people": [
                self.from_entity(
                    entity="number", intent=["inform", "request_restaurant"]
                ),
            ],
            "outdoor_seating": [
                self.from_entity(entity="seating"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "preferences": [
                self.from_intent(intent="deny", value="no additional preferences"),
                self.from_text(not_intent="affirm"),
            ],
            "feedback": [self.from_entity(entity="feedback"), self.from_text()],
            "search_type": [
                self.from_trigger_intent(
                    intent="search_transactions", value="spend"
                ),
                self.from_trigger_intent(
                    intent="check_earnings", value="deposit"
                )
            ]
        }

    def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate slot {cuisine} value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": value}
        else:
            dispatcher.utter_message(template="utter_wrong_cuisine")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cuisine": None}

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
