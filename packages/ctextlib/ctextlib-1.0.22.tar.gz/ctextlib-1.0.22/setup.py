import os
import re
import sys
import platform
import subprocess
import setuptools
import io
import sysconfig

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]
        
        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            n_bits = 32 << bool(sys.maxsize >> 32)
            #if sys.maxsize > 2**32:
            if n_bits > 32:
                # cmake_args += ['-A', 'x64']
                cmake_args += ['-G', 'Visual Studio 15 2017', '-A', 'x64'] 
            else:
            #cmake_args += ['-G', 'Visual Studio 16 2019', '-A', 'x64'] 
            #cmake_args += ['-G', 'Visual Studio 15 2017', '-A', 'x64'] 
            #    cmake_args += ['-G', 'Visual Studio 15 2017', '-A', 'win32'] 
                cmake_args += ['-A', 'win32']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        #PYTHON_DATA = sysconfig.get_path('data')
        PYTHON_SCRIPTS = sysconfig.get_path('scripts')
        #PITHON_LIBS = PYTHON_DATA + "\\libs"
        #PITHON_INCLUDES = PYTHON_DATA + "\\include"
        
        #cmake_args += ['include_dirs', PITHON_INCLUDES]
        # build_args += ['lib_dirs', PITHON_LIBS]     
        
        env = os.environ.copy()
        # env['PATH'] = PYTHON_SCRIPTS + "\\;" + PYTHON_DATA + "\\;" + PITHON_LIBS +";" + PITHON_INCLUDES +";"
        # print(env)
        
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
            
        correct_cmake_path = PYTHON_SCRIPTS + "\\cmake"   
        print('CMake path:  ', correct_cmake_path)
            
        subprocess.check_call([correct_cmake_path, ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call([correct_cmake_path, '--build', '.'] + build_args, cwd=self.build_temp)

with io.open("README.md", 'r', encoding='utf8') as f:
    long_description = f.read()
    
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

# I need CMAKE only when building from source  (pure python package)
PACKAGES = ''    
# from: https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py   
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            # The root_is_pure bit tells the wheel machinery to build a non-purelib 
            self.root_is_pure = False
            PACKAGES = 'cmake'
        #def get_tag(self):
        #    python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't contain any python source
            # python, abi = 'py2.py3', 'none'
         #   python, abi = 'py3', 'none'
         #   return python, abi, plat
            
except ImportError:
    bdist_wheel = None    
    
setup(
    name='ctextlib',
    version='1.0.22',
    author='Anton Milev',
    author_email='amil@abv.bg',
    description='Python package with CText C++ extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension('cmake_ctextlib')],
    cmdclass = {
                    'bdist_wheel': bdist_wheel,
                    'build_ext': CMakeBuild
               },
    zip_safe=False,
    url="https://github.com/antonmilev/CText",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[PACKAGES,],
    python_requires='>=2.7',
)





    