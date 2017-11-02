from setuptools import setup
import teampy

setup(
    name='teampy',
    version=teampy.__version__,
    author=teampy.__author__,
    author_email='git@edward.sh',
    description="Microsoft TFS (Team Foundation Server) SDK",
    license='MIT',
    url='https://github.com/arcward/teampy',
    packages=['teampy']
)