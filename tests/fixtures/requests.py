

WELCOME = {'version': '1.0',
           'response': {
             'outputSpeech':
                {
                  'text': 'Welcome to the Speedlighter feed. Ask me for the latest blog post',
                  'type': 'PlainText'
                },
              'shouldEndSession': False,
              'reprompt':
                {
                  'outputSpeech':
                    {
                      'text': "Ask me what's the latest blog post",
                      'type': 'PlainText'
                    }
                  }
                },
                'sessionAttributes': {}
            }

GOODBYE = {'version': '1.0',
           'response': {
             'outputSpeech': {
               'text': 'Have a nice day! ',
               'type': 'PlainText'},
             'shouldEndSession': True,
             'reprompt': {
               'outputSpeech': {
                 'text': None,
                 'type': 'PlainText'
               }
              }
             },
             'sessionAttributes': {}
            }
