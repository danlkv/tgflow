from setuptools import setup
setup(
      name = 'tgflow',
      packages = ['tgflow',
                  'tgflow.api',
                  'tgflow.api.whatsapp',
                  'tgflow.actions',
                  'tgflow.modules',
                 ],
      version = '0.4.2',
      description = 'A declarative-style telegram bot framework',
      author = 'Danil Lykov',
      author_email = 'lkvdan@gmail.com',
      url = 'https://github.com/DaniloZZZ/tgflow',
      download_url = 'https://github.com/DaniloZZZ/tgflow/archive/0.1.tar.gz',
      install_requires=['pyTelegramBotAPI', 'gspread', 'oauth2client', 'requests', 'bitrix24-python3-client'],
      python_requires='>=3.3',
      license='MIT',
      keywords = ['tools', 'telegram', 'framework', 'bot'], # arbitrary keywords
      classifiers = [],
)
