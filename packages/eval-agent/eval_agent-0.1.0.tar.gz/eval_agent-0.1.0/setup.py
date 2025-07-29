from setuptools import setup, find_packages

setup(
    name='eval_agent',
    version='0.1.0',
    author='Naman',
    packages=find_packages(),
    install_requires=['scikit-learn'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
