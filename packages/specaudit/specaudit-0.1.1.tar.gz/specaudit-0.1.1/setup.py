from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='specaudit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            'spec-checker=spec_checker.cli:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    author='Yuvaraj',
    author_email='yuvarajsithusankar@email.com',
    description='A CLI and Python tool to validate various specs from CSV/JSON input',
    long_description_content_type='text/markdown',
    python_requires='>=3.6',

    url='https://github.com/Yuvi369/Spec-Checker',
    project_urls={
        'Documentation': 'https://github.com/Yuvi369/Spec-Checker/blob/feature/version-1/README.md',
        'Source': 'https://github.com/Yuvi369/Spec-Checker/tree/feature/version-1/spec-checker',
        'Bug Tracker': 'https://github.com/Yuvi369/Spec-Checker/issues',
        'Feedback Form': 'https://forms.cloud.microsoft/r/LucPyefjm8',  # if using Microsoft Forms
    },
)
