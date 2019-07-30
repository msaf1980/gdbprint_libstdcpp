#!/bin/sh

GDB=`which gdb`
GDB_PYTHON=`ldd ${GDB} | grep libpython | awk '{ print $1; }' | sed -e 's/\.so.*//g' -e 's/libpython/\/usr\/bin\/python/g'`

[ -n "${GDB_PYTHON}" ] || {
    echo "incorrect GDB_PYTHON" >&2
    exit 1
}

#python -m pip install setuptools --user

git clone https://github.com/msaf1980/gdbprint || exit 1
cd gdbprint || exit 1
${GDB_PYTHON} setup.py install --user || exit 1
cd ..
rm -rf gdbprint

${GDB_PYTHON} setup.py test || exit 1
${GDB_PYTHON} setup.py install --user || exit 1
${GDB_PYTHON} setup.py bdist || exit 1
