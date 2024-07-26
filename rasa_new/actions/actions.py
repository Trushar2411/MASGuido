import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

# Initialize the Bayesian Network
def initialize_bn():
    bn = gum.BayesNet('CourseRecommendation')

    # Add nodes representing user preferences and course attributes
    topic_pref = bn.add(gum.LabelizedVariable('TopicPreference', 'Preference for Topic', 3))
    difficulty_pref = bn.add(gum.LabelizedVariable('DifficultyPreference', 'Preference for Difficulty', 3))
    duration_pref = bn.add(gum.LabelizedVariable('DurationPreference', 'Preference for Duration', 3))
    format_pref = bn.add(gum.LabelizedVariable('FormatPreference', 'Preference for Format', 3))

    course_topic = bn.add(gum.LabelizedVariable('CourseTopic', 'Course Topic', 3))
    course_difficulty = bn.add(gum.LabelizedVariable('CourseDifficulty', 'Course Difficulty', 3))
    course_duration = bn.add(gum.LabelizedVariable('CourseDuration', 'Course Duration', 3))
    course_format = bn.add(gum.LabelizedVariable('CourseFormat', 'Course Format', 3))
    course_rating = bn.add(gum.LabelizedVariable('CourseRating', 'Course Rating', 3))

    # Add arcs representing the dependencies
    bn.addArc(topic_pref, course_topic)
    bn.addArc(difficulty_pref, course_difficulty)
    bn.addArc(duration_pref, course_duration)
    bn.addArc(format_pref, course_format)
    bn.addArc(course_topic, course_rating)
    bn.addArc(course_difficulty, course_rating)
    bn.addArc(course_duration, course_rating)
    bn.addArc(course_format, course_rating)

    return bn

def set_cpts(bn):
    # Define the Conditional Probability Tables (CPTs)
    bn.cpt('TopicPreference').fillWith([0.3, 0.5, 0.2])
    bn.cpt('DifficultyPreference').fillWith([0.4, 0.4, 0.2])
    bn.cpt('DurationPreference').fillWith([0.5, 0.3, 0.2])
    bn.cpt('FormatPreference').fillWith([0.6, 0.3, 0.1])

    bn.cpt('CourseTopic')[{'TopicPreference': 0}] = [0.7, 0.2, 0.1]
    bn.cpt('CourseTopic')[{'TopicPreference': 1}] = [0.1, 0.6, 0.3]
    bn.cpt('CourseTopic')[{'TopicPreference': 2}] = [0.2, 0.2, 0.6]

    bn.cpt('CourseDifficulty')[{'DifficultyPreference': 0}] = [0.5, 0.3, 0.2]
    bn.cpt('CourseDifficulty')[{'DifficultyPreference': 1}] = [0.3, 0.5, 0.2]
    bn.cpt('CourseDifficulty')[{'DifficultyPreference': 2}] = [0.2, 0.2, 0.6]

    bn.cpt('CourseDuration')[{'DurationPreference': 0}] = [0.6, 0.2, 0.2]
    bn.cpt('CourseDuration')[{'DurationPreference': 1}] = [0.2, 0.6, 0.2]
    bn.cpt('CourseDuration')[{'DurationPreference': 2}] = [0.2, 0.2, 0.6]

    bn.cpt('CourseFormat')[{'FormatPreference': 0}] = [0.5, 0.3, 0.2]
    bn.cpt('CourseFormat')[{'FormatPreference': 1}] = [0.3, 0.5, 0.2]
    bn.cpt('CourseFormat')[{'FormatPreference': 2}] = [0.2, 0.2, 0.6]

    # Example CPT for course_rating (partially filled, needs to be completed)
    bn.cpt('CourseRating').fillWith(0)  # Initialize with zeros for completeness
    bn.cpt('CourseRating')[{'CourseTopic': 0, 'CourseDifficulty': 0, 'CourseDuration': 0, 'CourseFormat': 0}] = [0.6, 0.3, 0.1]
    bn.cpt('CourseRating')[{'CourseTopic': 0, 'CourseDifficulty': 0, 'CourseDuration': 0, 'CourseFormat': 1}] = [0.5, 0.3, 0.2]
    bn.cpt('CourseRating')[{'CourseTopic': 0, 'CourseDifficulty': 0, 'CourseDuration': 0, 'CourseFormat': 2}] = [0.4, 0.3, 0.3]
    bn.cpt('CourseRating')[{'CourseTopic': 0, 'CourseDifficulty': 1, 'CourseDuration': 1, 'CourseFormat': 1}] = [0.3, 0.5, 0.2]
    bn.cpt('CourseRating')[{'CourseTopic': 1, 'CourseDifficulty': 2, 'CourseDuration': 2, 'CourseFormat': 2}] = [0.2, 0.2, 0.6]

    # Fill remaining CPTs with example data
    for t in range(3):
        for d in range(3):
            for du in range(3):
                for f in range(3):
                    if bn.cpt('CourseRating')[{'CourseTopic': t, 'CourseDifficulty': d, 'CourseDuration': du, 'CourseFormat': f}].sum() == 0:
                        bn.cpt('CourseRating')[{'CourseTopic': t, 'CourseDifficulty': d, 'CourseDuration': du, 'CourseFormat': f}] = [0.33, 0.33, 0.34]

bn = initialize_bn()
set_cpts(bn)

def perform_inference(bn, evidence):
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()
    result = ie.posterior('CourseRating')
    return result

def generate_recommendations(result, courses):
    course_rating_dist = result.toarray()
    recommendations = sorted(range(len(course_rating_dist)), key=lambda k: course_rating_dist[k], reverse=True)
    return [courses[course] for course in recommendations]

class ActionCourseRecommendation(Action):
    def name(self) -> str:
        return "action_course_recommendation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        preferences = {
            'TopicPreference': tracker.get_slot('topic_preference'),
            'DifficultyPreference': tracker.get_slot('difficulty_preference'),
            'DurationPreference': tracker.get_slot('duration_preference'),
            'FormatPreference': tracker.get_slot('format_preference'),
        }

        evidence = {
            'TopicPreference': preferences['TopicPreference'],
            'DifficultyPreference': preferences['DifficultyPreference'],
            'DurationPreference': preferences['DurationPreference'],
            'FormatPreference': preferences['FormatPreference'],
        }

        result = perform_inference(bn, evidence)

        courses = [
            {'name': 'AI Basics', 'topic': 0, 'difficulty': 0, 'duration': 0, 'format': 0, 'rating': 1},
            {'name': 'AI Advanced', 'topic': 0, 'difficulty': 2, 'duration': 2, 'format': 2, 'rating': 3},
            {'name': 'AMR Basics', 'topic': 1, 'difficulty': 0, 'duration': 1, 'format': 1, 'rating': 2},
            {'name': 'AMR Intermediate', 'topic': 1, 'difficulty': 1, 'duration': 2, 'format': 2, 'rating': 3},
            {'name': 'ISW Basics', 'topic': 2, 'difficulty': 0, 'duration': 1, 'format': 1, 'rating': 2},
            {'name': 'ISW Advanced', 'topic': 2, 'difficulty': 2, 'duration': 2, 'format': 2, 'rating': 3}
        ]

        recommendations = generate_recommendations(result, courses)

        response = "Based on your preferences, I recommend the following courses:\n"
        for idx, course in enumerate(recommendations):
            response += f"{idx+1}. {course['name']} with Rating Level {course['rating']}\n"

        dispatcher.utter_message(response)
        return []

