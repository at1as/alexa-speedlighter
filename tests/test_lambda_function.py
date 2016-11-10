from   os import path
import sys
import unittest
import fixtures.requests as response

class TestStringMethods(unittest.TestCase):

  def test_welcome_msg(self):
    welcome_text = lambda_function.get_welcome_response()
    self.assertEqual(welcome_text, response.WELCOME)

  def test_session_end_msg(self):
    goodbye_text = lambda_function.handle_session_end_request()
    self.assertEqual(goodbye_text, response.GOODBYE)

  def test_get_recent_posts_more_than_limit(self):
    # Should return 5, the limit, when asked for 8 posts
    # Note: only 200 posts will be scanned, so less than 5 could be found
    intent = {'slots' : {'postNum' : {'value': 8}}}
    session = {}
    get_posts = lambda_function.get_recent_posts(intent, session)

    self.assertIn('Post 4', get_posts['response']['outputSpeech']['text'])
    self.assertNotIn('Post 5', get_posts['response']['outputSpeech']['text'])


if __name__ == '__main__':
  if __package__ == None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import lambda_function

  unittest.main()
