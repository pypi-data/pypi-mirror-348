import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


setup(
    name='michael_tools',
    version='0.0.6',
    author='Michael Smith',
    author_email='1422749310@qq.com',
    description='This is my personal toolkit',
    packages=find_packages(),  # 自动发现所有模块
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    install_requires=[  # 依赖项（可选）
        # 'requests',
    ],
)
