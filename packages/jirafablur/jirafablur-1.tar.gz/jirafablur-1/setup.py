
from setuptools.command.build_ext import build_ext
class my_build(build_ext):
	def run(self):
		N = "jirafablur"                      # name
		O = "-O3 -march=native -shared -fPIC" # compilation options
		E = "so"                              # .ext of shared objects
		import sys, os
		if sys.platform == "darwin":
			E = "dylib"
			O = f"{O} -undefined dynamic_lookup"
		os.system(f"cc {O} {N}.c -o c{N}.{E}")
		os.system(f"cp c{N}.{E} {self.build_lib}/c{N}.{E}")

from setuptools import Extension, setup
setup(
	name="jirafablur",
	version="1",
	py_modules=["jirafablur"],
	ext_modules=[ Extension(name="jirafablur", sources=["jirafablur.c"]) ],
	cmdclass={'build_ext': my_build}
)
