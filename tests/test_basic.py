"""
Tests for the RecommenderXBlock
"""

import json
from unittest.mock import patch
import requests
from django.test.testcases import TestCase
from .utils import make_block, make_url
from recommender.recommender import strip_and_clean_url


class TestForRecommenderXblock(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.xblock = make_block()
        self.recommendations = [
            {"id": 1, "title": "Covalent bonding and periodic trends", "upvotes": 15, "downvotes": 5, "url": "https://courses.edx.org/courses/MITx/3.091X/2013_Fall/courseware/SP13_Week_4/SP13_Periodic_Trends_and_Bonding/",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/videopage1.png", "descriptionText": "short description for Covalent bonding and periodic trends"},
            {"id": 2, "title": "Polar covalent bonds and electronegativity", "upvotes": 10, "downvotes": 7, "url": "https://courses.edx.org/courses/MITx/3.091X/2013_Fall/courseware/SP13_Week_4/SP13_Covalent_Bonding/",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/videopage2.png", "descriptionText": "short description for Polar covalent bonds and electronegativity"},
            {"id": 3, "title": "Longest wavelength able to to break a C-C bond ...", "upvotes": 1230, "downvotes": 7, "url": "https://answers.yahoo.com/question/index?qid=20081112142253AA1kQN1",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/dispage1.png", "descriptionText": "short description for Longest wavelength able to to break a C-C bond ..."},
            {"id": 4, "title": "Calculate the maximum wavelength of light for ...", "upvotes": 10, "downvotes": 3457, "url": "https://answers.yahoo.com/question/index?qid=20100110115715AA6toHw",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/dispage2.png", "descriptionText": "short description for Calculate the maximum wavelength of light for ..."},
            {"id": 5, "title": "Covalent bond - wave mechanical concept", "upvotes": 10, "downvotes": 7, "url": "http://people.csail.mit.edu/swli/edx/recommendation/img/textbookpage1.png",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/textbookpage1.png", "descriptionText": "short description for Covalent bond - wave mechanical concept"},
            {"id": 6, "title": "Covalent bond - Energetics of covalent bond", "upvotes": 10, "downvotes": 7, "url": "http://people.csail.mit.edu/swli/edx/recommendation/img/textbookpage2.png",
                "description": "http://people.csail.mit.edu/swli/edx/recommendation/img/textbookpage2.png", "descriptionText": "short description for Covalent bond - Energetics of covalent bond"}
        ]
        self.xblock.recommendations = json.dumps(self.recommendations)
        self.xblock.default_recommendations = json.dumps(self.recommendations)

    def test_user_is_staff(self):
        isStaff = self.xblock.get_user_is_staff()
        assert isStaff

    def test_validation_resource(self):
        mock_resourceId = 'https://courses.edx.org/courses/MITx/3.091X/2013_Fall/courseware/SP13_Week_4/SP13_Periodic_Trends_and_Bonding/'

        result = self.xblock._validate_resource(
            mock_resourceId, 'recommender_upvote')

        assert result == mock_resourceId

    @patch('recommender.recommender.strip_and_clean_url')
    def test_strip_and_clean_url(self, mock_method):
        mock_method.return_value = 'http://google.com'
        self.assertEqual(strip_and_clean_url(
            'http://google.com'), 'http://google.com')
        self.assertEqual(strip_and_clean_url(
            '1'), '')

    @patch('requests.post')
    def test_upvote_new_resource(self, mock_post):
        resource_id = '1'
        mock_post.return_value = {'newVotes': 16}
        data = {'id': resource_id,
                'event': 'recommender_upvote'}
        url = make_url(handler='handle_vote')
        response = requests.post(url, data=json.dumps(
            data), headers={'Content-Type': 'application/json'}, timeout=10)
        mock_post.assert_called_with(url, data=json.dumps(
            data), headers={'Content-Type': 'application/json'}, timeout=10)

        assert response['newVotes'] == 16
