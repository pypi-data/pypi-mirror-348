from skbuild import setup

setup(
    name="libcasm-xtal",
    version="2.0.1",
    packages=["libcasm", "libcasm.xtal"],
    package_dir={"": "python"},
    cmake_install_dir="python/libcasm",
    include_package_data=False,
)
