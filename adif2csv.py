import re
import collections

'''
Class for OrderedSet
'''
class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

'''
Simple class to take adif file - and create csv
'''
class adif2csv(object):
    '''
    expected usage
    import adif2csv
    cvt=adif2csv()
    cvt.process("test.adif")
    for a in cvt.dump():
        print(''+a,end='')
    '''

    def __init__(self):
        '''
        Basic constructor
        :return:  None
        '''
        self.fields=OrderedSet()
        self.lines=[]
        self.header=""

    def process(self, filename):
        '''
        Open the file and store the data internally

        Note: At the moment there is no error checking that this has worked.

        :param filename:
        :return:
        '''

        # extract the lines
        with open(filename, 'rt') as f:
            for line in f:
                if line.startswith("<call"):
                    self.lines.append(line)
            f.close()

        self.extract_all_fields()
        self.make_header()

    def get_fields(line):
        '''
        Extract a list of field from a line like this:
        <call:4>R6DV <qso_date_off:8>20240604 <qso_date:8>20240604
        :return: ['call', 'qso_date_off', 'qso_date']
        '''

        return re.findall(r'<(.*?):.*?>',line)

    def get_dic(self, line):
        '''
        Get dictionnary from a line like this:
        <call:4>R6DV <qso_date_off:8>20240604 <qso_date:8>20240604
        :return: [{call: "R6DV", ...]
        '''

        captures = re.findall(r'<(.*?):.*?>(.*?)\s+(?=<)',line)
        d = dict()
        for capture in captures:
            d[capture[0]] = capture[1]
        return d

    def render_line(self, dict):
        '''
        Render a line into a CSV line
        :param line:
        :return:
        '''
        res = ""
        for index, key in enumerate(self.fields):
            if dict.get(key) is not None:
                s = dict[key]
            else:
                s = ""
            res += s
            if index < len(self.fields):
                    res += ","
        return res

    def extract_all_fields(self, max_lines=0):
        for index, line in enumerate(self.lines):
            if max_lines > 0 and index > max_lines:
                return
            for field in adif2csv.get_fields(line):
                self.fields.add(field)

    def make_header(self):
        '''
        This gnerates the header for the CSV file
        :param all_lines_same:
        :return: set
        '''
        self.header = ",".join(self.fields)

    def dump(self):
        '''
        Simple iterator to allow the converted data to be output
        :return:
        '''
        yield (''+self.header+"\n")
        for line in self.lines:
            d = self.get_dic(line)
            rendered_line = self.render_line(d)
            yield(''+rendered_line+'\n')


if __name__ == "__main__":
    cvt=adif2csv()
    cvt.process("tests/test.adif")

    for a in cvt.dump():
        print(''+a)
