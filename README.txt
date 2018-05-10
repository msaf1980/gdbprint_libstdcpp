# gdbprint_libstdcpp

Package with printers for browse GNU libstdc++-v3 STL data structuras for gdbprint (https://github.com/msaf1980/gdbprint)
Based on pretty-printers for libstdc++.
Supported C++11 structuras

Tested on libstdc++-v3 (4.8 and 6.3)

Debug printers:
"std::tr1::unordered_set" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdUnorderedSetPrinter'>" (set)
"std::unordered_set" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdUnorderedSetPrinter'>" (set)
"std::unique_ptr" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdUniquePointerPrinter'>" (pointer)
"std::bitset" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdBitsetPrinter'>" (bitset)
"std::forward_list" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdForwardListPrinter'>" (list)
"std::stack" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdStackPrinter'>" (subtype)
"std::multimap" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdMapPrinter'>" (map)
"std::map" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdMapPrinter'>" (map)
"std::auto_ptr" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdAutoPointerPrinter'>" (pointer)
"std::weak_ptr" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdSharedPointerPrinter'>" (pointer)
"std::__cxx11::basic_string" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdStringPrinter'>" (string)
"std::deque" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdDequePrinter'>" (list_sized)
"std::tuple" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdTuplePrinter'>" (struct)
"std::basic_string" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdStringPrinter'>" (string)
"std::unordered_map" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdUnorderedMapPrinter'>" (map)
"std::array" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdArrayPrinter'>" (array)
"std::set" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdSetPrinter'>" (set)
"std::list" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdListPrinter'>" (list)
"std::vector" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdVectorPrinter'>" (array)
"std::shared_ptr" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdSharedPointerPrinter'>" (pointer)
"std::tr1::unordered_map" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdUnorderedMapPrinter'>" (map)
"std::multiset" = "<class 'gdbprint_libstdcpp.libstdcpp_v3.StdSetPrinter'>" (set)
