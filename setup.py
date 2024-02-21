from setuptools import setup, find_packages

setup(
    name='arxiver',
    version='0.0.1',
    author='huxiaoyang',
    author_email='545960442@qq.com',

    install_requires=[
        'fire',
        'loguru',
        'requests',
        'feedparser',
        'tabulate',
        'unidecode',
        'tenacity'
    ],

    entry_points={
      'console_scripts': [
          'arxiver = arxiver.main:main'
      ]
    },

    packages=find_packages(),

  

    # package_dir={"": ""},
    # package_data={
    #   'dataminingtools': ['configs/infer_configs/*.py']
    # },
    include_package_data=True

)