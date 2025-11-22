import logging
import requests


logger = logging.getLogger(__name__)
CAT_API_URL = 'https://api.thecatapi.com/v1/breeds'


def normalize(text: str) -> str:
    return text.strip().lower()


def validate_breed(breed: str) -> bool:
    try:
        breed = normalize(breed)
        response = requests.get(CAT_API_URL, timeout=5)
        if response.status_code != 200:
            return False
        for item in response.json():
            if normalize(item['name']) == breed:
                return True

            alt = item.get('alt_names')
            if alt:
                alt_list = [normalize(a) for a in alt.split(',')]
                if breed in alt_list:
                    return True

        return False

    except Exception as e:
        logger.error(f'Error in getting breeds: {e}')
        return False
