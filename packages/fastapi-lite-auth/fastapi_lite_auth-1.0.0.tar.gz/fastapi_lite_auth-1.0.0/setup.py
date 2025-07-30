from setuptools import setup


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='fastapi_lite_auth',
  version='1.0.0',
  author='losos3000',
  author_email='andreygolikov.work@yandex.ru',
  description='Simple login/password authentication module for FastAPI project.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/losos3000/fastapi-lite-auth',
  packages=['fastapi_lite_auth'],
  install_requires=['authx>=1.4.2', 'fastapi>=0.115.12', 'pydantic>=2.11.4'],
  classifiers=[
    'Programming Language :: Python :: 3.13',
    'Operating System :: OS Independent'
  ],
  keywords='fastapi auth authentication lite simple basic base',
  project_urls={
    'GitHub': 'https://github.com/losos3000/fastapi-lite-auth'
  },
  python_requires='>=3.13.0'
)