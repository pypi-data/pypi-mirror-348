from setuptools import setup
import os.path

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="UTF-8"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line.strip())

setup(
      name="thonny-grader101",
      version="1.1.5",
      description="Thonny Plugins for Grader 101",
      long_description="""Thonny plugin for ChulaEngineeing Grader 101""",
      url="https://2110101.cp.eng.chula.ac.th",
      author="somchai.p",
      author_email="somchai.p@chula.ac.th",
      license="MIT",
      install_requires=requirements,
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