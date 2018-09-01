from . import PatchFile


class ByuuFile(PatchFile):

    def parse_int(self):
        """
        uint64_t data = 0, shift = 1;
        while(true) {
          uint8_t x = read();
          data += (x & 0x7f) * shift;
          if(x & 0x80) break;
          shift <<= 7;
          data += shift;
        }
        return data;
        """
