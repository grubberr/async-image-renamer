#!/usr/bin/env python3

"""
https://dev.projectoxford.ai/docs/services/56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fe
"""

import os
import glob
import logging
import argparse
import asyncio
import aiohttp

MICROSOFT_VISION_API_KEY = ''
url = 'http://api.projectoxford.ai/vision/v1.0/describe'


def get_new_filename(filename, text):
    dirname = os.path.dirname(filename)
    ext = os.path.splitext(filename)[1]
    return os.path.join(dirname, text + ext)


async def request(session, filename):

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': MICROSOFT_VISION_API_KEY,
    }

    while True:

        with open(filename, 'rb') as fp:
            response = await session.post(url, data=fp, headers=headers)
            json = await response.json()

        if response.status == 200:
            return (filename, json)

        logging.warn(json)
        await asyncio.sleep(int(response.headers['Retry-After']))


async def bound_request(sem, session, filename):
    async with sem:
        return await request(session, filename)


async def run(filenames):

    sem = asyncio.Semaphore(2)

    async with aiohttp.ClientSession() as session:

        tasks = [bound_request(sem, session, f) for f in filenames]

        for task in asyncio.as_completed(tasks):
            (filename, json) = await task
            text = json['description']['captions'][0]['text']
            new_filename = get_new_filename(filename, text)
            os.rename(filename, new_filename)


def main(dir):

    images = glob.glob(os.path.join(dir, '*.jpg'))

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(run(images))
    ioloop.close()

if __name__ == '__main__':

    assert MICROSOFT_VISION_API_KEY, \
    """
    Please, get a Microsoft API Key,
    https://www.microsoft.com/cognitive-services/en-us/sign-up
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='image directory', type=str)
    args = parser.parse_args()

    main(args.dir)
