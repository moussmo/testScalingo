from setuptools import setup

setup(
   name='test',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['test'],  #same as name
   install_requires=['flask'], #external packages as dependencies
)