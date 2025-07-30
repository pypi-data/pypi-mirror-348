from setuptools import setup, find_packages

setup(
    name='fastai_newuser_recommender',
    version='0.1.0',
    description='A simple new-user cold start recommender for fastai collaborative filtering',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        'fastai>=2.0.0',
        'torch>=1.7.0'
    ],
    python_requires='>=3.7',
    url='https://github.com/yourname/fastai_newuser_recommender',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 