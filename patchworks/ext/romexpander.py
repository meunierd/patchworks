"""
Expand NES ROMs.

See: http://dvdtranslations.eludevisibility.org/rom_expander_pro.html
"""

import binascii

from patchworks import util


class ROMExpander:

    FILENAME = "ROM Expander Pro.txt"

    def __init__(self, fp):
        self.lines = fp.readlines()

    def parse_metadata(self):
        self.parse_name()
        self.parse_file_metadata()

    def parse_header(self):
        line = self.readline()
        assert line.pop(0) == 'HEADER'
        self.header_size = self.parse_int(line.pop(0))
        self.header_data = self.parse_bytes(line)

    def parse_file_sizes_and_checksum(self):
        line = self.readline()
        assert line.pop(0) == 'SIZE'
        self.source_size = self.parse_int(line.pop(0))
        self.modified_size = self.parse_int(line.pop(0))
        if line:
            self.source_checksum = line.pop(0).lower()

    def parse_filenames(self):
        line = self.readline()
        assert line.pop(0) == 'NAME'
        self.source_name, self.modified_name = line

    def parse_bytes(self, byte_list):
        return self._unhexlify("".join(map(self._leftpad, byte_list)))

    def parse_int(self, hex_string):
        return util.int_from_bytes(self._unhexlify(hex_string), endian='big')

    def readline(self):
        return self._tokenize(self.lines.pop(0))

    def _tokenize(self, line):
        return line.strip().split('\t')

    def _unhexlify(self, hex_string):
        return binascii.unhexlify(self._leftpad(hex_string))

    # def load_script(self, txt=None):
    #     script["ops"] = []
    #     while script_lines:
    #         script["ops"].append(self._tokenize(script_lines.pop(0)))

    #     script["patches"] = []
    #     for op in script["ops"]:
    #         if op[0] == "REPLACE":
    #             script["patches"].append(op[1:])
    #             script["ops"].remove(op)

    #     return script

    def expand_rom(script):
        if "MD5" in script:
            with open(script["source"], "rb") as s_file:
                # Don't digest the header.
                s_file.read(script["header_size"])
                assert script["MD5"] == util.md5_sum(s_file)
                print("MD5... match!")

        print("Expanding...")
        with open(script["source"], "rb") as s, open(script["target"], "wb") as t:
            def copy(s_offset, t_offset):
                source_ptr = script["header_size"] + s_offset
                write_ptr = script["header_size"] + t_offset
                s.seek(source_ptr)
                t.seek(write_ptr)
                t.write(s.read(end_ptr - write_ptr))

            def fill(destination, value):
                write_ptr = script["header_size"] + destination
                t.seek(write_ptr)
                t.write(value * (end_ptr - write_ptr))

            t.write(script["header"])

            while script["ops"]:
                op = script["ops"].pop(0)
                cmd = op.pop(0)

                if not script["ops"]:
                    end_ptr = script["header_size"] + script["new_size"]
                else:
                    end_ptr = util.bytes_from_str(script["ops"][0][1]) + script["header_size"]

                if cmd == "COPY":
                    copy(util.bytes_from_str(op[1]),  # Source
                         util.bytes_from_str(op[0]))  # Target

                elif cmd == "FILL":
                    fill(util.bytes_from_str(op[0]),  # Destination
                         util.bytes_from_str(op[1]))  # Value
                else:
                    raise Exception

            # REPLACE
            for patch in script["patches"]:
                offset, data = map(util.bytes_from_str, patch)
                t.seek(offset + script['header_size'])
                t.write(util.bytes_from_str(data))
