from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
  name='shapeslib',
  version='0.0.1',
  author='vlad',
  author_email='velikiy6789@gmail.com',
  description='Библиотека для вычисления площадей фигур',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/vladislav032/testTaskMindbox1',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'Operating System :: OS Independent'
  ],
  project_urls={
    'GitHub': 'https://github.com/vladislav032/testTaskMindbox1'
  },
  python_requires='>=3.6'
)