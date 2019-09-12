from setuptools import setup, find_packages

setup(name='Hearthstone Card Generation',
      version='0.1',
      description='Hearthstone Card Generation using Deep Learning',
      author='Oisin McLaughlin',
      author_email='mclaughlin-o9@ulster.ac.uk',
      url='https://github.com/oisinmcl/final_year_project',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
	   install_requires=["python-firebase >= 1.2.0 ",
						"tensorflow == 1.12.2",
						"kivy == 1.10.0"],
     )