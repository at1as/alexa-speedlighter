from   os import path
import sys
import unittest

class TestStringMethods(unittest.TestCase):

  def test_removing_url_data(self):
    trailing_chars  = ['www.google.com', 'www.google.com/', 'www.google.com?']
    nested_resource = ['www.google.com/abc', 'www.google.com/abc?page=1', 'www.google.com/abc/def', 'www.google.com/abc/def/']
    query_params    = ['www.google.com/?', 'www.google.com?abc=def']
    http_www_urls   = ['https://www.google.com/abc/def?xyz=123', 'http://www.google.com/abc/def?xyz=123']
    http_urls       = ['https://google.com/abc/def?xyz=123', 'http://google.com/abc/def?xyz=123']

    for url in trailing_chars:
      self.assertEqual(xml_parser.remove_url_paths(url), 'google.com')
    
    for url in nested_resource:
      self.assertEqual(xml_parser.remove_url_paths(url), 'google.com')
    
    for url in query_params:
      self.assertEqual(xml_parser.remove_url_paths(url), 'google.com')
    
    for url in http_www_urls:
      self.assertEqual(xml_parser.remove_url_paths(url), 'www.google.com')

    for url in http_urls:
      self.assertEqual(xml_parser.remove_url_paths(url), 'google.com')


  def test_replace_unpronounceable_chars(self):
    input_text = u"Here!\nIs!\u2018Some!\u2019Text!"
    self.assertEqual(xml_parser.replace_unpronounceable_chars(input_text), "Here! Is!'Some!'Text!")


  def test_remove_unpronounceable_chars(self):
    input_text = u"Here!\u2011Is!\u2018Some!\u2019Text!"
    self.assertEqual(xml_parser.remove_unpronounceable_chars(input_text), "Here!Is!Some!Text!")


  def test_extract_date(self):
    input_date = "Fri, 04 Nov 2016 19:53:18 +0000"
    self.assertEqual(xml_parser.extract_date(input_date), "Fri, 04 Nov 2016")


  def test_get_extracted_text_length_0(self):
    function_response = xml_parser.get_extracted_text(0)
    expected_response = [{'content': 'Sorry, there are no recent or archived posts currently available. Please try again later', 'date': '', 'title': ''}]
    self.assertEqual(function_response, expected_response)
 

  def test_get_extracted_text_length_no_params(self):
    self.assertTrue(len(xml_parser.get_extracted_text()) == 1)


  def test_get_extracted_text_length_no_params(self):
    # returned length can be 1 if error, 1 if one post is found, 2 if two posts are found
    # Will scan up to 200 posts, but there is not gaurentee at least two of those will have the desired tag
    self.assertTrue(len(xml_parser.get_extracted_text(2)) <= 2)


if __name__ == '__main__':
  if __package__ == None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import xml_parser
  
  unittest.main()

