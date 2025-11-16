class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
    def chat(self, prompt):
        return '[Gemini stub] ' + (prompt or '')
    def analyze_risk(self, src, mode, data):
        return '[Gemini stub analysis]'
