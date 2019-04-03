from setuptools import setup
setup(
      name = 'tgflow',
      packages = ['tgflow','tgflow.api'],
      version = '0.3.7a1',
      description = 'A declarative-style telegram bot framework',
      author = 'Danil Lykov',
      author_email = 'lkvdan@gmail.com',
      url = 'https://github.com/DaniloZZZ/tgflow',
      download_url = 'https://github.com/DaniloZZZ/tgflow/archive/0.1.tar.gz',
      install_requires=['pyTelegramBotAPI'],
      python_requires='>=3.3',
      license='MIT',
      keywords = ['tools', 'telegram', 'framework', 'bot'], # arbitrary keywords
      classifiers = [],
)
