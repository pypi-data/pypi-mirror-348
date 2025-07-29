from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='maji_passport',
  version='1.0.10',
  author='ViktorTeodorih',
  author_email='viktorteodorihivanov@gmail.com',
  description='Maji Passport With custom authorisation',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://passport.maji.la/',
  packages=find_packages(),
  install_requires=[
    "djangorestframework-simplejwt",
    "pyjwt==2.10.1",
    "djangorestframework==3.11.1",
    "django-countries-plus",
    "loguru==0.5.3",
    "httpx==0.18.1",
    "confluent-kafka==2.3.0",
    "Pillow>=7.2.0",
    "sentry_sdk",
    "drf-yasg[validation]",
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='maji passport python',
  project_urls={
    'Documentation': 'link'
  },
  python_requires='>=3.9'
)