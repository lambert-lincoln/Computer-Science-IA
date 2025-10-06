class _ApiKey:
    def __init__(self):
        self.api_dict = {
            "fmp api key" : 'INxICpbAyIxj5wNPo2vX4ky1BKY6T15K',
            "alpha vintage api key" : '103V74WY32FL7PWJ',
            "GLM 4.5 API KEY" : "a2c42996f098427fa00d7bb2e621f765.JtKbmR2FDvLRYQgc",
        }
    def get_FMP_key(self):
        return self.api_dict.get('fmp api key', 'key not found')
    def get_AV_key(self):
        return self.api_dict.get('alpha vintage api key', 'key not found')
    def get_ZAI_key(self):
        return self.api_dict.get('GLM 4.5 API KEY', 'key not found')
        