from yookassa import Payment, Configuration
import uuid
import json
import logging
# from config_data.config import load_yookassa_config

# config = load_yookassa_config('.env')


logger = logging.getLogger(__name__)
format='[%(asctime)s] #%(levelname)-15s %(filename)s: %(lineno)d - %(pathname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

ACCOUNT_ID=1148677
SECRET_KEY="test_esP38iWHxikeiA49V7WsSaaDTT61i5fcCuEdv4fnEe0"

Configuration.account_id = ACCOUNT_ID
Configuration.secret_key = SECRET_KEY


class PaymentYoo:
    def __init__(self):
        self.id = None
        self.link = None

    async def create_payment(self, amount: int, plan: str, email: str):
        payment_id = uuid.uuid4()
        try:
            payment = Payment.create({
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://t.me/ivvpnbot"
                },
                "capture": True,
                "description": "Подписка на VPN. В боте @ivvpnbot",
                "receipt": {
                    "customer": {
                            "email": email # Обязательно для отправки чека
                        },
                        "items": [
                            {
                                "description": plan,
                                "quantity": 1.0,
                                "amount": {
                                    "value": amount,
                                    "currency": "RUB"
                                },
                                "vat_code": "2" # Код НДС, например "2" для "без НДС"
                            }
                        ]
                }
            }, payment_id)
            payment_data = json.loads(payment.json())
            self.id = payment_data['id']
            self.link = payment.confirmation.confirmation_url # type: ignore
            return self.link
        except Exception as e:
            logger.warning(f'Ошибка создания платежа: {e}')

        return None