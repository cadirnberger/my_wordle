import random
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


def get_game_context(tracker: Tracker) -> Dict[Text, Any]:
    latest_message = tracker.latest_message or {}
    metadata = latest_message.get("metadata") or {}
    return metadata.get("wordle", {}) if isinstance(metadata, dict) else {}



def get_most_common_letter_from_metadata(game_context: Dict[Text, Any]) -> Text:
    letters: Dict[Text, int] = {}
    answer = str(game_context.get("answer") or "").upper()
    
    for letter in answer:
        if letter.isalpha():
         letters[letter] = letters.get(letter, 0) + 1
    if max(letters.values()) == 2:
        return "Doesn't have a common letter"
    else:
        return sorted(letters.items(), key=lambda item: (-item[1], item[0]))[0][0]


class ActionWordleHint(Action):
    def name(self) -> Text:
        return "wordle_hint"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        game_context = get_game_context(tracker)
        common_letter = get_most_common_letter_from_metadata(game_context)
        message = (
            f"Hint: the most common letter in your guesses is '{common_letter}'. "
            f"Try using it in your next guess."
        )
        dispatcher.utter_message(text=message)
        return []


class ActionWordleDefinition(Action):
    def name(self) -> Text:
        return "wordle_definition"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        game_context = get_game_context(tracker)
        definition = str(game_context.get("definition") or "No definition available.")
        dispatcher.utter_message(text=f"Definition: {definition}")
        return []