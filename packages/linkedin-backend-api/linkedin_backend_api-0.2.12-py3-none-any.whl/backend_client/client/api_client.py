from aiohttp import ClientSession, ClientError, ClientTimeout
from typing import Dict, List, Optional, Any, Union, TypeVar, Generic, Type
import json
from pydantic import BaseModel
from datetime import datetime

# Import models from the models module
from backend_client.models import (
    User, UserBotSettings, UserCreateDTO, UserSearchSettings, 
    Vacancy, Location, AIFilter, 
    PromptInput, OutputJson, RelevanceInput, RelevanceOutput,
    Notification
)

PROMPT_TO_JSON = "/ai/prompt-to-json"
OPTIMIZE_DESCRIPTION = "/ai/optimize-description"
SCORE_VACANCY = "/ai/score-vacancy"
USERS = "/users/"
VACANCIES = "/vacancies/"
TELEGRAM_SEND_MESSAGE = "/telegram/send_message"

# Type variable for generic response models
T = TypeVar('T', bound=BaseModel)


class ApiError(Exception):
    """Base class for all API errors."""
    def __init__(self, status_code: int, message: str, details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"API Error [{status_code}]: {message}")


class NotFoundError(ApiError):
    """Error 404 - resource not found."""
    def __init__(self, message: str = "Resource not found", details: Any = None):
        super().__init__(404, message, details)


class ConflictError(ApiError):
    """Error 409 - conflict (e.g., resource already exists)."""
    def __init__(self, message: str = "Resource conflict", details: Any = None):
        super().__init__(409, message, details)


class BadRequestError(ApiError):
    """Error 400 - bad request."""
    def __init__(self, message: str = "Bad request", details: Any = None):
        super().__init__(400, message, details)


class UnauthorizedError(ApiError):
    """Error 401 - unauthorized."""
    def __init__(self, message: str = "Unauthorized", details: Any = None):
        super().__init__(401, message, details)


class ForbiddenError(ApiError):
    """Error 403 - access forbidden."""
    def __init__(self, message: str = "Forbidden", details: Any = None):
        super().__init__(403, message, details)


class ServerError(ApiError):
    """Errors 5xx - server errors."""
    def __init__(self, status_code: int = 500, message: str = "Server error", details: Any = None):
        super().__init__(status_code, message, details)


class ConnectionError(ApiError):
    """Error connecting to the server."""
    def __init__(self, message: str = "Connection error", details: Any = None):
        super().__init__(0, message, details)


class ResponseMessage(BaseModel):
    """Generic response message model."""
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = ClientSession(timeout=ClientTimeout(total=240))
        
    async def close(self):
        await self.session.close()
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def _process_response(self, response):
        if response.status >= 400:
            details = None
            try:
                details = await response.json()
            except:
                details = await response.text()
            
            # Create appropriate error class based on status code
            if response.status == 404:
                raise NotFoundError(response.reason, details)
            elif response.status == 409:
                raise ConflictError(response.reason, details)
            elif response.status == 400:
                raise BadRequestError(response.reason, details)
            elif response.status == 401:
                raise UnauthorizedError(response.reason, details)
            elif response.status == 403:
                raise ForbiddenError(response.reason, details)
            elif response.status >= 500:
                raise ServerError(response.status, response.reason, details)
            else:
                raise ApiError(response.status, response.reason, details)
            
        try:
            return await response.json()
        except:
            return await response.text()
            
    async def _process_model_response(self, response, model_class: Type[T]) -> T:
        """Process response and convert it to a Pydantic model."""
        print(await response.text())
        data = await self._process_response(response)
        if isinstance(data, dict):
            return model_class.model_validate(data)
        raise ApiError(response.status, f"Cannot convert response to {model_class.__name__}", data)
            
    async def _process_model_list_response(self, response, model_class: Type[T]) -> List[T]:
        """Process response and convert it to a list of Pydantic models."""
        data = await self._process_response(response)
        if isinstance(data, list):
            return [model_class.model_validate(item) for item in data]
        raise ApiError(response.status, f"Cannot convert response to List[{model_class.__name__}]", data)
            
    async def prompt_to_json(self, prompt: str) -> OutputJson:
        """Convert prompt to JSON using AI."""
        url = f"{self.base_url}{PROMPT_TO_JSON}"
        payload = PromptInput(prompt=prompt)
        try:
            async with self.session.post(url, json=payload.model_dump()) as response:
                return await self._process_model_response(response, OutputJson)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def optimize_description(self, prompt: str) -> OutputJson:
        """Optimize description using AI."""
        url = f"{self.base_url}{OPTIMIZE_DESCRIPTION}"
        payload = PromptInput(prompt=prompt)
        try:
            async with self.session.post(url, json=payload.model_dump()) as response:
                return await self._process_model_response(response, OutputJson)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def score_vacancy(self, user_requirements: str, vacancy_text: str, additional_info: str = "") -> RelevanceOutput:
        """Score vacancy relevance using AI."""
        url = f"{self.base_url}{SCORE_VACANCY}"
        payload = RelevanceInput(
            user_requirements=user_requirements,
            vacancy_text=vacancy_text,
            additional_info=additional_info
        )
        try:
            async with self.session.post(url, json=payload.model_dump()) as response:
                return await self._process_model_response(response, RelevanceOutput)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def get_users(self, only_with_search_settings: bool = False) -> List[User]:
        """Get all users."""
        url = f"{self.base_url}{USERS}"
        params = {"only_with_search_settings": str(only_with_search_settings).lower()}
        try:
            async with self.session.get(url, params=params) as response:
                return await self._process_model_list_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def create_user(self, user_id: int, bot_settings: Optional[UserBotSettings] = None) -> User:
        """Create a new user."""
        url = f"{self.base_url}{USERS}"
        create_dto = UserCreateDTO(user_id=user_id, bot_settings=bot_settings)
        try:
            async with self.session.post(url, json=create_dto.model_dump(exclude_none=True)) as response:
                return await self._process_model_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        url = f"{self.base_url}{USERS}{user_id}"
        try:
            async with self.session.get(url) as response:
                if response.status == 404:
                    return None
                return await self._process_model_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def update_language(self, user_id: int, language: str) -> User:
        """Update user language."""
        url = f"{self.base_url}{USERS}{user_id}/language"
        params = {"language": language}
        try:
            async with self.session.put(url, params=params) as response:
                return await self._process_model_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def update_onboarding_status(self, user_id: int, status: bool) -> User:
        """Update user onboarding status."""
        url = f"{self.base_url}{USERS}{user_id}/onboarding_status"
        params = {"status": str(status).lower()}
        try:
            async with self.session.put(url, params=params) as response:
                return await self._process_model_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def update_search_settings(self, user_id: int, settings: UserSearchSettings) -> UserSearchSettings:
        """Update user search settings."""
        url = f"{self.base_url}{USERS}{user_id}/search_settings"
        try:
            settings_data = settings.model_dump(exclude_none=True)
            async with self.session.put(url, json=settings_data) as response:
                return await self._process_model_response(response, UserSearchSettings)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
    
    async def remove_search_settings(self, user_id: int) -> None:
        """Remove user search settings."""
        url = f"{self.base_url}{USERS}{user_id}/search_settings"
        try:
            async with self.session.delete(url) as response:
                return await self._process_model_response(response, User)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
                
    
    async def update_last_run(self, user_id: int) -> None:
        """Update last run."""
        url = f"{self.base_url}{USERS}{user_id}/last_run"
        try:
            async with self.session.put(url) as response:
                return await self._process_model_response(response, ResponseMessage)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
    
    async def get_all_vacancies(self) -> List[Vacancy]:
        """Get all vacancies."""
        url = f"{self.base_url}{VACANCIES}"
        try:
            async with self.session.get(url) as response:
                return await self._process_model_list_response(response, Vacancy)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def get_vacancy(self, vacancy_id: str) -> Optional[Vacancy]:
        """Get vacancy by ID."""
        url = f"{self.base_url}{VACANCIES}{vacancy_id}"
        try:
            async with self.session.get(url) as response:
                if response.status == 404:
                    return None
                return await self._process_model_response(response, Vacancy)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def update_vacancy(self, vacancy_id: str, vacancy_data: Dict[str, Any]) -> Vacancy:
        """Update vacancy."""
        url = f"{self.base_url}{VACANCIES}{vacancy_id}"
        try:
            async with self.session.put(url, json=vacancy_data) as response:
                return await self._process_model_response(response, Vacancy)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")

    
    async def add_vacancy(self, vacancy_data: Vacancy) -> Vacancy:
        """Add a new vacancy."""
        url = f"{self.base_url}{VACANCIES}"
        try:
            data = vacancy_data.model_dump(exclude_none=True)
            async with self.session.post(url, json=data) as response:
                return await self._process_model_response(response, Vacancy)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def send_telegram_message(self, notification: Notification) -> ResponseMessage:
        """Send telegram message using a Notification object."""
        url = f"{self.base_url}{TELEGRAM_SEND_MESSAGE}"
        try:
            async with self.session.post(url, json=notification.model_dump(exclude_none=True)) as response:
                return await self._process_model_response(response, ResponseMessage)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
            
    async def get_or_create_user(self, user_id: int, bot_settings: Optional[UserBotSettings] = None) -> User:
        """Get a user or create if not exists."""
        try:
            user = await self.get_user(user_id)
            if not user:
                return await self.create_user(user_id, bot_settings)
            return user
        except ConflictError as e:
            if isinstance(e.details, dict) and e.details.get('detail') == 'User already exists':
                return await self.get_user(user_id)
            raise

    async def get_notification(self, user_id: int, job_id: str) -> Optional[Notification]:
        """Get notification by user ID and job ID."""
        url = f"{self.base_url}/telegram/notifications/{user_id}/{job_id}"
        try:
            async with self.session.get(url) as response:
                if response.status == 404:
                    return None
                return await self._process_model_response(response, Notification)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
    
    async def save_notification(self, notification: Notification) -> ResponseMessage:
        """Save notification to the database."""
        url = f"{self.base_url}/telegram/notifications/save"
        try:
            async with self.session.post(url, json=notification.model_dump(exclude_none=True)) as response:
                return await self._process_model_response(response, ResponseMessage)
        except ClientError as e:
            raise ConnectionError(f"Connection error: {str(e)}")
        
        