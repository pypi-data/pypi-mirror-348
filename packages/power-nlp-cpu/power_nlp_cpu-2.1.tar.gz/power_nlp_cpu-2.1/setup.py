from setuptools import setup, find_packages

setup(name='power_nlp_cpu',
		version='2.1',
		license='MIT',
		packages=find_packages(),
		include_package_data=True,
		classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		],
		python_requires='>=3.6',
		install_requires = []
		)
