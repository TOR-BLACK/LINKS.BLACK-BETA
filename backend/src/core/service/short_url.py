from abc import ABC, abstractmethod

import requests
from loguru import logger
from sentry_sdk import capture_exception


class ShortUrlAbstract(ABC):

    @abstractmethod
    def get_url(self, url: str) -> str:
        raise NotImplementedError()


class ClickRuShortUrlAbstract(ShortUrlAbstract):
    API_URL = 'https://clck.ru/--'

    def get_url(self, url: str) -> str:
        try:
            response = requests.get(self.API_URL, params={'url': url}, verify=True, timeout=2)
            if response.ok:
                return response.text.strip().replace('https://', '')
            else:
                logger.error(f'Ошибка запроса CLCKRU status: {response.status_code} response: {response.text}')
            return url
        except Exception as e:
            logger.exception(e)
            capture_exception(e)
            return url


