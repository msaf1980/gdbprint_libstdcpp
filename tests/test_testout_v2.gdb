(gdb) file test
(gdb) py sys.path.insert(0, '..')
(gdb) py import gdbprint
load gdbprint
(gdb) py import gdbprint_libstdcpp
load gdbprint_libstdcpp 0.1.1
(gdb) break 135
(gdb) run
Breakpoint: file test.cpp, line 135.

Breakpoint 1, main at test.cpp:135

(gdb) p_s verbose 2
(gdb) p_s w 0
(gdb) p_v cppwstr
"cppwstr" = (std::basic_string<wchar_t, ..>) <0xHEX> str_len:30 capacity:N { [0:29] = L"Василий Пупкин, Vasiliy Pupkin" }
(gdb) p_v cppwstr [ 0:10, 15 ]
"cppwstr" = (std::basic_string<wchar_t, ..>) <0xHEX> str_len:30 capacity:N {
     { [0:10] = L"Василий Пуп" },
     { [15] = L" " },
}
(gdb) p_v cppstr<utf8>
"cppstr" = (std::basic_string<char, ..>) <0xHEX> str_len:42 capacity:N { [0:41] = utf-8:"Василий Пупкин Vasiliy Pupkin" }
(gdb) p_v cppstr<arr,utf8> [ 0:10, 15 ]
"cppstr" = (std::basic_string<char, ..>) <0xHEX> str_len:42 capacity:N {
    [0] = 208 "Р",
    [1] = 146 "’" utf-8:"В",
    [2] = 208 "Р",
    [3] = 176 "°" utf-8:"а",
    [4] = 209 "С",
    [5] = 129 "Ѓ" utf-8:"с",
    [6] = 208 "Р",
    [7] = 184 "ё" utf-8:"и",
    [8] = 208 "Р",
    [9] = 187 "»" utf-8:"л",
    [10] = 208 "Р",
    [15] = 208 "Р",
}
(gdb) p_v cppstr1251
"cppstr1251" = (std::basic_string<char, ..>) <0xHEX> str_len:15 capacity:N { [0:14] = "Василий Vasiliy" }
(gdb) p_v cppstr1251<arr> [ 0:10, 15 ]
"cppstr1251" = (std::basic_string<char, ..>) <0xHEX> str_len:15 capacity:N {
    [0] = 194 "В",
    [1] = 224 "а",
    [2] = 241 "с",
    [3] = 232 "и",
    [4] = 235 "л",
    [5] = 232 "и",
    [6] = 233 "й",
    [7] = 32 " ",
    [8] = 86 "V",
    [9] = 97 "a",
    [10] = 115 "s",
}
(gdb) p_v tuple1
"tuple1" = (std::tuple<int, char>) <0xHEX> {
    [1] = (int) 10,
    [2] = (char) 120 "x",
}
(gdb) p_v tuple1
"tuple1" = (std::tuple<int, char>) <0xHEX> {
    [1] = (int) 10,
    [2] = (char) 120 "x",
}
(gdb) p_v vec
"vec" = (std::vector<int, ..>) <0xHEX> size:100000 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
    [3] = 0,
    [4] = 0,
    [5] = 0,
    [6] = 0,
    [7] = 0,
    [8] = 0,
    [9] = 0,
    [10] = 0,
    [11] = 0,
    [12] = 0,
    [13] = 0,
    [14] = 0,
    [15] = 0,
    [16] = 0,
    [17] = 0,
    [18] = 0,
    [19] = 0,
    [20] = 0,
    [21] = 0,
    [22] = 0,
    [23] = 0,
    [24] = 0,
    [25] = 0,
    [26] = 0,
    [27] = 0,
    [28] = 0,
    [29] = 0,
    [30] = 0,
    [31] = 0,
    [32] = 0,
    [33] = 0,
    [34] = 0,
    [35] = 0,
    [36] = 0,
    [37] = 0,
    [38] = 0,
    [39] = 0,
    [40] = 0,
    [41] = 0,
    [42] = 0,
    [43] = 0,
    [44] = 0,
    [45] = 0,
    [46] = 0,
    [47] = 0,
    [48] = 0,
    [49] = 0,
}
(gdb) p_v vec[0:10, 15]
"vec" = (std::vector<int, ..>) <0xHEX> size:100000 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
    [3] = 0,
    [4] = 0,
    [5] = 0,
    [6] = 0,
    [7] = 0,
    [8] = 0,
    [9] = 0,
    [10] = 0,
    [15] = 0,
}
(gdb) p_v vec[]@
"vec" = (std::vector<int, ..>) <0xHEX> size:100000 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
}
(gdb) p_v ptr
"ptr" = (std::vector<int, ..> *) <0xHEX> { ptr = size:100000 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
    [3] = 0,
    [4] = 0,
    [5] = 0,
    [6] = 0,
    [7] = 0,
    [8] = 0,
    [9] = 0,
    [10] = 0,
    [11] = 0,
    [12] = 0,
    [13] = 0,
    [14] = 0,
    [15] = 0,
    [16] = 0,
    [17] = 0,
    [18] = 0,
    [19] = 0,
    [20] = 0,
    [21] = 0,
    [22] = 0,
    [23] = 0,
    [24] = 0,
    [25] = 0,
    [26] = 0,
    [27] = 0,
    [28] = 0,
    [29] = 0,
    [30] = 0,
    [31] = 0,
    [32] = 0,
    [33] = 0,
    [34] = 0,
    [35] = 0,
    [36] = 0,
    [37] = 0,
    [38] = 0,
    [39] = 0,
    [40] = 0,
    [41] = 0,
    [42] = 0,
    [43] = 0,
    [44] = 0,
    [45] = 0,
    [46] = 0,
    [47] = 0,
    [48] = 0,
    [49] = 0,
} }
(gdb) p_v vec_st
"vec_st" = (std::vector<st, ..>) <0xHEX> size:2 capacity:N {
    [0] = (st) <0xHEX> {
        "i" = (int) 1,
        "ui" = (unsigned int) 1000,
        "l" = (long) 1000,
        "ul" = (unsigned long) 1000,
        "f" = (float) 1000,
        "d" = (double) 1000,
        "inc" = (st_inc) <0xHEX> {
            "inc" = (int) 0,
        },
    },
    [1] = (st) <0xHEX> {
        "i" = (int) 2,
        "ui" = (unsigned int) 1000,
        "l" = (long) 1000,
        "ul" = (unsigned long) 1000,
        "f" = (float) 1000,
        "d" = (double) 1000,
        "inc" = (st_inc) <0xHEX> {
            "inc" = (int) 0,
        },
    },
}
(gdb) p_v ar
"ar" = (std::array<int, 200>) <0xHEX> size:200 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
    [3] = 0,
    [4] = 0,
    [5] = 0,
    [6] = 0,
    [7] = 0,
    [8] = 0,
    [9] = 0,
    [10] = 0,
    [11] = 0,
    [12] = 0,
    [13] = 0,
    [14] = 0,
    [15] = 0,
    [16] = 0,
    [17] = 0,
    [18] = 0,
    [19] = 0,
    [20] = 0,
    [21] = 0,
    [22] = 0,
    [23] = 0,
    [24] = 0,
    [25] = 0,
    [26] = 0,
    [27] = 0,
    [28] = 0,
    [29] = 0,
    [30] = 0,
    [31] = 0,
    [32] = 0,
    [33] = 0,
    [34] = 0,
    [35] = 0,
    [36] = 0,
    [37] = 0,
    [38] = 0,
    [39] = 0,
    [40] = 0,
    [41] = 0,
    [42] = 0,
    [43] = 0,
    [44] = 0,
    [45] = 0,
    [46] = 0,
    [47] = 0,
    [48] = 0,
    [49] = 0,
}
(gdb) p_v ar[]@
"ar" = (std::array<int, 200>) <0xHEX> size:200 capacity:N {
    [0] = 1,
    [1] = 2,
    [2] = 0,
}
(gdb) p_v deque
"deque" = (std::deque<int, ..>) <0xHEX> size:7 {
    [0] = (int) 100,
    [1] = (int) 100,
    [2] = (int) 100,
    [3] = (int) 100,
    [4] = (int) 100,
    [5] = (int) 100,
    [6] = (int) 100,
}
(gdb) p_v list
"list" = (std::list<int, ..>) <0xHEX> {
    [0] = (int) 100,
    [1] = (int) 200,
    [2] = <0x0>,
}
(gdb) p_v list_it
"list_it" = (std::_List_iterator<int>) <0xHEX> { ptr = (int) 100 }
(gdb) p_v list_fw
"list_fw" = (std::forward_list<int, ..>) <0xHEX> {
    [0] = (int) 34,
    [1] = (int) 19,
    [2] = (int) 77,
    [3] = (int) 2,
    [4] = (int) 16,
    [5] = <0x0>,
}
(gdb) p_v list_fw_it
"list_fw_it" = (std::_Fwd_list_iterator<int>) <0xHEX> { ptr = (int) 34 }
(gdb) p_v stack
"stack" = (std::stack<int, ..>) <0xHEX> {
    "c" = (std::deque<int, ..>) <0xHEX> size:2 {
        [0] = (int) 1,
        [1] = (int) 2,
    },
}
(gdb) p_v queue
"queue" = (std::queue<int, ..>) <0xHEX> {
    "c" = (std::deque<int, ..>) <0xHEX> size:2 {
        [0] = (int) 2,
        [1] = (int) 3,
    },
}
(gdb) p_v set
"set" = (std::set<int, ..>) <0xHEX> size:3 {
    [0] = (int) 1,
    [1] = (int) 2,
    [2] = (int) 3,
}
(gdb) p_v multiset
"multiset" = (std::multiset<int, ..>) <0xHEX> size:2 {
    [0] = (int) 1,
    [1] = (int) 1,
}
(gdb) p_v set_unorder
"set_unorder" = (std::unordered_set<std::basic_string<char, ..>) <0xHEX> size:3 {
    [0] = (std::basic_string<char, ..>) <0xHEX> str_len:4 capacity:N { [0:3] = "blue" },
    [1] = (std::basic_string<char, ..>) <0xHEX> str_len:5 capacity:N { [0:4] = "green" },
    [2] = (std::basic_string<char, ..>) <0xHEX> str_len:6 capacity:N { [0:5] = "yellow" },
}
(gdb) p_v bitset0[]@
"bitset0" = (std::bitset<50>) <0xHEX> {
    [0] = 0,
}
(gdb) p_v bitset1[] { @ _ = 1 }
"bitset1" = (std::bitset<50>) <0xHEX> {
    [0] = 1,
}
(gdb) p_v map
"map" = (std::map<int, ..>) <0xHEX> size:2 {
    [0] = { (int) 1 } => { (std::basic_string<char, ..>) <0xHEX> str_len:1 capacity:N { [0] = "1" } },
    [1] = { (int) 3 } => { (std::basic_string<char, ..>) <0xHEX> str_len:5 capacity:N { [0:4] = "str 3" } },
}
(gdb) p_v map_unorder
"map_unorder" = (std::unordered_map<std::basic_string<char, ..>) <0xHEX> size:4 {
    [0] = { (std::basic_string<char, ..>) <0xHEX> str_len:13 capacity:N { [0:12] = "mineral water" } } => { (double) 2.5 },
    [1] = { (std::basic_string<char, ..>) <0xHEX> str_len:5 capacity:N { [0:4] = "water" } } => { (double) 3.5 },
    [2] = { (std::basic_string<char, ..>) <0xHEX> str_len:5 capacity:N { [0:4] = "flour" } } => { (double) 1.5 },
    [3] = { (std::basic_string<char, ..>) <0xHEX> str_len:4 capacity:N { [0:3] = "milk" } } => { (double) 2 },
}
(gdb) p_v map_unorder[3]
"map_unorder" = (std::unordered_map<std::basic_string<char, ..>) <0xHEX> size:4 {
    [3] = { (std::basic_string<char, ..>) <0xHEX> str_len:4 capacity:N { [0:3] = "milk" } } => { (double) 2 },
}
(gdb) p_v multimap
"multimap" = (std::multimap<int, ..>) <0xHEX> size:2 {
    [0] = { (int) 2 } => { (std::basic_string<char, ..>) <0xHEX> str_len:1 capacity:N { [0] = "1" } },
    [1] = { (int) 2 } => { (std::basic_string<char, ..>) <0xHEX> str_len:1 capacity:N { [0] = "2" } },
}
(gdb) p_v set
"set" = (std::set<int, ..>) <0xHEX> size:3 {
    [0] = (int) 1,
    [1] = (int) 2,
    [2] = (int) 3,
}
(gdb) p_v ptr_auto
"ptr_auto" = (std::auto_ptr<int>) <0xHEX> { ptr = (int *) <0xHEX> { ptr = 1 } }
(gdb) p_v ptr_shared
"ptr_shared" = (std::shared_ptr<int>) <0xHEX> desc:"count 1, weak 0" { ptr = (int *) <0xHEX> { ptr = 4 } }
(gdb) p_v ptr_unique
"ptr_unique" = (std::unique_ptr<int, ..>) <0xHEX> { ptr = (int *) <0xHEX> { ptr = 1 } }
