import os
import yaml
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

class ElectiveSelector:
    '''Bayesian Network based elective selector'''
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.df = None
        self.model = None
        self.inference = None
        self.mappings = None
        self.inv_mappings = None
        self.load_data()
        self.create_model()

    def load_data(self):
        
        with open(self.yaml_path, 'r') as file:
            data = yaml.safe_load(file)
        
        courses = []
        for course, attributes in data.items():
            semesters = attributes.pop('semester')
            attributes['elective'] = course
            attributes['semester_winter'] = 1 if 'winter' in semesters else 0
            attributes['semester_summer'] = 1 if 'summer' in semesters else 0
            courses.append(attributes)

        self.df = pd.DataFrame(courses)
        print(self.df)
        self.mappings = self.create_mappings(self.df)
        self.df.replace(self.mappings, inplace=True)

    def create_mappings(self, df):
        mappings = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                mappings[col] = {val: idx for idx, val in enumerate(df[col].unique())}
        return mappings

    def create_model(self):
        self.model = BayesianNetwork()

        nodes_list = ["semester_winter", "semester_summer", "course_content", "university", "assignment", "project", "exam", "prerequisites", "course_type", "project_type", "elective"]
        self.model.add_nodes_from(nodes_list)

        self.model.add_edges_from([
            ("semester_winter", "course_content"),
            ("semester_summer", "course_content"),
            ("course_content", "university"),
            ("university", "prerequisites"),
            ("university", "course_type"),
            ("university", "assignment"),
            ("university", "project"),
            ("university", "exam"),
            ("project", "project_type"),
            ("prerequisites", "elective"),
            ("course_type", "elective"),
            ("assignment", "elective"),
            ("project_type", "elective"),
            ("exam", "elective")
        ])

        self.model.fit(self.df, estimator=MaximumLikelihoodEstimator)
        self.inference = VariableElimination(self.model)

    def map_evidence(self, evidence):
        mapped_evidence = {}
        for key, value in evidence.items():
            if key in self.mappings:
                mapped_evidence[key] = self.mappings[key][value]
            else:
                mapped_evidence[key] = value
        return mapped_evidence

    def get_top_electives(self, evidence, top_n=3):
        mapped_evidence = self.map_evidence(evidence)
        conditional_probs = self.inference.query(variables=['elective'], evidence=mapped_evidence)

        self.inv_mappings = {column: {value: key for key, value in mapping.items()} for column, mapping in self.mappings.items()}

        penalty_factor = 0.1
        for elective in self.df['elective'].unique():
            elective_str = self.inv_mappings['elective'][elective]
            for key, value in evidence.items():
                value = self.mappings[key][value] if key in self.mappings else value
                if key in self.df.columns and self.df[self.df['elective'] == elective][key].values[0] != value:
                    conditional_probs.values[elective] *= penalty_factor

        prob_dict = {self.inv_mappings['elective'][idx]: prob for idx, prob in enumerate(conditional_probs.values)}
        sorted_probs = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)

        return [sorted_probs[i][0] for i in range(min(top_n, len(sorted_probs)))]

# Example usage
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(script_dir, 'courses.yaml')
    selector = ElectiveSelector(yaml_path)
    
    # Example evidence
    evidence = {'university':'hbrs', 'course_content':'robotics', 'semester_winter': 0}
    
    top_electives = selector.get_top_electives(evidence, top_n=3)
    print("Top electives:", top_electives)
