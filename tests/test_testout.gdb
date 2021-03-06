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

(gdb) p_s verbose 0
(gdb) p_s w 0
(gdb) p_v cppwstr
"cppwstr" =  { [0:29] = L"Василий Пупкин, Vasiliy Pupkin" }
(gdb) p_v cppwstr [ 0:10, 15 ]
"cppwstr" = {
     { [0:10] = L"Василий Пуп" },
     { [15] = L" " },
}
(gdb) p_v cppstr<utf8>
"cppstr" =  { [0:41] = utf-8:"Василий Пупкин Vasiliy Pupkin" }
(gdb) p_v cppstr<arr,utf8> [ 0:10, 15 ]
"cppstr" = {
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
"cppstr1251" =  { [0:14] = "Василий Vasiliy" }
(gdb) p_v cppstr1251<arr> [ 0:10, 15 ]
"cppstr1251" = {
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
"tuple1" = {
    [1] = 10,
    [2] = 120 "x",
}
(gdb) p_v tuple1
"tuple1" = {
    [1] = 10,
    [2] = 120 "x",
}
(gdb) p_v vec
"vec" = {
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
"vec" = {
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
"vec" = {
    [0] = 1,
    [1] = 2,
    [2] = 0,
}
(gdb) p_v ptr
"ptr" = { ptr = {
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
"vec_st" = {
    [0] = {
        "i" = 1,
        "ui" = 1000,
        "l" = 1000,
        "ul" = 1000,
        "f" = 1000,
        "d" = 1000,
        "inc" = {
            "inc" = 0,
        },
    },
    [1] = {
        "i" = 2,
        "ui" = 1000,
        "l" = 1000,
        "ul" = 1000,
        "f" = 1000,
        "d" = 1000,
        "inc" = {
            "inc" = 0,
        },
    },
}
(gdb) p_v ar
"ar" = {
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
"ar" = {
    [0] = 1,
    [1] = 2,
    [2] = 0,
}
(gdb) p_v deque
"deque" = {
    [0] = 100,
    [1] = 100,
    [2] = 100,
    [3] = 100,
    [4] = 100,
    [5] = 100,
    [6] = 100,
}
(gdb) p_v list
"list" = {
    [0] = 100,
    [1] = 200,
    [2] = <0x0>,
}
(gdb) p_v list_it
"list_it" = { ptr = 100 }
(gdb) p_v list_fw
"list_fw" = {
    [0] = 34,
    [1] = 19,
    [2] = 77,
    [3] = 2,
    [4] = 16,
    [5] = <0x0>,
}
(gdb) p_v list_fw_it
"list_fw_it" = { ptr = 34 }
(gdb) p_v stack
"stack" = {
    "c" = {
        [0] = 1,
        [1] = 2,
    },
}
(gdb) p_v queue
"queue" = {
    "c" = {
        [0] = 2,
        [1] = 3,
    },
}
(gdb) p_v set
"set" = {
    [0] = 1,
    [1] = 2,
    [2] = 3,
}
(gdb) p_v multiset
"multiset" = {
    [0] = 1,
    [1] = 1,
}
(gdb) p_v set_unorder
"set_unorder" = {
    [0] =  { [0:3] = "blue" },
    [1] =  { [0:4] = "green" },
    [2] =  { [0:5] = "yellow" },
}
(gdb) p_v bitset0[]@
"bitset0" = {
    [0] = 0,
}
(gdb) p_v bitset1[] { @ _ = 1 }
"bitset1" = {
    [0] = 1,
}
(gdb) p_v map
"map" = {
    [0] = { 1 } => {  { [0] = "1" } },
    [1] = { 3 } => {  { [0:4] = "str 3" } },
}
(gdb) p_v map_unorder
"map_unorder" = {
    [0] = {  { [0:12] = "mineral water" } } => { 2.5 },
    [1] = {  { [0:4] = "water" } } => { 3.5 },
    [2] = {  { [0:4] = "flour" } } => { 1.5 },
    [3] = {  { [0:3] = "milk" } } => { 2 },
}
(gdb) p_v map_unorder[3]
"map_unorder" = {
    [3] = {  { [0:3] = "milk" } } => { 2 },
}
(gdb) p_v multimap
"multimap" = {
    [0] = { 2 } => {  { [0] = "1" } },
    [1] = { 2 } => {  { [0] = "2" } },
}
(gdb) p_v set
"set" = {
    [0] = 1,
    [1] = 2,
    [2] = 3,
}
(gdb) p_v ptr_auto
"ptr_auto" = { ptr = { ptr = 1 } }
(gdb) p_v ptr_shared
"ptr_shared" = { ptr = { ptr = 4 } }
(gdb) p_v ptr_unique
"ptr_unique" = { ptr = { ptr = 1 } }
