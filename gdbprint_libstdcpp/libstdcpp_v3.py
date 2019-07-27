# Based on pretty-printers for libstdc++.

# Copyright (C) 2008-2018 Free Software Foundation, Inc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gdb
import re
#from dumper import *
from gdbprint.gdbutils import *
from gdbprint.gdbprinters import *
from gdbprint.utils import *


class StdBitsetPrinter(DebugPrinter):
    names = ["std::bitset"]

    @staticmethod
    def display_hint():
        return DisplayType.BITSET

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.words = self.value['_M_w']
        self.wtype = self.words.type
        # The _M_w member can be either an unsigned long, or an
        # array.  This depends on the template specialization used.
        # If it is a single long, convert to a single element list.
        if self.wtype.code == gdb.TYPE_CODE_ARRAY:
            self.tsize = self.wtype.target().sizeof
        else:
            self.words = [self.words]
            self.tsize = self.wtype.sizeof
        self.nwords = self.wtype.sizeof / self.tsize

    def get(self, start, end):
        byte = int(start / (8 * self.tsize))
        bit = start - byte * self.tsize * 8
        if byte >= self.nwords:
            raise StopIteration
        i = start
        result = []
        while byte < self.nwords and i < end:
            w = self.words[byte]
            if bit > 0:
                w = w >> bit
            while w != 0 and i < end:
                if (w & 1) != 0:
                    # Return not-0 bit
                    result.append((i, 1))
                else:
                    # Return 0 bit
                    result.append((i, 0))
                bit += 1
                i += 1
                w = w >> 1
            byte = byte + 1
        return (result, i - 1)


class StdDequePrinter(DebugPrinter):
    names = ["std::deque"]

    @staticmethod
    def display_hint():
        return DisplayType.LIST_SIZED

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.elttype = self.value.type.template_argument(0)
        size = self.elttype.sizeof
        if size < 512:
            self.buffer_size = int(512 / size)
        else:
            self.buffer_size = 1
        self.seek_first()

    def size(self):
        start = self.value['_M_impl']['_M_start']
        end = self.value['_M_impl']['_M_finish']

        delta_n = end['_M_node'] - start['_M_node'] - 1
        delta_s = start['_M_last'] - start['_M_cur']
        delta_e = end['_M_cur'] - end['_M_first']

        return int(self.buffer_size * delta_n + delta_s + delta_e)

    def seek_first(self):
        start = self.value['_M_impl']['_M_start']
        end = self.value['_M_impl']['_M_finish']

        self.node = start['_M_node']
        self.p = start['_M_cur']
        self.end_iter = start['_M_last']
        self.last_iter = end['_M_cur']
        self.pos = 0

    def next(self):
        if self.p == self.last_iter:
            raise StopIteration

        result = (self.pos, self.p.dereference())
        self.pos += 1

        # Advance the 'cur' pointer.
        self.p = self.p + 1
        if self.p == self.end_iter:
            # If we got to the end of this bucket, move to the
            # next bucket.
            self.node = self.node + 1
            self.p = self.node[0]
            self.end_iter = self.p + self.buffer_size

        return result

    def get_pos(self):
        return self.pos


def get_value_from_aligned_membuf(buf, valtype):
    """Returns the value held in a __gnu_cxx::__aligned_membuf."""
    return buf['_M_storage'].address.cast(valtype.pointer()).dereference()


def get_value_from_list_node(node):
    """Returns the value held in an _List_node<_Val>"""
    try:
        member = node.type.fields()[1].name
        if member == '_M_data':
            # C++03 implementation, node contains the value as a member
            return node['_M_data']
        elif member == '_M_storage':
            # C++11 implementation, node stores value in __aligned_membuf
            valtype = node.type.template_argument(0)
            return get_value_from_aligned_membuf(node['_M_storage'], valtype)
    except:
        pass
    raise ValueError("Unsupported implementation for %s" % str(node.type))


class NodeIteratorPrinter:
    def __init__(self, val, typename):
        self.val = val
        self.typename = typename

    def ptr(self):
        itype = self.val.type.template_argument(0)
        nodetype = gdb.lookup_type('std::_List_node<%s>' % itype).pointer()
        elt = self.val['_M_node'].cast(nodetype).dereference()
        return get_value_from_list_node(elt), None


class StdListIteratorPrinter(NodeIteratorPrinter, DebugPrinter):
    "Print std::list::iterator"
    names = ["std::_List_iterator"]

    @staticmethod
    def display_hint():
        return DisplayType.PTR

    def __init__(self, val, typename):
        NodeIteratorPrinter.__init__(self, val, typename)


class StdFwdListIteratorPrinter(NodeIteratorPrinter, DebugPrinter):
    "Print std::forward_list::iterator"
    names = ["std::_Fwd_list_iterator"]

    @staticmethod
    def display_hint():
        return DisplayType.PTR

    def __init__(self, val, typename):
        NodeIteratorPrinter.__init__(self, val, typename)


class StdListPrinter(DebugPrinter):
    names = ["std::list", "std::__cxx11::list"]

    @staticmethod
    def display_hint():
        return DisplayType.LIST

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.nodetype = find_type(self.type,
                                  '_Node').strip_typedefs().pointer()
        self.seek_first()

    def seek_first(self):
        self.head = self.value['_M_impl']['_M_node']
        self.base = self.head['_M_next']
        self.head_addr = self.head.address
        self.pos = 0

    def next(self):
        #print (self.base)
        #print (self.head_addr)
        if self.base == self.head_addr:
            raise StopIteration
        elt = self.base.cast(self.nodetype).dereference()
        self.base = elt['_M_next']
        pos = self.pos
        self.pos += 1
        val = get_value_from_list_node(elt)
        return (pos, val)

    def get_pos(self):
        return self.pos


class StdForwardListPrinter(DebugPrinter):
    names = ["std::forward_list"]

    @staticmethod
    def display_hint():
        return DisplayType.LIST

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.nodetype = find_type(self.type,
                                  '_Node').strip_typedefs().pointer()
        self.seek_first()

    def seek_first(self):
        self.head = self.value['_M_impl']['_M_head']
        self.base = self.head['_M_next']
        self.head_addr = self.head.address
        self.pos = 0

    def next(self):
        #print (self.base)
        #print (self.head_addr)
        if self.base == 0:
            raise StopIteration
        elt = self.base.cast(self.nodetype).dereference()
        self.base = elt['_M_next']
        pos = self.pos
        self.pos += 1
        valptr = elt['_M_storage'].address
        val = valptr.cast(
            elt.type.template_argument(0).pointer()).dereference()
        return (pos, val)

    def get_pos(self):
        return self.pos


class StdStringPrinter(DebugPrinter):
    names = ["std::basic_string", 'std::__cxx11::basic_string']

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        # Make sure &string works, too.
        if self.type.code == gdb.TYPE_CODE_REF:
            self.type = type.target()

        self.new_string = str(type).find("std::__cxx11::basic_string") != -1

        if str(self.ptr().dereference().type) == "wchar_t":
            self.unicode = True
        else:
            self.unicode = False

    @staticmethod
    def display_hint():
        return DisplayType.STRING

    def is_unicode(self):
        return self.unicode

    def size(self):
        # Calculate the length of the string so that to_string returns
        # the string according to length, not according to first null
        # encountered.
        length = None
        capacity = None

        # Calculate the length of the string so that to_string returns
        # the string according to length, not according to first null
        # encountered.
        ptr = self.ptr()
        try:
            if self.new_string:
                length = int(self.value['_M_string_length'])
                capacity = int(self.value['_M_string_capacity'])
            else:
                realtype = self.type.unqualified().strip_typedefs()
                reptype = gdb.lookup_type(str(realtype) + '::_Rep').pointer()
                header = ptr.cast(reptype) - 1
                length = int(header.dereference()['_M_length'])
                capacity = int(header.dereference()['_M_capacity'])

        except:
            #libstdc++6 6.3.0-18
            if length is None: length = int(self.value['_M_string_length'])
            capacity = int(self.value['_M_allocated_capacity'])

        if capacity > 4294967291:
            capacity = length  # Fix for libstdc++6 6.3.0-18, but sometimes this don't work
        return (length, capacity)

    def ptr(self):
        dataplus = self.value['_M_dataplus']
        ptr = dataplus['_M_p']
        if self.new_string:
            # https://sourceware.org/bugzilla/show_bug.cgi?id=17728
            ptr = ptr.cast(ptr.type.strip_typedefs())
        #print("%s" % encode_unicode(ptr))
        return ptr

    def get(self, i):
        return (self.ptr() + i).dereference()

    def string(self):
        (l, c) = self.size()
        if self.unicode:
            #return self.ptr().string()
            return read_unicode(self.ptr(), 0, l)
        else:
            return read_string(self.ptr(), 0, l)

    def substring(self, start, end=-1):
        #print("%d - %d" % (start,  end))
        (l, c) = self.size()
        if end > 0 and end < l:
            l = end
        if self.unicode:
            #return self.ptr().string()
            return read_unicode(self.ptr(), start, l)
        else:
            return read_string(self.ptr(), start, l)


class StdVectorPrinter(DebugPrinter):
    names = ["std::vector"]

    @staticmethod
    def display_hint():
        return DisplayType.ARRAY

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)

    def size(self):
        if self.type.code == gdb.TYPE_CODE_BOOL:
            start = self.value['_M_impl']['_M_start']['_M_p']
            finish = self.value['_M_impl']['_M_finish']['_M_p']
            finish_offset = self.valuej['_M_impl']['_M_finish']['_M_offset']
            end = self.value['_M_impl']['_M_end_of_storage']
            bit_size = start.dereference().type.sizeof * 8
            len = (finish - start) * bit_size + finish_offset
            capacity = (end - start) * bit_size
            return (len, capacity)
        else:
            len = int(self.value['_M_impl']['_M_finish'] -
                      self.value['_M_impl']['_M_start'])
            capacity = int(self.value['_M_impl']['_M_end_of_storage'] -
                           self.value['_M_impl']['_M_start'])
            return (len, capacity)

    def get(self, index):
        if self.type.code == gdb.TYPE_CODE_BOOL:
            start = self.value['_M_impl']['_M_start']['_M_p']
            bit_size = start.dereference().type.sizeof * 8
            valp = start + index // bit_size
            offset = index % bit_size
            return (valp.dereference() & (1 << offset)) > 0
        else:
            return self.value['_M_impl']['_M_start'][index]


class StdArrayPrinter(DebugPrinter):
    names = ["std::array"]

    @staticmethod
    def display_hint():
        return DisplayType.ARRAY

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)

    def array(self):
        return self.value['_M_elems']

    def size(self):
        nvalue = self.array()
        size = nvalue.type.sizeof
        if size == 0:
            len = 0
        else:
            target = nvalue[0]
            len = nvalue.type.sizeof / target.type.sizeof
        return (len, len)

    def get(self, index):
        return self.array()[index]


class StdTuplePrinter(DebugPrinter):
    names = ["std::tuple"]

    @staticmethod
    def display_hint():
        return DisplayType.STRUCT

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.seek_first()

    def seek_first(self):
        self.head = self.value
        # Set the base class as the initial head of the
        # tuple.
        nodes = self.head.type.fields()
        if len(nodes) == 1:
            # Set the actual head to the first pair.
            self.head = self.head.cast(nodes[0].type)
        elif len(nodes) != 0:
            raise ValueError(
                "Top of tuple tree does not consist of a single node.")
        self.pos = 0

    def next(self):
        # Check for further recursions in the inheritance tree.
        # For a GCC 5+ tuple self.head is None after visiting all nodes:
        if self.head is None:
            raise StopIteration
        nodes = self.head.type.fields()
        # For a GCC 4.x tuple there is a final node with no fields:
        if len(nodes) == 0:
            self.head = None
            raise StopIteration
        # Check that this iteration has an expected structure.
        if len(nodes) > 2:
            raise ValueError("Cannot parse more than 2 nodes in a tuple tree.")

        if len(nodes) == 1:
            # This is the last node of a GCC 5+ std::tuple.
            impl = self.head.cast(nodes[0].type)
            self.head = None
        else:
            # Either a node before the last node, or the last node of
            # a GCC 4.x tuple (which has an empty parent).

            # - Left node is the next recursion parent.
            # - Right node is the actual class contained in the tuple.

            # Process right node.
            impl = self.head.cast(nodes[1].type)

            # Process left node and set it as head.
            self.head = self.head.cast(nodes[0].type)

        self.pos += 1

        # Finally, check the implementation.  If it is
        # wrapped in _M_head_impl return that, otherwise return
        # the value "as is".
        fields = impl.type.fields()

        if len(fields) < 1 or fields[0].name != "_M_head_impl":
            return (self.pos, impl)
        else:
            return (self.pos, impl['_M_head_impl'])


class RbtreeIterator:
    """
    Turn an RB-tree-based container (std::map, std::set etc.) into
    a Python iterable object.
    """

    def __init__(self, rbtree):
        self.size = rbtree['_M_t']['_M_impl']['_M_node_count']
        self.node = rbtree['_M_t']['_M_impl']['_M_header']['_M_left']
        self.pos = 0

    def __iter__(self):
        return self

    def __len__(self):
        return int(self.size)

    def __next__(self):
        if self.pos == self.size:
            raise StopIteration
        result = self.node
        self.pos += 1
        if self.pos < self.size:
            # Compute the next node.
            node = self.node
            if node.dereference()['_M_right']:
                node = node.dereference()['_M_right']
                while node.dereference()['_M_left']:
                    node = node.dereference()['_M_left']
            else:
                parent = node.dereference()['_M_parent']
                while node == parent.dereference()['_M_right']:
                    node = parent
                    parent = parent.dereference()['_M_parent']
                if node.dereference()['_M_right'] != parent:
                    node = parent
            self.node = node
        return result


def get_value_from_Rb_tree_node(node):
    """Returns the value held in an _Rb_tree_node<_Val>"""
    try:
        member = node.type.fields()[1].name
        if member == '_M_value_field':
            # C++03 implementation, node contains the value as a member
            return node['_M_value_field']
        elif member == '_M_storage':
            # C++11 implementation, node stores value in __aligned_membuf
            valtype = node.type.template_argument(0)
            return get_value_from_aligned_membuf(node['_M_storage'], valtype)
    except:
        pass
    raise ValueError("Unsupported implementation for %s" % str(node.type))


class StdMapPrinter(DebugPrinter):
    names = ["std::map", "std::multimap"]

    @staticmethod
    def display_hint():
        return DisplayType.MAP

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        rep_type = find_type(self.type, '_Rep_type')
        self.node_type = find_type(rep_type, '_Link_type').strip_typedefs()
        self.seek_first()

    def seek_first(self):
        self.rbiter = RbtreeIterator(self.value)
        self.pos = 0

    def next(self):
        n = self.rbiter.__next__()
        n = n.cast(self.node_type).dereference()
        n = get_value_from_Rb_tree_node(n)
        self.pair = n
        key = n['first']
        item = self.pair['second']
        self.pos += 1
        result = (key, item)

        return result

    def size(self):
        return len(self.rbiter)

    def get_pos(self):
        return self.pos


class StdSetPrinter(DebugPrinter):
    names = ["std::set", "std::multiset"]

    @staticmethod
    def display_hint():
        return DisplayType.SET

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        rep_type = find_type(self.type, '_Rep_type')
        self.node_type = find_type(rep_type, '_Link_type').strip_typedefs()
        self.seek_first()

    def seek_first(self):
        self.rbiter = RbtreeIterator(self.value)
        self.pos = 0

    def next(self):
        n = self.rbiter.__next__()
        n = n.cast(self.node_type).dereference()
        n = get_value_from_Rb_tree_node(n)
        i = self.pos
        self.pos += 1

        return n

    def size(self):
        return len(self.rbiter)

    def get_pos(self):
        return self.pos


class StdAutoPointerPrinter(DebugPrinter):
    names = ["std::auto_ptr"]

    @staticmethod
    def display_hint():
        return DisplayType.PTR

    def ptr(self):
        #print(self.type.fields()[0].type)
        v = self.value['_M_ptr']
        return (v, None)


def is_specialization_of(type, template_name):
    return re.match('^std::([0-9]+::)?%s<.*>$' % template_name,
                    type) is not None


class StdUniquePointerPrinter(DebugPrinter):
    names = ["std::unique_ptr"]

    @staticmethod
    def display_hint():
        return DisplayType.PTR

    def ptr(self):
        #print(self.type.fields()[0].type)
        impl_type = str(self.type.fields()[0].type)
        if impl_type.endswith('::__tuple_type'):
            v = self.value['_M_t']['_M_head_impl']
        elif is_specialization_of(impl_type,
                                  '__uniq_ptr_impl'):  # New implementation
            v = self.value['_M_t']['_M_t']['_M_head_impl']
        else:
            raise ValueError("Unsupported implementation for unique_ptr: %s" %
                             self.value.type.fields()[0].type.tag)
        return (v, None)


class StdSharedPointerPrinter(DebugPrinter):
    names = ["std::shared_ptr", "std::weak_ptr"]

    @staticmethod
    def display_hint():
        return DisplayType.PTR

    def ptr(self):
        state = 'empty'
        refcounts = self.value['_M_refcount']['_M_pi']
        if refcounts != 0:
            usecount = refcounts['_M_use_count']
            weakcount = refcounts['_M_weak_count']
            if usecount == 0:
                state = 'expired, weak %d' % weakcount
            else:
                state = 'count %d, weak %d' % (usecount, weakcount - 1)
        return (self.value['_M_ptr'], state)


class StdStackPrinter(SubTypePrinter):
    names = ["std::stack"]
    fields = {"c"}


class Tr1HashtableIterator:
    def __init__(self, hash):
        self.buckets = hash['_M_buckets']
        self.bucket = 0
        self.bucket_count = hash['_M_bucket_count']
        self.node_type = find_type(hash.type, '_Node').pointer()
        self.node = 0
        while self.bucket != self.bucket_count:
            self.node = self.buckets[self.bucket]
            if self.node:
                break
            self.bucket = self.bucket + 1

    def __next__(self):
        if self.node == 0:
            raise StopIteration
        node = self.node.cast(self.node_type)
        result = node.dereference()['_M_v']
        self.node = node.dereference()['_M_next']
        if self.node == 0:
            self.bucket = self.bucket + 1
            while self.bucket != self.bucket_count:
                self.node = self.buckets[self.bucket]
                if self.node:
                    break
                self.bucket = self.bucket + 1
        return result


class StdHashtableIterator:
    def __init__(self, hash):
        self.vers = 0
        try:
            # gcc 4.9 libstdc++
            self.node = hash['_M_before_begin']['_M_nxt']
        except:
            # gcc 4.8 or 4.8 libstdc++ or libc++
            self.vers = 8
            self.node = hash['_M_bbegin']['_M_node']['_M_nxt']
        self.node_type = find_type(hash.type, '__node_type').pointer()

    def __next__(self):
        if self.node == 0:
            raise StopIteration
        if self.vers == 8:
            node = self.node.cast(self.node_type)
            result = node.dereference()['_M_v']
            self.node = node.dereference()['_M_nxt']
            return result
        else:
            elt = self.node.cast(self.node_type).dereference()
            self.node = elt['_M_nxt']
            valptr = elt['_M_storage'].address
            valptr = valptr.cast(elt.type.template_argument(0).pointer())
            return valptr.dereference()


class StdUnorderedMapPrinter(DebugPrinter):
    names = ["std::unordered_map", "std::tr1::unordered_map"]

    @staticmethod
    def display_hint():
        return DisplayType.MAP

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.seek_first()

    def size(self):
        return int(self.hashtable['_M_element_count'])

    def seek_first(self):
        self.pos = 0
        if str(self.type).startswith('std::tr1'):
            self.hashtable = self.value
            self.iter = Tr1HashtableIterator(self.hashtable)
        else:
            self.hashtable = self.value['_M_h']
            self.iter = StdHashtableIterator(self.hashtable)

    def next(self):
        n = self.iter.__next__()
        self.pos += 1

        key = n['first']
        item = n['second']
        result = (key, item)

        return result

    def get_pos(self):
        return self.pos


class StdUnorderedSetPrinter(DebugPrinter):
    names = ["std::unordered_set", "std::tr1::unordered_set"]

    @staticmethod
    def display_hint():
        return DisplayType.SET

    def __init__(self, value, type, **kwargs):
        DebugPrinter.__init__(self, value, type)
        self.seek_first()

    def size(self):
        return int(self.hashtable['_M_element_count'])

    def seek_first(self):
        self.pos = 0
        if str(self.type).startswith('std::tr1'):
            self.hashtable = self.value
            self.iter = Tr1HashtableIterator(self.hashtable)
        else:
            self.hashtable = self.value['_M_h']
            self.iter = StdHashtableIterator(self.hashtable)

    def next(self):
        n = self.iter.__next__()
        self.pos += 1
        return n

    def get_pos(self):
        return self.pos


libstdcpp_v3_printers = [
    StdArrayPrinter,
    StdBitsetPrinter,
    StdDequePrinter,
    StdListIteratorPrinter,
    StdListPrinter,
    StdFwdListIteratorPrinter,
    StdForwardListPrinter,
    StdMapPrinter,
    StdSetPrinter,
    StdStringPrinter,
    StdTuplePrinter,
    StdVectorPrinter,
    StdAutoPointerPrinter,
    StdUniquePointerPrinter,
    StdSharedPointerPrinter,
    StdStackPrinter,
    StdUnorderedMapPrinter,
    StdUnorderedSetPrinter,
]


def register():
    for p in libstdcpp_v3_printers:
        #print(p)
        register_printer(p)
