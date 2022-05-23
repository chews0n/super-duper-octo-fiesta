import setuptools

setuptools.setup(
    name='superduperoctofiesta',
    version='0.2',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['superduperoctofiesta=superduperoctofiesta.__main__:main']},
    python_requires=">=3.6",
    url='https://github.com/chews0n/super-duper-octo-fiesta',
    license='APACHE v2.0',
    author='chewson',
    author_email='chris@thehewsons.com',
    description='Create, train and run models for production prediction'
)
