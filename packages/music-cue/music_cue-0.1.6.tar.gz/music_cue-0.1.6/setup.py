from setuptools import setup

setup(name='music-cue',
      version='0.1.6',
      description='A data entry application',
      url='https://github.com/hans-vvv/Music-Cue',
      author='Hans Verkerk',
      author_email='verkerk.hans@gmail.com',
      license='MIT',
      packages=['music_cue'],
      entry_points={'console_scripts': ['music_cue=music_cue.command_line:main']},
      install_requires=['openpyxl', 'ttkbootstrap'],
      zip_safe=False)
