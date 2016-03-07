"""
Expand NES ROMs.

See: http://dvdtranslations.eludevisibility.org/rom_expander_pro.html
"""

from .. import util


class ROMExpander:

    FILENAME = "ROM Expander Pro.txt"

    def tokenize_line(self, line):
        """Tokenize a tab-delineated string and return as a list."""
        return line.strip().split('\t')

    def load_script(self, txt=None):
        script = {}
        script["file"] = txt
        with open(script["file"]) as script_file:
            script_lines = script_file.readlines()

        # Load the `NAME` line from script.
        l = self.tokenize_line(script_lines.pop(0))
        assert 'NAME' == l.pop(0)
        script["source"], script["target"] = l
        assert script["target"] != script["source"]

        # Load the `SIZE` and optional `MD5`
        l = self.tokenize_line(script_lines.pop(0))
        script["old_size"] = eval("0x" + l[1])
        script["new_size"] = eval("0x" + l[2])
        if l.index(l[-1]) > 2:
            script["MD5"] = l[3].lower()

        # Load the replacement `HEADER`.
        l = self.tokenize_line(script_lines.pop(0))
        assert 'HEADER' == l.pop(0)
        script["header_size"] = eval("0x" + l.pop(0))
        assert script["header_size"] > len(l)
        # Sanitize and concatenate the header data.
        new_header = "".join(["0" * (2 - len(x)) + x for x in l])
        # Cast to character data and pad with 0x00 to header_size
        new_header = util.bytes_from_str(new_header)
        script["header"] = new_header + "\x00" * (script["header_size"] - len(l))

        script["ops"] = []
        while script_lines:
            script["ops"].append(self.tokenize_line(script_lines.pop(0)))

        script["patches"] = []
        for op in script["ops"]:
            if op[0] == "REPLACE":
                script["patches"].append(op[1:])
                script["ops"].remove(op)

        return script

    def expand_rom(script):
        if "MD5" in script:
            with open(script["source"], "rb") as s_file:
                # Don't digest the header.
                s_file.read(script["header_size"])
                assert script["MD5"] == util.md5_sum(s_file)
                print "MD5... match!"

        print "Expanding..."
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
                    end_ptr = eval("0x" + script["ops"][0][1]) + script["header_size"]

                if cmd == "COPY":
                    copy(eval("0x" + op[1]),  # Source
                         eval("0x" + op[0]))  # Target

                elif cmd == "FILL":
                    fill(eval("0x" + op[0]),  # Destination
                         util.bytes_from_str(op[1]))  # Value
                else:
                    raise Exception

            # REPLACE
            for patch in script["patches"]:
                offset = eval("0x" + patch.pop(0))
                data = "".join(["0" * (2 - len(x)) + x for x in patch])
                t.seek(offset + script['header_size'])
                t.write(util.bytes_from_str(data))
