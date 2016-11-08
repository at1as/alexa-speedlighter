from   __future__ import print_function
import xml_parser

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(audio_output, audio_reprompt, should_end_session):
  return {
    'outputSpeech': {
      'type': 'PlainText',
      'text': audio_output
    },
    'reprompt': {
      'outputSpeech': {
        'type': 'PlainText',
        'text': audio_reprompt
      }
    },
    'shouldEndSession': should_end_session
  }


def build_speechlet_response_with_card(title, audio_output, card_output, audio_reprompt, should_end_session):
  return {
    'outputSpeech': {
      'type': 'PlainText',
      'text': audio_output
    },
    'card': {
      'type': 'Simple',
      'title': title,
      'content': card_output
    },
    'reprompt': {
      'outputSpeech': {
        'type': 'PlainText',
        'text': audio_reprompt
      }
    },
    'shouldEndSession': should_end_session
  }


def build_response(session_attributes, speechlet_response):
  return {
    'version': '1.0',
    'sessionAttributes': session_attributes,
    'response': speechlet_response
  }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
  output   = 'Welcome to the Speedlighter feed. Ask me for the latest blog post'
  reprompt = 'Ask me what\'s the latest blog post'
  should_end_session = False

  return build_response({}, build_speechlet_response(output, reprompt, should_end_session))


def handle_session_end_request():
  output = 'Have a nice day! '
  should_end_session = True

  return build_response({}, build_speechlet_response(output, None, should_end_session))


def get_recent_posts(intent, session):
  try:
    desired_responses = int(intent['slots']['postNum']['value'])
  except:
    desired_responses = 1

  responses     = xml_parser.get_extracted_text(min(desired_responses, 5))
  response_body = ''

  print('Attempting to fetch {} responses'.format(str(desired_responses)))

  for idx, response in enumerate(responses):
    if response['title']:
      response_body += 'Post {} entitled {}. '.format(idx + 1, response['title'])

    if response['date']:
      response_body += 'Published on {} . '.format(response['date'])

    if response['content']:
      response_body += '{}. '.format(response['content'])

  reprompt_text = None
  speech_output = response_body
  should_end_session = True

  return build_response({}, build_speechlet_response(speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
  print('on_session_started requestId=' + session_started_request['requestId'] + ', sessionId=' + session['sessionId'])


def on_launch(launch_request, session):
  print('on_launch requestId=' + launch_request['requestId'] + ', sessionId=' + session['sessionId'])

  return get_welcome_response()


def on_intent(intent_request, session):
  """ Called when the user specifies an intent for this skill """

  print('on_intent requestId=' + intent_request['requestId'] + ', sessionId=' + session['sessionId'])

  intent = intent_request['intent']
  intent_name = intent_request['intent']['name']

  # Dispatch to your skill's intent handlers
  if intent_name == 'GetNextPost':
    return get_recent_posts(intent, session)
  elif intent_name == 'AMAZON.HelpIntent':
    return get_welcome_response()
  elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
    return handle_session_end_request()
  else:
    raise ValueError('Invalid intent')


def on_session_ended(session_ended_request, session):
  print('on_session_ended requestId=' + session_ended_request['requestId'] + ', sessionId=' + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
  """
  Route the incoming request based on type (LaunchRequest, IntentRequest,
  etc.) The JSON body of the request is provided in the event parameter.
  """
  print('event.session.application.applicationId=' + event['session']['application']['applicationId'])

  if event['session']['application']['applicationId'] != 'amzn1.ask.skill.03f76c69-9c9d-4364-ad9d-8a4dbcddc65d':
    raise ValueError('Invalid Application ID')

  if event['session']['new']:
    on_session_started({'requestId': event['request']['requestId']}, event['session'])

  request_type = event['request']['type']

  if request_type == 'LaunchRequest':
    return on_launch(event['request'], event['session'])
  elif request_type == 'IntentRequest':
    return on_intent(event['request'], event['session'])
  elif request_type == 'SessionEndedRequest':
    return on_session_ended(event['request'], event['session'])
