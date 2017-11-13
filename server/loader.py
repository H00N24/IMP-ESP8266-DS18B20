"""File with Loader class

Author:
    Ondrej Kurak
"""
import re
from os import path as ph
from hashlib import sha1


class Loader():
    """Class

    Class for loading file with known devices.
    Also for command line parsing and adding new
    devices to the known list.

    Attributes:
        known (set): known devices
        macs (set): known MAC addresses
    """

    def __init__(self):
        self.known = set()
        self.macs = set()
        self.main_dir = ph.dirname(ph.abspath(__file__))
        self.regex = "<!--NEW ENTRY-->"

    def load_known(self):
        """Loading file with known devices
        """
        with open(self.main_dir + '/known.conf') as inp:
            for line in inp:
                if line[:-1]:
                    tmp = tuple(line[:-1].split(';'))
                    self.known.add(tmp)
                    self.macs.add(tmp[1])

    def add_to_known(self, name, mac, pasw):
        """Adding file to known devices

        Args:
            name (str): device name
            mac (str): device MAC address
            pasw (str): password for device
        """
        h_p = sha1(pasw.encode('utf-8')).hexdigest()
        if mac in self.macs:
            print("Device not added!")
            return False
        with open(self.main_dir + '/known.conf', 'a') as out:
            out.write(';'.join([name, mac, h_p]))
            out.write('\n')

        self.load_known()
        print("Device added!")
        return True

    def proc_line(self, line):
        """Command line parsing

        Command line processing for adding new devices
        to the known list and index.html file and creating
        history file.

        Args:
            line (str): command line text
        """
        tmp = line[:-1].split()
        if len(tmp) != 3:
            return False

        if not ld.add_to_known(tmp[0], tmp[1], tmp[2]):
            return False

        with open(main_dir + '/index.html') as inp:
            text = inp.read()

            hist = '/history/{0}.html'.format(tmp[1].replace(':', '-'))
            repl = ('<tr>\n<td>{0}</td>\n'
                    '<td>{1}</td><td>-</td><td>-</td><td>-</td><!--{1}-->\n'
                    '<td><a href={2}>History</a></td>').format(tmp[0], tmp[1], hist)
            new_text = re.sub(self.regex, repl + '\n</tr>\n' + self.regex, text)
            with open(self.main_dir + '/index.html', 'w') as out:
                out.write(new_text)

            with open(self.main_dir + '/pattern.html') as inp:
                text = inp.read()

            new_text = re.sub('<!--NAME MAC-->', ' '.join([tmp[0], tmp[1]]), text)
            with open(self.main_dir + hist, 'w') as out:
                out.write(new_text)
