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

import argparse
from pathlib import Path
from shutil import copy2


class DiffPatcher:
    def __init__(self, data_dict):
        self.data = data_dict
        self.check_files()

    def check_files(self):
        self.data['sfp'] = Path(self.data['source_file_path'])
        self.data['dfp'] = Path(self.data['dest_file_path'])
        self.data['pfp'] = Path(self.data['patch_file_path'])

        assert self.data['sfp'].is_file(), 'Source file is not a file'
        dfp_is_file = self.data['dfp'].is_file()
        pfp_is_file = self.data['pfp'].is_file()

        if self.data['patch_mode']:
            if dfp_is_file:
                print('Warning: Destination file exists and will be overwritten!')
            assert pfp_is_file, 'Patch file is not a file'
        else:
            assert dfp_is_file, 'Destination file is not a file'
            if pfp_is_file:
                print('Warning: Patch file exists and will be overwritten!')
            if self.data['sfp'].stat().st_size != self.data['dfp'].stat().st_size:
                print('Warning: Source and destination file sizes do not match. Output may be incorrect.')

    def diff(self):
        b_len = self.data['diff_bytes']

        with open(self.data['sfp'], 'rb') as source_file, \
                open(self.data['dfp'], 'rb') as dest_file, \
                open(self.data['pfp'], 'w') as patch_file:
            source_byte = source_file.read(b_len)
            dest_byte = dest_file.read(b_len)
            while source_byte:
                if source_byte != dest_byte:
                    source_offset = source_file.tell() - b_len + 1
                    patch_file.write(f"{source_offset:#x} {source_byte.hex()} {dest_byte.hex()}\n")

                source_byte = source_file.read(b_len)
                dest_byte = dest_file.read(b_len)

    def patch(self):
        copy2(self.data['sfp'], self.data['dfp'])

        with open(self.data['dfp'], 'rb+') as dest_file, \
                open(self.data['pfp'], 'r') as patch_file:
            patch_line = patch_file.readline()
            while patch_line:
                # ignore comments
                if not patch_line.startswith('#'):
                    patch = patch_line.rstrip().split(" ")
                    dest_file.seek(int(patch[0], 16) - 1)
                    # calculate how many bytes to patch at once
                    b_len = len(patch[1]) // 2
                    dest_byte = dest_file.read(b_len)
                    if dest_byte == bytes.fromhex(patch[1]):
                        dest_file.seek(-b_len, 1)
                        dest_file.write(bytes.fromhex(patch[2]))

                patch_line = patch_file.readline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a human-readable binary patch file.')
    parser.add_argument('-p', '--patch_mode', help='patch mode', action='store_true')
    parser.add_argument(
        '-b',
        '--diff_bytes',
        help='size of one diff in bytes (default: 1)',
        action='store',
        default=1,
        type=int)
    parser.add_argument('source_file_path', help='Path for the source file', action='store', type=str)
    parser.add_argument('dest_file_path', help='Path for the destination file', action='store', type=str)
    parser.add_argument('patch_file_path', help='Path for the patch file', action='store', type=str)
    args = vars(parser.parse_args())

    dp = DiffPatcher(args)
    if args['patch_mode']:
        dp.patch()
    else:
        dp.diff()
