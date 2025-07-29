from setuptools import setup, find_packages

setup(
    name='cluster365',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['google-generativeai'],
    entry_points={
        'console_scripts': [
            'cluster365=cluster365.main:main',
        ],
    },
    author='Your Name',
    author_email='you@example.com',
    description='Send file content to Gemini AI and get reply in terminal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cluster365',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
