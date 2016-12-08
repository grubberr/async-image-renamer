# async-image-renamer
rename image files using computer vision

## Usage

### 1) Get a Microsoft API Key for Free
[https://www.microsoft.com/cognitive-services/en-us/sign-up](https://www.microsoft.com/cognitive-services/en-us/sign-up "API Key").

Replace this key with `MICROSOFT_VISION_API_KEY` in renamer.py

### 2) Usage

`
python3 -m venv env
. env/bin/activate
pip install aiohttp
python3 renamer.py images
`

## Credits

Originally inspired from https://github.com/sanjujosh/auto-image-renamer
