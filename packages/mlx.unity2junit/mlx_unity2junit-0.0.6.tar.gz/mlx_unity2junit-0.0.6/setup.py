from setuptools import find_namespace_packages, setup

requires = [
]

setup(
    name='mlx.unity2junit',
    url='https://github.com/melexis/unity2junit',
    zip_safe=False,
    platforms='any',
    packages=find_namespace_packages(where=".", exclude=("doc.*", "doc", "tests.*", "tests", "build*")),
    package_dir={"": "."},
    package_data={
    },
    include_package_data=True,
    install_requires=requires,
)
