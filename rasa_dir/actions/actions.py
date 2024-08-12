from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import sys
import os

# Assuming your project directory structure
project_root = os.path.dirname(os.path.dirname(__file__))
bn_dir = os.path.join(project_root, '..', 'bn_dir')

print(bn_dir)
sys.path.insert(0, bn_dir)

from bayesian_selector import ElectiveSelector
class ValidateElectivesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_electives_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("project") == "no":
            updated_slots.remove("project_type")

        return updated_slots

    def validate_semester(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value.lower() in ["winter", "summer", "any"]:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"semester": slot_value}
        else:
            dispatcher.utter_message("I'm sorry, but the semester options are winter and summer only.")
            return {"semester": None}
        
    def validate_course_content(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ["manipulation", "perception", "navigation", "artificial_intelligence", "machine_learning", "robotics", "natural_language_processing", "any"]:
            dispatcher.utter_message("I'm sorry, but the course content options are manipulation, perception, navigation, artificial intelligence, machine learning, HRI, control, and natural language processing only.")
            return {"course_content": None}
        return {"course_content": slot_value}
    
    def validate_university(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ["unibonn", "hbrs", "any"]:
            dispatcher.utter_message("I'm sorry, but the university options are UniBonn and HBRS only.")
            return {"university": None}
        return {"university": slot_value}
    
    def validate_project_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ["individual", "group", "any"]:
            dispatcher.utter_message("I'm sorry, but the project type options are individual and group only.")
            return {"project_type": None}
        return {"project_type": slot_value}
    
    def validate_exam(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ["written", "oral", "any"]:
            dispatcher.utter_message("I'm sorry, but the exam options are written and oral only.")
            return {"exam": None}
        return {"exam": slot_value}
    
    def validate_course_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ["theory", "practical", "research", "any"]:
            dispatcher.utter_message("I'm sorry, but the course type options are theory, practical, and research only.")
            return {"course_type": None}
        return {"course_type": slot_value}
    
class ActionFetchElectives(Action):
    def name(self) -> Text:
        return "action_fetch_electives"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        semester = tracker.get_slot("semester")
        course_content = tracker.get_slot("course_content")
        university = tracker.get_slot("university")
        assignment = tracker.get_slot("assignment")
        project = tracker.get_slot("project")
        project_type = tracker.get_slot("project_type")
        exam = tracker.get_slot("exam")
        prerequisites = tracker.get_slot("prerequisites")
        course_type = tracker.get_slot("course_type")
        
        evidence = {}
        if semester != "any":
            if semester == "winter":
                evidence["semester_winter"] = 1
            if semester == "summer":
                evidence["semester_summer"] = 1
        if course_content != "any":
            evidence["course_content"] = course_content
        if university != "any":
            evidence["university"] = university
        if assignment != "any":
            if assignment == "yes":
                assignment = True
            else:
                assignment = False
            evidence["assignment"] = assignment
        if project != "any":
            if project == "yes":
                project = True
            else:
                project = False
        if project == 'yes' and project_type != "any":
            evidence["project_type"] = project_type
        if exam != "any":
            evidence["exam"] = exam
        if prerequisites != "any":
            # if user has not done the mandatory courses, then electives that require prerequisites are not shown
            # if user has done the mandatory courses, then all electives are shown
            if prerequisites == "no":
                evidence["prerequisites"] = False
        if course_type != "any":
            evidence["course_type"] = course_type

        print(evidence)

        yaml_path = os.path.join(bn_dir, 'courses.yaml')
        elective_selector = ElectiveSelector(yaml_path=yaml_path)
        electives = elective_selector.get_top_electives(evidence)
        dispatcher.utter_message(
            f"Here are the electives that match your criteria: {electives}"
        )

        return []
    
class ActionClearSlots(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        return[SlotSet(slot, None) for slot in tracker.slots.keys()]