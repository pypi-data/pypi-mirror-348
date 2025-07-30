from setuptools import setup, find_packages

setup(
    name='langid_indian',
    version='0.1.0',
    author='Yash Ingle',
    author_email='yash.ingle003@gmail.com',
    description='A language identifier for Indian languages using a pretrained Random Forest model.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yashingle-ai/TextLangDetect',
    project_urls={
        "Bug Tracker": "https://github.com/yashingle-ai/TextLangDetect/issues",
    },
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
        'tqdm',
        'requests',
        'joblib'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.7',
)
