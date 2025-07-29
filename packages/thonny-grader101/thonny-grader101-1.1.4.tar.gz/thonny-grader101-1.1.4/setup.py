from setuptools import setup
import os.path

setup(
      name="thonny-grader101",
      version="1.1.4",
      description="Thonny Plugins for Grader 101",
      long_description="""Thonny plugin for ChulaEngineeing Grader 101""",
      url="https://2110101.cp.eng.chula.ac.th",
      author="somchai.p",
      author_email="somchai.p@chula.ac.th",
      license="MIT",
      install_requires=[
        'thonny>=3.0.0',
        'requests>=2.27.1',
        'bs4>=0.0.2',
        'pypdf>=5.4.0', 
        'm2r2>=0.3.3',        
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      keywords="Grader101",
      platforms=["Windows", "macOS", "Linux"],
      python_requires=">=3.8",
      packages=["thonnycontrib.grader101"],
)