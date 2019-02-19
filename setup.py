import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='pygame_lui',  

     version='0.1',

     author="Lanboost",

     author_email="lanboost@hotmail.com",

     description="A small UI package for pygame, in the spirit of Unity UI style.",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/javatechy/dokr",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: MIT License",

         "Operating System :: OS Independent",

     ],

 )