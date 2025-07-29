#!/usr/bin/python3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys
import os
import platform

pyver = str(sys.version_info.major) + "." + str(sys.version_info.minor)
dir_path = os.path.dirname(os.path.realpath(__file__))
static_obj_dir = ''

def gcc_version():
    return int(os.popen('gcc -dumpversion').read().strip().split(".")[0])

if platform.system() == 'Linux':
    rdirs = ['$ORIGIN/../../../../lib', '$ORIGIN/../../../lib', '$ORIGIN/../../lib', '/usr/local/lib', '$ORIGIN']
    linkerdirs = ['-std=c++11'] if gcc_version() > 5 else []
    library_dirs = []
elif platform.system() == 'Darwin':
    rdirs = ['@loader_path/../../../../lib', '@loader_path/../../../lib', '@loader_path/../../lib', '/usr/local/lib', '@loader_path', '@loader_path/../build']
    linkerdirs = ['-std=c++11', '-Wl,-rpath,'+'@loader_path/', '-Wl,-rpath,'+'@loader_path/../../../../lib', '-Wl,-rpath,'+'@loader_path/../../../lib', '-Wl,-rpath,'+'@loader_path/../../lib', '-Wl,-rpath,'+'/usr/local/lib', '-Wl,-rpath,'+'@loader_path/../build']
    library_dirs = []
elif platform.system() == 'Windows':
    linkerdirs = ['-std=c++11', '-static-libgcc', '-static-libstdc++', '-Wl,-Bstatic,--whole-archive', '-lwinpthread', '-Wl,--no-whole-archive']
    static_obj_dir = os.path.join(os.path.dirname(dir_path), '_skbuild', 'win-amd64-' + pyver, 'cmake-build', 'CMakeFiles')
    print('Windows MINGW!')
else:
    print('Unsupported Platform!!!')

if platform.system() == 'Windows':
    cythonize_ext = [
        Extension("topoly.topoly_knot", ["topoly_knot.pyx"],
                  include_dirs=["preprocess", "knot_net", f'{os.getenv("BOOST_ROOT")}/include', f'{os.getenv("BOOST_INCLUDE")}'],
                  extra_compile_args=["-std=c++11"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\knotfinder.dir\\knot_net\\determinant.cpp.obj',
                      static_obj_dir + '\\knotfinder.dir\\knot_net\\KknotsSimpler_cpu.cpp.obj',
                      static_obj_dir + '\\knotfinder.dir\\knot_net\\knotsFinder.cpp.obj',
                      static_obj_dir + '\\knotfinder.dir\\knot_net\\libknot.cpp.obj',
                      static_obj_dir + '\\knotfinder.dir\\knot_net\\whichKnot.cpp.obj',
                      static_obj_dir + '\\preprocess.dir\\preprocess\\libpreprocess.cpp.obj']),
        Extension("topoly.topoly_preprocess", ["topoly_preprocess.pyx"],
                  include_dirs=["preprocess"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\preprocess.dir\\preprocess\\libpreprocess.cpp.obj']),
        Extension("topoly.topoly_lmpoly", ["topoly_lmpoly.pyx"],
                  include_dirs=["homfly/lmpoly/Wandy"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\lmpoly.dir\\homfly\\lmpoly\\Wandy\\lmpolyWN.c.obj',
                      static_obj_dir + '\\lmpoly.dir\\homfly\\lmpoly\\Wandy\\times.c.obj']),
        Extension("topoly.topoly_homfly", ["topoly_homfly.pyx"],
                  include_dirs=["homfly/homflylink","/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1"],
                  extra_compile_args=["-std=c++11"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\homfly.dir\\homfly\\homflylink\\libhomfly.cpp.obj',
                      static_obj_dir + '\\homfly.dir\\homfly\\homflylink\\homflyFinder.cpp.obj',
                      static_obj_dir + '\\preprocess.dir\\preprocess\\libpreprocess.cpp.obj']),
        Extension("topoly.topoly_surfaces", ["topoly_surfaces.pyx"],
                  include_dirs=["preprocess", "surfaces"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\surfaces.dir\\surfaces\\baricentre.cpp.obj',
                      static_obj_dir + '\\surfaces.dir\\surfaces\\GLN.cpp.obj',
                      static_obj_dir + '\\surfaces.dir\\surfaces\\intersections_zOrient_Pablo130715.cpp.obj',
                      static_obj_dir + '\\surfaces.dir\\surfaces\\libsurfaces.cpp.obj',
                      static_obj_dir + '\\surfaces.dir\\surfaces\\surfacesFinder.cpp.obj',
                      static_obj_dir + '\\preprocess.dir\\preprocess\\libpreprocess.cpp.obj']),
        Extension("topoly.topoly_gln", ["topoly_gln.pyx"],
                  include_dirs=["preprocess", "glns"],
                  extra_link_args=linkerdirs,
                  extra_objects=[
                      static_obj_dir + '\\glnfinder.dir\\glns\\libgln.cpp.obj',
                      static_obj_dir + '\\surfaces.dir\\surfaces\\GLN.cpp.obj',
                      static_obj_dir + '\\preprocess.dir\\preprocess\\libpreprocess.cpp.obj']),
    ]
else:
    cythonize_ext = [
        Extension("topoly.topoly_knot", ["topoly_knot.pyx"],
                  include_dirs=["preprocess", "knot_net", f'{os.getenv("BOOST_ROOT")}/include' ],
                  libraries=["knotfinder"],
                  extra_compile_args=["-std=c++11"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=rdirs),
        Extension("topoly.topoly_preprocess", ["topoly_preprocess.pyx"],
                  include_dirs=["preprocess"],
                  libraries=["preprocess"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=rdirs),
        Extension("topoly.topoly_lmpoly", ["topoly_lmpoly.pyx"],
                  include_dirs=["homfly/lmpoly/Wandy"],
                  libraries=["lmpoly"],
                  extra_compile_args=["-std=c99"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=linkerdirs),
        Extension("topoly.topoly_homfly", ["topoly_homfly.pyx"],
                  include_dirs=["homfly/homflylink","/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1"],
                  libraries=["homfly"],
                  extra_compile_args=["-std=c++11"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=rdirs
                  ),
        Extension("topoly.topoly_surfaces", ["topoly_surfaces.pyx"],
                  include_dirs=["preprocess", "surfaces"],
                  libraries=["surfaces"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=rdirs),
        Extension("topoly.topoly_gln", ["topoly_gln.pyx"],
                  include_dirs=["preprocess", "glns"],
                  libraries=["glnfinder"],
                  extra_link_args=linkerdirs,
                  runtime_library_dirs=rdirs),
    ]

setup(
    ext_modules=cythonize(cythonize_ext, compiler_directives={'language_level': "3"})
)