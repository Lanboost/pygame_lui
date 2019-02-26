import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='pygamelui',  

     version='0.1',

     author="Lanboost",

     author_email="lanboost@hotmail.com",

     description="A small UI package for pygame, in the spirit of Unity UI style.",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/Lanboost/pygame_lui",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )