from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flyf',
    version='0.0.3',
    author='FLYF',
    author_email='flyf@94209420.xyz',
    description='一个致力于打造最好用最方便的AI使用工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AiFLYF/flyf',
    packages=find_packages(),
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords=[
        'chat', 'Windows', 'Linux', 'MacOS',
        'chatgpt', 'openai', 'aitool',
        'ai工具', 'ai聊天工具', 'flyf', 'FLYFAI'
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'flyf=flyf.chat:main',
        ],
    },
)