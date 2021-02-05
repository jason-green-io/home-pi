#!/usr/bin/python3
import requests
import qrunicode
import itertools
import textwrap
import time
import os

w = 60

while True:
    r = requests.get("http://jservice.io/api/random?count=1")

    obj = r.json()[0]

    answer = qrunicode.qrunicode(obj["answer"])

    cat = textwrap.wrap("{} for {} Alex".format(obj.get("category", {}).get("title", ""), obj.get("value", "")), w)
    cat = "\n".join(cat)

    question = textwrap.wrap(obj["question"], w)
    question = cat + "\n\n" + "\n".join(question)

    #text = ["  ".join(a) for a in (filter(None, b) for b in itertools.zip_longest(answer, question))]
    #print("\n".join(text))

    print(question)
    print("")
    print(answer)
    time.sleep(30)
    print("\n" * 30)
