import unittest
import sys
import os

# Add parent directory to path to import rank.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rank import is_honeypot

class TestHoneypotDetection(unittest.TestCase):
    def test_valid_candidate(self):
        c = {
            'profile': {'years_of_experience': 5.0},
            'skills': [{'name': 'Python', 'proficiency': 'expert', 'duration_months': 60}],
            'career_history': [{'company': 'TCS', 'start_date': '2021-01', 'title': 'Software Engineer'}],
            'education': [{'degree': 'B.Tech', 'start_year': 2016}]
        }
        ishp, msg = is_honeypot(c)
        self.assertFalse(ishp, "Valid candidate should not be flagged")

    def test_expert_zero_duration(self):
        c = {
            'profile': {'years_of_experience': 5.0},
            'skills': [{'name': 'RAG', 'proficiency': 'expert', 'duration_months': 0}],
        }
        ishp, msg = is_honeypot(c)
        self.assertTrue(ishp)
        self.assertIn("expert with 0 duration", msg)

    def test_tech_before_release(self):
        c = {
            'profile': {'years_of_experience': 8.0},
            'skills': [{'name': 'GPT-4', 'proficiency': 'expert', 'duration_months': 60}],
        }
        ishp, msg = is_honeypot(c)
        self.assertTrue(ishp)
        self.assertIn("impossible duration", msg)
        self.assertIn("GPT-4", msg)

    def test_job_before_founding(self):
        c = {
            'profile': {'years_of_experience': 10.0},
            'career_history': [{'company': 'Sarvam AI', 'start_date': '2019-05', 'title': 'AI Engineer'}],
        }
        # Sarvam AI founded in 2023
        ishp, msg = is_honeypot(c)
        self.assertTrue(ishp)
        self.assertIn("founded 2023", msg)

    def test_job_before_education(self):
        c = {
            'profile': {'years_of_experience': 10.0},
            'career_history': [{'company': 'Infosys', 'start_date': '2012-05', 'title': 'Software Engineer'}],
            'education': [{'degree': 'B.Tech', 'start_year': 2018}]
        }
        ishp, msg = is_honeypot(c)
        self.assertTrue(ishp)
        self.assertIn("college started 2018", msg)

    def test_skill_duration_exceeds_yoe(self):
        c = {
            'profile': {'years_of_experience': 3.0}, # 36 months
            'skills': [{'name': 'Java', 'duration_months': 60}], # 60 months
        }
        ishp, msg = is_honeypot(c)
        self.assertTrue(ishp)
        self.assertIn("exceeds total YoE", msg)

if __name__ == '__main__':
    unittest.main()
