from setuptools import setup, find_packages

setup(name='unit_identification_cpu',
		version='3.3',
		license='MIT',
		packages=find_packages(),
		include_package_data=True,
		classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		],
		python_requires='>=3.6'
		)
