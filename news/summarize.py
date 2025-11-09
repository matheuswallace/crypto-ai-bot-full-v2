import os
OPENAI_KEY = os.getenv('OPENAI_API_KEY','')
def summarize(text):
    if not OPENAI_KEY:
        return 'OpenAI not configured'
    return 'Summary placeholder'
