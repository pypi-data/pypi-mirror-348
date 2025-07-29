# -*- coding: utf-8 -*-

'''A setuptools-based setup module.

See https://packaging.python.org/distributing/

See:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
... for list of trove classifiers

'''


from codecs import open
from os import path
from setuptools import setup, find_packages


# See https://github.com/pypa/sampleproject/setup.py
root = path.abspath(path.dirname(__file__))

with open(path.join(root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(root, 'LICENSE.txt'), encoding='utf-8') as f:
    license = f.read()

with open(path.join(root, 'VERSION.txt'), encoding='utf-8') as f:
    version = f.read().strip()


project_description = '''
# AudioX: Transform Any Inspiration Into Professional Audio With AI

[AudioX](https://audiox.app/) is revolutionizing audio production with AI technology that transforms any input into professional-quality sound. With true "anything to audio" capabilities, AudioX offers unmatched versatility for creators of all skill levels.

## Five Powerful Generation Modes

1. **Text to Audio**: Describe any sound effect or voice for instant generation, from nature sounds to futuristic interfaces.

2. **Text to Music**: Transform written descriptions into complete musical compositions by specifying mood, style, and instrumentation.

3. **Image to Audio**: Upload images and AudioX creates matching audio - serene landscapes generate calming sounds, action scenes produce energetic audio.

4. **Video to Audio**: Generate synchronized sound effects that perfectly complement video content, enhancing immersion.

5. **Video to Music**: Create custom musical soundtracks that match the mood and pacing of your videos.

## Key Features

- Multi-modal input system (text, images, videos)
- Dual output capabilities (general audio and music)
- 30+ music styles and countless sound profiles
- Professional-grade quality with rapid generation
- Multi-track editing capabilities
- AI-assisted optimizations
- Platform-specific export presets

## Perfect For

- Content creators: Copyright-free background music and sound effects
- Game developers: Custom soundtracks and environmental audio
- Filmmakers: Quick production of temp tracks or final soundtracks
- Marketers: Efficient audio for commercials and promotions
- Podcasters: Professional intros and sound effects

## User Benefits

- No musical knowledge required
- Commercial usage rights for all generated audio
- Support for all mainstream audio formats
- Intuitive editing tools with DAW export options
- Significant time and cost savings in production

AudioX democratizes audio production, making professional sound creation accessible to everyone regardless of technical expertise. The platform enables creators to bring their audio visions to life in minutes instead of hours or days.

Ready to transform your ideas into professional audio? Start your AudioX journey today at [audiox.app](https://audiox.app/).
'''

setup(
    name='minimal_gq',
    # See https://packaging.python.org/single_source_version/
    version=version,
    description='Transform any inspiration into professional audio in minutes with AudioX. Create stunning music and sound effects with AudioX AI technology.',
    long_description=project_description,
    long_description_content_type='text/markdown',
    url='https://audiox.app/',
    author='GaoQ1',
    author_email='gaoquan199035@gmail.com',
    license=license,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='audio, ai, music, sound effects, generation, audioX',
    packages=find_packages(exclude=['test_*', 'docs']),
    extras_require={
        'dev': ['pytest'],
    },
    package_data={
        '': ['VERSION.txt', 'LICENSE.txt']
    },
)