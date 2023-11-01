#!/usr/bin/env python3

"""
    Applies a human-readable binary patch file.
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
import shutil

source_file_path = sys.argv[1]
patch_file_path = sys.argv[2]
dest_file_path = sys.argv[3]

shutil.copy2(source_file_path, dest_file_path)

with open(dest_file_path, 'rb+') as dest_file, \
        open(patch_file_path, 'r') as patch_file:
    patch_line = patch_file.readline()
    while patch_line:
        patch = patch_line.rstrip().split(" ")
        dest_file.seek(int(patch[0], 16) - 1)
        dest_byte = dest_file.read(1)
        if dest_byte == bytes.fromhex(patch[1]):
            dest_file.seek(-1, 1)
            dest_file.write(bytes.fromhex(patch[2]))

        patch_line = patch_file.readline()
