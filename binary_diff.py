#!/usr/bin/env python3

"""
    Creates a human-readable binary patch file.
    Copyright (C) 2023  nghfp9wa7bzq@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys

source_file_path = sys.argv[1]
dest_file_path = sys.argv[2]
patch_file_path = sys.argv[3]

with open(source_file_path, 'rb') as source_file, \
        open(dest_file_path, 'rb') as dest_file, \
        open(patch_file_path, 'w') as patch_file:
    source_byte = source_file.read(1)
    dest_byte = dest_file.read(1)
    while source_byte:
        if source_byte != dest_byte:
            source_offset = source_file.tell()
            patch_file.write(f"{source_offset:#x} {source_byte.hex()} {dest_byte.hex()}\n")

        source_byte = source_file.read(1)
        dest_byte = dest_file.read(1)
