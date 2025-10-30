import aiohttp
import asyncio
from config_data.config import settings as s
from logger_setup import logger

MARZ_DATA = (s.M_DIGITAL_U, s.M_DIGITAL_P, s.M_DIGITAL_URL)

class BackendContext:
    def __init__(self, user: str, password: str, url: str):
        self.user = user
        self.password = password
        self.base_url = url
        self.token = None
        self.headers = {"accept": "application/json"}
        self.session = None
    
    async def __aenter__(self):
        """Вход в контекстный менеджер"""
        self.session = aiohttp.ClientSession()

        if not self.headers.get("Authorization"):
            await self._authorize()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера"""
        await self._cleanup_session()
    
    async def _cleanup_session(self):
        """Правильное закрытие сессии"""
        if self.session and not self.session.closed:
            try:
                await self.session.close()
                # Даем время на закрытие соединений
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"Ошибка при закрытии сессии: {e}")
            finally:
                self.session = None
                self._authorized = False
                logger.debug(f"Сессия закрыта")
    
    async def _authorize(self):
            data = {
                "username": self.user,
                "password": self.password
            }

            async with self.session.post( #type: ignore
                        url=f"{self.base_url}/api/admin/token",
                        data=data) as result:
                
                if result.status == 200:
                    json_data = await result.json()
                    token = json_data.get("access_token")
                    self.headers["Authorization"] = f"Bearer {token}"
                    logger.info(f"Токен получен: {token[:10]}")
                else:
                    logger.warning(f"Ошибка авторизации: {result.status}")
    

    async def get_user(self, id):
        id = str(id)
        get_route = f"/api/user/{id}"

        async with self.session as session: #type: ignore
            request = await session.get(
                url= self.base_url + get_route,
                headers=self.headers
            )

            if request.status not in (200, 201):
                logger.warning(f"Ошибка в редактирование пользовтеля {id}")
                return None

            json_data = await request.json()
            return json_data
    

    async def modify_user(self, id: str, expire: int):
        get_route = f"/api/user/{id}"

        data = {
            "expire": expire
        }

        async with self.session as session: #type: ignore
            request = await session.put(
                url= self.base_url + get_route,
                headers=self.headers,
                json=data
            )

            if request.status not in (200, 201):
                logger.warning(f"Ошибка в редактирование пользовтеля {id}")
                return None
            
            json_data = await request.json()
            logger.info(json_data)
            return json_data
    
    async def create_user(self, username):
        username = str(username)

        get_route = f"/api/user/"
        data = {
            "username": username,
            "proxies": {
                "vless": {
                    "flow": "xtls-rprx-vision"
                }
            },
            "inbounds": {
                "vless": [
                "VLESS TCP REALITY",
                ]
            }
        }

        async with self.session as session: #type: ignore
            request = await session.post(
                url= self.base_url + get_route,
                headers=self.headers, 
                json=data
            )
            
            if request.status not in (200, 201):
                logger.warning(f"Ошибка в создании пользовтеля")
                return None

            json_data = await request.json()
            logger.info(json_data)
            return json_data