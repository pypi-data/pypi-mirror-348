#!/usr/bin/env python

import os
import os.path
from glob import glob
from setuptools import Extension, setup

def main():
    # Just in case we are being called from a different directory
    cwd = os.path.dirname(__file__)
    if cwd:
        os.chdir(cwd)

    distorm_module = Extension(
        "_distorm3",
        sources=sorted(glob('src/*.c')) + ["python/python_module_init.c"],
        include_dirs=['src', 'include'],
        define_macros=[('SUPPORT_64BIT_OFFSET', None), ('DISTORM_DYNAMIC', None)],
    )

    options = {
    # Setup instructions
    'packages'          : ['distorm3'],
    'package_dir'       : { 'distorm3' : 'python/distorm3' },
    'ext_modules'       : [distorm_module],
    # Metadata
    'name'              : 'distorm3s',
    'version'           : '3.5.4',
    'license_files'     : ['LICENSE'],
    'description'       : 'The goal of diStorm3 is to decode x86/AMD64' \
                          ' binary streams and return a structure that' \
                          ' describes each instruction.',
    'long_description'  : (
                        'Powerful Disassembler Library For AMD64\n'
                        'by Gil Dabah (distorm@gmail.com)\n'
                        '\n'
                        'Python bindings by Mario Vilas (mvilas@gmail.com)'
                        ),
    'author'            : 'Gil Dabah',
    'author_email'      : 'distorm@gmail.com',
    'maintainer'        : 'Gil Dabah',
    'maintainer_email'  : 'distorm@gmail.com',
    'url'               : 'https://github.com/gdabah/distorm/',
    'download_url'      : 'https://github.com/gdabah/distorm/',
    'platforms'         : ['cygwin', 'win', 'linux', 'macosx'],
    'classifiers'       : [
                        'License :: OSI Approved :: BSD License',
                        'Development Status :: 5 - Production/Stable',
                        'Intended Audience :: Developers',
                        'Natural Language :: English',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: POSIX :: Linux',
                        'Programming Language :: Python :: 3.12',
                        'Topic :: Software Development :: Disassemblers',
                        'Topic :: Software Development :: Libraries :: Python Modules',
                        ],
    'python_requires'   : '>=3.6',
    'long_description_content_type' : "text/plain",                    
    }

    # Call the setup function
    setup(**options)

if __name__ == '__main__':
    main()
