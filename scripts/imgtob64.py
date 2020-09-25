import argparse
import base64
import io
from os.path import splitext

from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('--urlsafe', '-u', action='store_true')
args = parser.parse_args()

path = args.path
ext = splitext(path)[-1][1:]

if args.urlsafe:
    b64encoder = base64.urlsafe_b64encode
else:
    b64encoder = base64.b64encode

image = Image.open(path)
buffer = io.BytesIO()
image.save(buffer, format=ext)
b64str = b64encoder(buffer.getvalue())
print(b64str.decode('utf8'))
