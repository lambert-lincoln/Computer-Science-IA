class _ApiKey:
    def __init__(self):
        self.api_dict = {
            "GLM 4.5 API KEY" : "a2c42996f098427fa00d7bb2e621f765.JtKbmR2FDvLRYQgc",
        }
    def get_ZAI_key(self):
        return self.api_dict.get('GLM 4.5 API KEY', 'key not found')
        