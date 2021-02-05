#!/usr/bin/python3
import html
import sys

stdin_buffer = getattr(sys.stdin, 'buffer', sys.stdin)


print(html.unescape(stdin_buffer.read().decode("utf-8")))
