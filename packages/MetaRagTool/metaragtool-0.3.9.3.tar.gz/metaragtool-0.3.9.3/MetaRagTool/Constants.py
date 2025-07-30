use_wandb = False
local_mode = False
trust_remote_code = True
lang='multi'



WandbToken = None
HFToken = None
GitHubToken = None

API_KEY_GEMINI = None
API_KEY_OPENAI = None
API_KEY_OPENROUTER = None

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except BaseException:
    try:
        nltk.download('punkt')
    except BaseException as e:
        print(f"Error downloading 'punkt' for nltk: {e}")


