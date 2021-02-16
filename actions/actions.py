
import os
import pandas as pd

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from google_trans_new import google_translator  

# create translator object
translator = google_translator()  


class ActionLanguageSearch(Action):    
    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        lang_entities = list(tracker.get_latest_entity_values("language"))

        if len(lang_entities) > 0:
            query_lang = lang_entities.pop()
            hindi_query_lang = query_lang
            query_lang = translator.translate(query_lang, lang_tgt='en')
            query_lang = query_lang.lower().capitalize()

            out_row = wals_data[wals_data["Name"] == query_lang.strip()].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                lang_name = translator.translate(out_row["Name"], lang_tgt='hi')
                lang_family = translator.translate(out_row["Family"], lang_tgt='hi')
                lang_genus = translator.translate(out_row["Genus"], lang_tgt='hi')
                out_text = "इस भाषा का नाम: %s, परिवार: %s, उपपरिवार: %s और आईएसओ कोड: %s है" % (lang_name, lang_family, lang_genus, out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "माफ़ करना! हमारे पास भाषा इस %s का रिकॉर्ड नहीं हैं" % hindi_query_lang)

        return []