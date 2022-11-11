#!/usr/bin/env python

from __future__ import print_function

import argparse
import errno
import io
import json
import logging
import os
import shutil
import sys
try:
    from stat import filemode
except ImportError:
    def filemode(mode): return "(0o%06o)" % mode
import tarfile
import tempfile
import time

from contextlib import closing


LOG = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--ignore-errors', '-i',
                   action='store_true',
                   help='Ignore OS errors when extracting files')
    p.add_argument('--output', '-o',
                   default='.',
                   help='Output directory (defaults to ".")')
    p.add_argument('--layers',
                   action='store_true',
                   help='List layers in an image')
    p.add_argument('--list', '--ls',
                   action='store_true',
                   help='List images/tags contained in archive')
    p.add_argument('--du',
                   action='store_true',
                   help='Show disk usage of files')
    p.add_argument('--files',
                   action='store_true',
                   help='List all files in an image')
    p.add_argument('--layer', '-l',
                   action='append',
                   help='Extract only the specified layer')
    p.add_argument('--no-whiteouts', '-W',
                   action='store_true',
                   help='Do not process whiteout (.wh.*) files')

    g = p.add_argument_group('Logging options')
    g.add_argument('--verbose', '-v',
                   action='store_const',
                   const=logging.INFO,
                   dest='loglevel')
    g.add_argument('--debug', '-d',
                   action='store_const',
                   const=logging.DEBUG,
                   dest='loglevel')

    p.add_argument('image', nargs='?')

    p.set_defaults(level=logging.WARN)
    return p.parse_args()


def find_layers(img, id):
    with closing(img.extractfile('%s/json' % id)) as fd:
        # This is an ugly hack for Python 2.
        if not hasattr(fd, 'readable'):
            fd.readable = lambda: True
            fd.seekable = lambda: True
            fd.writable = lambda: False
        info = json.load(io.TextIOWrapper(fd, encoding='utf-8'))

    LOG.debug('layer = %s', id)
    for k in ['os', 'architecture', 'author', 'created']:
        if k in info:
            LOG.debug('%s = %s', k, info[k])

    yield id
    if 'parent' in info:
        pid = info['parent']
        for layer in find_layers(img, pid):
            yield layer


def parse_image_spec(image):
    try:
        path, base = image.rsplit('/', 1)
    except ValueError:
        path, base = None, image
    try:
        name, tag = base.rsplit(':', 1)
    except ValueError:
        name, tag = base, 'latest'
    name = path + '/' + name if path else name
    return name, tag

def du(members):
    for tarinfo in members:
        if tarinfo.isdir() or tarinfo.isdev():
            continue
        if tarinfo.issym() or tarinfo.islnk():
            continue
        if tarinfo.size < 4096:
            size = 4
        else:
            size = tarinfo.size / 1024
        print("%d\t%s" % (size, tarinfo.name))

def ls(members, verbose=True):
    for tarinfo in members:
        if verbose:
            print(filemode(tarinfo.mode), end=" ")
            print("%s/%s" % (tarinfo.uname or tarinfo.uid,
                             tarinfo.gname or tarinfo.gid), end=" ")
            if tarinfo.ischr() or tarinfo.isblk():
                print("%10s" % (
                      "%d,%d" % (tarinfo.devmajor, tarinfo.devminor)), end=" ")
            else:
                print("%10d" % tarinfo.size, end=" ")
            print("%d-%02d-%02d %02d:%02d:%02d"
                  % time.localtime(tarinfo.mtime)[:6], end=" ")

        print(tarinfo.name + ("/" if tarinfo.isdir() else ""), end="")

        if verbose:
            if tarinfo.issym():
                print(" -> " + tarinfo.linkname, end="")
            if tarinfo.islnk():
                print(" link to " + tarinfo.linkname, end="")
        print()

def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    with tempfile.NamedTemporaryFile() as fd, (
            open(args.image, 'rb') if args.image
            else io.open(sys.stdin.fileno(), 'rb')) as image:
        while True:
            data = image.read(8192)
            if not data:
                break
            fd.write(data)
        fd.seek(0)
        with tarfile.TarFile(fileobj=fd) as img:
            repos = img.extractfile('repositories')
            repos = json.loads(repos.read().decode('utf-8'))

            if args.list:
                for name, tags in repos.items():
                    print('%s: %s' % (
                        name,
                        ' '.join(tags)))
                sys.exit(0)

            if args.image:
                name, tag = parse_image_spec(args.image)
            elif len(repos) == 1:
                name = list(repos.keys())[0]
                tag = list(repos[name].keys())[0]
            else:
                LOG.error('No image name specified and multiple '
                          'images contained in archive')
                sys.exit(1)

            try:
                top = repos[name][tag]
            except KeyError:
                LOG.error('failed to find image %s with tag %s',
                          name,
                          tag)
                sys.exit(1)

            LOG.info('extracting image %s (%s)', name, top)
            layers = list(find_layers(img, top))

            if args.layers:
                print('\n'.join(reversed(layers)))
                sys.exit(0)

            if args.du or args.files:
                members = {}
                order = {}
                o = 0
                for id in reversed(layers):
                    if args.layer and id not in args.layer:
                        continue

                    LOG.info('extracting layer %s', id)
                    with tarfile.TarFile(
                            fileobj=img.extractfile('%s/layer.tar' % id),
                            errorlevel=(0 if args.ignore_errors else 1)) as layer:
                        if not args.no_whiteouts:
                            LOG.info('processing whiteouts')
                            for member in layer.getmembers():
                                path = member.path
                                if path.startswith('.wh.') or '/.wh.' in path:
                                    if path.startswith('.wh.'):
                                        newpath = path[4:]
                                    else:
                                        newpath = path.replace('/.wh.', '/')
                                    del members[path]
                                    del members[newpath]
                                else:
                                    members[path] = member
                                    order[path] = o
                                    o += 1
                        else:
                            for member in layer.getmembers():
                                members[member.path] = member
                                order[path] = o
                                o += 1
                s = []
                for member in members:
                    s.append((order[member], members[member]))
                s.sort()
                m = []
                for t in s:
                    m.append(t[1])
                if args.du:
                    du(m)
                else:
                    ls(m)
                sys.exit(0)

            if not os.path.isdir(args.output):
                os.mkdir(args.output)

            for id in reversed(layers):
                if args.layer and id not in args.layer:
                    continue

                LOG.info('extracting layer %s', id)
                with tarfile.TarFile(
                        fileobj=img.extractfile('%s/layer.tar' % id),
                        errorlevel=(0 if args.ignore_errors else 1)) as layer:
                    layer.extractall(path=args.output)
                    if not args.no_whiteouts:
                        LOG.info('processing whiteouts')
                        for member in layer.getmembers():
                            path = os.path.join(args.output, member.path)
                            if path.startswith('.wh.') or '/.wh.' in path:
                                if path.startswith('.wh.'):
                                    newpath = path[4:]
                                else:
                                    newpath = path.replace('/.wh.', '/')

                                try:
                                    LOG.info('removing path %s', newpath)
                                    os.unlink(path)

                                    if os.path.isdir(newpath) and not os.path.islink(newpath):
                                        shutil.rmtree(newpath)
                                    else:
                                        os.unlink(newpath)
                                except OSError as err:
                                    if err.errno != errno.ENOENT:
                                        raise


if __name__ == '__main__':
    main()
