from setuptools import setup, find_packages
from setuptools.command.build import build
from os.path import dirname, join
import subprocess

class TreesitterBuild(build):
    def run(self):
        try:
            subprocess.run(['tree-sitter', 'generate'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to generate parser: {e}")
        build.run(self)

setup(
    name="tree_sitter_designtime",
    version="0.1.2",
    use_scm_version=True,
    packages=find_packages(),
    python_requires=">=3.6",
    author="Preston Arnold",
    description="Tree-sitter grammar for the DesignTime language",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/preston/tree-sitter-designtime",
    include_package_data=True,
    cmdclass={
        'build': TreesitterBuild,
    },
)
