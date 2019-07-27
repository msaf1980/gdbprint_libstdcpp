import sys
import os
import time
import re
from distutils.cmd import Command
from setuptools import setup
from distutils.command.clean import clean
from distutils.errors import *

class TestError(DistutilsError):
    pass

class RunTests(Command):
    user_options = [
        ('xml-output=', None,
         "file for JUnit compatible XML output."),
        ]

    def initialize_options(self):
        self.xml_output = None

    def finalize_options(self): pass

    def run(self):
        tests = ['test_testout', 'test_testout_v2']
        from subprocess import Popen, PIPE, call
        from os import getcwd, execlp, chdir, path
        import re
        cdir = path.dirname(path.realpath(__file__))

        if self.xml_output:
            xmlfile = open(self.xml_output, "w")
            xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n<testsuite tests="%d">\n' % len(tests))

        cwd = path.join(cdir, 'tests')
        chdir(cwd)
        if os.system("make > /dev/null 2>&1"):
            raise Exception("make failed")
        for test in tests:
            if self.xml_output:
                xmlfile.write('<testcase classname="gdbtest" name="%s"' % test)
            else:
                sys.stdout.write(test)
            sys.stdout.flush()
            test = path.join(cwd, test)
            fg = open(test+'.gdb', 'r')
            fi = open(test+'.in', 'w')
            fo = open(test+'.out', 'w')
            for l in fg:
                if l.startswith('(gdb) '):
                    fi.write(l[6:])
                else:
                    fo.write(l)
            fg.close()
            fi.close()
            fo.close()
            start = time.time()
            p=Popen(['gdb', '-batch', '-n', '-x', test + '.in'], cwd=cwd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            (o,e)=p.communicate()
            err = re.sub(r'warning: .*\n', '', e)
            err = re.sub(r'[ \t]+\n', '', err)
            err = re.sub(r'\n', '', err)
            if err: raise Exception(e)
            o = re.sub(r'load gdbprint \d+.\d+.\d+', 'load gdbprint', o)
            o = re.sub(r'(=.*) 0x[0-9a-f]+', r'\1 0xXXXXX', o)
            o = re.sub(r'Temporary breakpoint 1 at .*\n', '', o)
            o = re.sub(r'Breakpoint [0-9]+ at 0x[0-9a-f]+:', 'Breakpoint:', o)
            o = re.sub(r'Breakpoint [0-9]+, main \(argc=1, argv=0x[0-9a-f]+\) at', 'Breakpoint 1, main at', o)
            o = re.sub(r'[0-9]+[ \t]+return 0;', '', o)
            o = re.sub(r'0x[0-9a-f]*[1-9a-f]+[0-9a-f]*', '0xHEX', o)
            o = re.sub(r'std::__cxx11::', 'std::', o)
            o = re.sub(r'capacity:\d+ ', 'capacity:N ', o)
            o = re.sub(r'(\d+)ul>', r'\1>', o)
            o = re.sub(r'std::__shared_ptr<int, \.\.>::element_type', 'int', o)
            o = re.sub(cdir, '', o)
            timediff = time.time() - start
            if self.xml_output:
                xmlfile.write(' time="%f">\n' % timediff)
            else:
                sys.stdout.write(' in %f s\n' % timediff)
            with open(test + '.reject', 'w') as f: f.write(o)
            with open(test + '.out', 'r') as f: i = f.read()

            if o == i:
	            failed = False
            else:
                failed = True    
                if self.xml_output:
                    xmlfile.write('<failure message="test failure">\n')
                    diff_p = Popen(['diff', '-u', test + '.out', test + '.reject' ], cwd=cwd, stdout=PIPE, universal_newlines=True)
                    (diff_o, diff_e) = diff_p.communicate()
                    xmlfile.write(diff_o)
                else:
                    call([ 'diff', '-u', test + '.out', test + '.reject' ])

                if self.xml_output:
                    xmlfile.write('</failure>\n')

            if self.xml_output:
                xmlfile.write('</testcase>\n')

        if self.xml_output:
            xmlfile.write('</testsuite>\n')
            xmlfile.close()

        if failed:
            raise TestError("test failed!")


class RunClean(clean):
    def run(self):
        from subprocess import Popen, PIPE, call
        from os import getcwd, chdir, path
        from os import remove
        import glob
        import shutil
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()
        cdir = path.dirname(path.realpath(__file__))
        for f in glob.glob(path.join(cdir, pname, "*.pyc")):
            remove(f)
        shutil.rmtree(path.join(cdir, 'build'), ignore_errors=True)
        shutil.rmtree(path.join(cdir, 'dist'), ignore_errors=True)
        shutil.rmtree(path.join(cdir, pname + '.egg-info'), ignore_errors=True)
        shutil.rmtree(path.join(cdir, pname, '__pycache__'), ignore_errors=True)
        cwd = path.join(cdir, 'tests')
        chdir(cwd)
        call([ 'make', 'clean' ])


def pkg_version(name):
    with open('%s/__init__.py' % name, 'r') as f:
        for line in f:
            m = re.match(r'^version * = *\"(.*)\"', line)
            if not m is None:
                v = m.group(1)
                m = re.match(r'^\"?([0-9]+)\.([0-9]+)\.([0-9]+)\"?$', v)
                if m is None:
                    raise ValueError("incorrect version: %s" % v)
                return "%d.%d.%d" % (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        raise ValueError("version not found")


if __name__ == '__main__':

    pname = 'gdbprint_libstdcpp'

    setup(name=pname,
        version=pkg_version(pname),
        description='GDB GNU libstdc++-v3 STL data structuras printers for gdbprint',
        url='http://github.com/msaf1980/gdbprint_libstdcpp',
        author='Michail Safronov',
        author_email='msaf1980@gmail.com',
        license='MIT',
        packages=[pname],
        install_requires=['gdbprint'],
        zip_safe=True,
        cmdclass={
            'test': RunTests,
            'clean': RunClean
        },
)
