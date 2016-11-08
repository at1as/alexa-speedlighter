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


if __name__ == '__main__':
  if __package__ == None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import lambda_function

  unittest.main()
