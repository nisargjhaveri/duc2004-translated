# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
from collections import defaultdict


articleMap = defaultdict(int)


def getFilePath(dest, id):
    articleId = (id.split('.')[0] + 't').lower()

    articleMap[id] += 1
    fileName = ".".join([id, str(articleMap[id])])

    return os.path.join(dest, articleId, fileName)


def ensureDir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        if not os.path.isdir(dirname):
            raise


def getTranslation(sentence):
    if 'editedTarget' in sentence:
        return sentence['editedTarget']
    return sentence['target']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Parse translated articles dump')

    parser.add_argument('dump', type=file,
                        help="Dump file path")
    parser.add_argument('dest', type=str,
                        help="Path to destimation directory")

    args = parser.parse_args()

    for line in args.dump:
        article = json.loads(line)

        filename = getFilePath(args.dest, article['id'])
        dirname = os.path.dirname(filename)

        ensureDir(dirname)
        with open(filename, "w") as refFile:
            for para in article['bodySentences']:
                line = u" ".join(map(getTranslation, para))
                line = re.sub(r'[\s\xa0]+', ' ', line).strip() + "\n"

                refFile.write(line.encode('utf-8'))
