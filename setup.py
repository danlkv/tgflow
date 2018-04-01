from setuptools import setup
setup(
      name = 'tgflow',
      packages = ['tgflow'],
      version = '0.1.4rc',
      description = 'A declarative-style telegram bot framework',
      author = 'Danil Lykov',
      author_email = 'lkvdan@gmail.com',
      url = 'https://github.com/DaniloZZZ/tgflow',
      download_url = 'https://github.com/DaniloZZZ/tgflow/archive/0.1.tar.gz',
      install_requires=['telebot'],
      python_requires='>=3.3',
      license='MIT',
      keywords = ['tools', 'telegram', 'framework', 'bot'], # arbitrary keywords
      classifiers = [],
)
