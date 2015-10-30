#!/usr/bin/env python
# vim:fileencoding=utf-8

import struct


class IdxHeader(object):
    HEADER_UNPACK_TYPE = "i"
    DATA_FORMAT_TABLE = {
        8:  "B",  # unsigned char
        9:  "b",  # signed char
        11: "h",  # short
        12: "i",  # int
        13: "f",  # float
        14: "d"   # double
        }   # default value => "x"  # pad byte

    DATA_SIZE_TABLE = {
        8:  1,  # unsigned char
        9:  1,  # signed char
        11: 2,  # short
        12: 4,  # int
        13: 4,  # float
        14: 8   # double
        }   # default value => 1  # pad byte

    def __init__(self, file_path):
        with open(file_path, "rb") as fp:
            # parse magic number
            self.magic_number_bytes = struct.unpack(">bbbb", fp.read(4))

            # get info from magic number
            self.body_unpack_type = (IdxHeader.DATA_FORMAT_TABLE.
                                     get(self.magic_number_bytes[2], "x"))
            self.body_type_size = (IdxHeader.DATA_SIZE_TABLE.
                                   get(self.magic_number_bytes[2], 1))
            self.dim = self.magic_number_bytes[3]

            # parse header using magic number info
            self.shape = struct.unpack((">{0}{1}"
                                        .format(self.dim,
                                                IdxHeader.HEADER_UNPACK_TYPE)),
                                       fp.read(self.dim * 4))

    def __str__(self):
        return "{0} {1} {2}".format(self.body_unpack_type,
                                    self.dim,
                                    self.shape)


class IdxBody(object):
    def __init__(self, file_path, idx_header):
        with open(file_path) as fp:
            fp.read(4 + (idx_header.dim * 4))  # offset

            self.set_nelem_(idx_header)
            self.set_nbyte_(idx_header)
            self.parse_(fp, idx_header)

    def set_nelem_(self, idx_header):
        self.nelem = idx_header.shape[0]

    def set_nbyte_(self, idx_header):
        self.nbyte_ = idx_header.body_type_size
        for i in range(1, idx_header.dim):
            self.nbyte_ *= idx_header.shape[i]

    def parse_(self, fp, idx_header):
        self.elems = []

        for i in range(self.nelem):
            self.elems.append(self.get_elem_(fp, idx_header))

    def get_elem_(self, fp, idx_header):
        return struct.unpack(">{0}{1}".format(self.nbyte_,
                                              idx_header.body_unpack_type),
                             fp.read(self.nbyte_))

    def __str__(self):
        return "{0} {1}".format(self.nbyte_, self.elems[2])


class IdxFileParser(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.header = IdxHeader(self.file_path)
        self.body = IdxBody(self.file_path, self.header)

        self.length = self.body.nelem

    def item(self, i):
        return self.body.elems[i]

    def __getitem__(self, i):
        return self.body.elems[i]

    def to_ndary(self):
        import numpy
        return numpy.array(self.body.elems).reshape(self.header.shape)

    def print_info(self):
        print self.header
        print self.body
