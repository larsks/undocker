#!/usr/bin/python

import argparse
import json
import logging
import os
import sys
import tarfile
import tempfile

from contextlib import closing


LOG = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--tag', '-t',
                   default='latest')
    p.add_argument('--ignore-errors', '-i',
                   action='store_true')
    p.add_argument('--output', '-o',
                   default='.')
    p.add_argument('--verbose', '-v',
                   action='store_const',
                   const=logging.INFO,
                   dest='loglevel')
    p.add_argument('--debug', '-d',
                   action='store_const',
                   const=logging.DEBUG,
                   dest='loglevel')
    p.set_defaults(level=logging.WARN)
    return p.parse_args()


def find_layers(img, id):
    with closing(img.extractfile('%s/json' % id)) as fd:
        info = json.load(fd)

    LOG.debug('layer = %s', id)
    for k in ['os', 'architecture', 'author']:
        if k in info:
            LOG.debug('%s = %s', k, info[k])

    yield id
    if 'parent' in info:
        pid = info['parent']
        for layer in find_layers(img, pid):
            yield layer

def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    with tempfile.NamedTemporaryFile() as fd:
        fd.write(sys.stdin.read())
        fd.seek(0)
        with tarfile.TarFile(fileobj=fd) as img:
            repos = img.extractfile('repositories')
            repos = json.load(repos)

            top = repos[repos.keys()[0]][args.tag]
            LOG.info('extracting image %s', top)
            layers = list(find_layers(img, top))

            if not os.path.isdir(args.output):
                os.mkdir(args.output)

            for id in reversed(layers):
                LOG.info('extracting layer %s', id)
                with tarfile.TarFile(
                        fileobj=img.extractfile('%s/layer.tar' % id)) as layer:
                    try:
                        layer.extractall(path=args.output)
                    except OSError:
                        if not args.ignore_errors:
                            raise


if __name__ == '__main__':
    main()
