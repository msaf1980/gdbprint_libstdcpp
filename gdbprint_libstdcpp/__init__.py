from . import libstdcpp_v3
from gdbprint.gdbutils import print_str

name = "gdbprint_libstdcpp"
version = "0.1.1"
print_str("load %s %s\n" % (name, version))

libstdcpp_v3.register()
