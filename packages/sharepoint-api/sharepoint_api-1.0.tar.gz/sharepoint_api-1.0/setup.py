from distutils.core import setup
setup(
    name='sharepoint_api',
    packages=['sharepoint_api'],
    version='1.0',
    license='MIT',
    description='Python SharePoint API for folder or file operations (download, upload, delete)',
    author='Naseem AP',
    author_email='naseemalassampattil@gmail.com',
    url="https://github.com/naseemap-er/sharepoint_api",
    download_url="https://github.com/naseemap-er/sharepoint_api/archive/refs/tags/v1.0.tar.gz",
    keywords=['sharepoint', 'api', 'python', 'sharepoint api', 'sharepoint folder', 'sharepoint file'],
    install_requires=[
        'requests',
        'requests_ntlm',
        'beautifulsoup4',
        'lxml',
        'html5lib',
        'office365-rest-python-client'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    
)