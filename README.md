Unpacks a Docker image.

## Usage

    usage: undocker.py [-h] [--ignore-errors] [--output OUTPUT] [--verbose]
                       [--debug] [--list] [--layer LAYER]
                       image

    positional arguments:
      image

    optional arguments:
      -h, --help            show this help message and exit
      --ignore-errors, -i   Ignore OS errors when extracting files
      --output OUTPUT, -o OUTPUT
                            Output directory (defaults to ".")
      --verbose, -v
      --debug, -d
      --list, --ls          List layers in an image
      --layer LAYER, -l LAYER
                            Extract only the specified layer

## Examples

Extract an entire image:

    $ docker save busybox | undocker -i -o busybox busybox

The `-i` option is necessary here because I am not running as root,
and the extract operation will fail when it attempts to create device
nodes.

List the layers in an image:

    $ docker save busybox | undocker --list
    511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158
    df7546f9f060a2268024c8a230d8639878585defcc1bc6f79d2728a13957871b
    ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2
    4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125

Extract only specific layers:

    $ docker save busybox |
      undocker -o busybox -v \
      -l 4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125 \
      busybox
    INFO:undocker:extracting image busybox (4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125)
    INFO:undocker:extracting layer 4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125

## License

undocker -- a tool for decomposing Docker images  
Copyright (C) 2015 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

