from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pass


class PaymentData(Base):
    __tablename__ = 'payment_data'

    payment_id: Mapped[str]
    status: Mapped[str] = mapped_column(server_default='pending')
    amount: Mapped[int]

    pass


class PaymentIDs(Base):
    __tablename__ = 'payment_ids'

    payment_id: Mapped[str]
    user_id: Mapped[str]



# {
#   "type": "notification",
#   "event": "payment.succeeded",
#   "object": {
#     "id": "3093c911-000f-5000-8000-1b2c39026a5c",
#     "status": "succeeded",
#     "amount": {
#       "value": "100.00",
#       "currency": "RUB"
#     },
#     "income_amount": {
#       "value": "96.50",
#       "currency": "RUB"
#     },
#     "description": "Подписка на VPN. В боте @ivvpnbot",
#     "recipient": {
#       "account_id": "1148677",
#       "gateway_id": "2520642"
#     },
#     "payment_method": {
#       "type": "yoo_money",
#       "id": "3093c911-000f-5000-8000-1b2c39026a5c",
#       "saved": false,
#       "status": "inactive",
#       "title": "YooMoney wallet 410011758831136",
#       "account_number": "410011758831136"
#     },
#     "captured_at": "2025-10-29T06:34:13.717Z",
#     "created_at": "2025-10-29T06:33:53.174Z",
#     "test": true,
#     "refunded_amount": {
#       "value": "0.00",
#       "currency": "RUB"
#     },
#     "paid": true,
#     "refundable": true,
#     "metadata": {
#       "cms_name": "yookassa_sdk_python"
#     }
#   }
# }