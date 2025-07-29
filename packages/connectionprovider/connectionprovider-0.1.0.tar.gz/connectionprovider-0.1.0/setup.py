from setuptools import setup, find_packages

setup(
    name='connectionprovider',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A sample installable Python module.',
    long_description=open('README.md').read() if open('README.md', 'r', encoding='utf-8') else 'A longer description of the module.',
    long_description_content_type='text/markdown',
    url='https://example.com/your_project_url',  # Replace with your project's actual URL
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'google-api-python-client>=2.0.0',
        'google-auth>=2.0.0',
        # List your project's dependencies here, e.g.:
        # 'numpy>=1.20',
        # 'requests<3.0,>=2.25',
    ],
    project_urls={
        'Bug Reports': 'https://example.com/your_project_url/issues',
        'Source': 'https://example.com/your_project_url',
    },
) 