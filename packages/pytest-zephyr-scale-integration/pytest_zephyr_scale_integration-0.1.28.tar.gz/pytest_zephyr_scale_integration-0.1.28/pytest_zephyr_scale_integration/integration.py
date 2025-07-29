import os
import time
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
import requests
from requests import HTTPError
from requests_toolbelt.utils import dump


JIRA_TOKEN = None
JIRA_PROJECT_ID = None
JIRA_URL = None


class Integration:
    def __init__(self, jira_token):
        self.session = requests.Session()
        self.max_retries = 5  # Максимальное количество повторных попыток
        self.retry_delay = 1  # Начальная задержка перед повторной попыткой (в секундах)

        self.JIRA_TOKEN = jira_token
        self.JIRA_PROJECT_ID = None
        self.JIRA_URL = None
        self.folder_name = None

        # Установка заголовков для сессии
        self.session.headers.update({
            'Authorization': f'Bearer {self.JIRA_TOKEN}',
            'Content-Type': 'application/json'
        })

    def load_environment_variables(self):
        """Загрузка переменных окружения из .env файла"""

        load_dotenv()

        # Получение значений из переменных окружения
        self.JIRA_PROJECT_ID = int(os.getenv("JIRA_PROJECT_ID"))
        self.JIRA_URL = os.getenv("JIRA_URL")
        self.folder_name = os.getenv("FOLDER_NAME", None)

        # Проверка на наличие обязательных переменных
        missing_env_vars = [var for var in ["JIRA_TOKEN", "JIRA_PROJECT_ID", "JIRA_URL"] if not getattr(self, var)]
        if missing_env_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_env_vars)}")
        else:
            print(
                f'Переменные загружены: {self.JIRA_TOKEN} \t {self.JIRA_PROJECT_ID} \t '
                f'{self.JIRA_URL} \t {self.JIRA_PROJECT_ID}')

    def _send_request_with_retries(self, method, url, **kwargs):
        """Отправка запроса с повторными попытками при статусе 429"""

        retries = 0
        while retries < self.max_retries:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 429:
                retries += 1
                wait_time = self.retry_delay * (2 ** (retries - 1))  # Экспоненциальная задержка
                print(f"Превышен лимит количества отправленный сообщений. "
                      f"Ожидаю {wait_time} секунд до повторной отправки...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()
                return response
        raise HTTPError(f"Не удалось выполнить запрос после {self.max_retries} "
                        f"попыток из-за ограничений скорости отправки запросов.")

    def get_project_key_by_project_id(self):
        """Получение ключа проекта по его ID"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/project/{self.JIRA_PROJECT_ID}"
        response = self.session.get(url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json().get('key')

    def create_test_cycle(self, cycle_name, folder_id=None):
        """Создание тестового цикла"""
        test_cycle_statuses = self.get_test_cycle_statuses()
        test_cycle_status_id = None
        for test_cycle_status in test_cycle_statuses:
            if test_cycle_status.get('name').lower() == 'not executed':
                test_cycle_status_id = test_cycle_status.get('id')

        now_utc = datetime.now(timezone.utc)
        formatted_time = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        url = f"{self.JIRA_URL}/rest/tests/1.0/testrun"
        payload = {
            "name": cycle_name,
            "projectId": self.JIRA_PROJECT_ID,
            "statusId": test_cycle_status_id if not test_cycle_status_id else test_cycle_statuses[0].get('id'),
            "plannedStartDate": formatted_time,
            "plannedEndDate": formatted_time
        }

        if folder_id:
            payload["folderId"] = folder_id

        response = self.session.post(url, json=payload)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        test_run_id = response.json().get('id')  # ID созданного тестового цикла

        # Сохраняем в файл, чтобы потом получить в pipeline'е
        with open(".test_run_id", "w") as f:
            f.write(str(test_run_id))

        return test_run_id

    def create_test_run_folder(self, folder_name):
        """Создание новой папки для тестового цикла"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/folder/testrun"
        payload = {
            "name": folder_name,
            "projectId": self.JIRA_PROJECT_ID,
            "index": 0
        }
        response = self._send_request_with_retries('POST', url, json=payload)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json().get('id')  # Возвращаем ID новой папки

    def get_test_run_folders(self):
        """Получение дерева папок тестовых циклов"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/project/{self.JIRA_PROJECT_ID}/foldertree/testrun"
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        return response.json()

    def get_test_case_id(self, project_key, test_case_key):
        """Получение ID тест-кейса по ключу проекта и ключу тест-кейса"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/testcase/{project_key}-{test_case_key}?fields=id"
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json().get('id')

    def get_test_run_id(self, test_cycle_key):
        """Получение ID тестового цикла"""
        url = f"{self.JIRA_URL}/rest/tests/1.0/testrun/{test_cycle_key}?fields=id"
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json().get('id')

    def add_test_cases_to_cycle(self, test_run_id, test_case_ids, user_key=None):
        """Добавление тест-кейсов в тестовый цикл"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/testrunitem/bulk/save"

        if user_key:
            added_test_run_items = [
                {"index": i, "lastTestResult": {"testCaseId": test_case_id}, "assignedTo": user_key}
                for i, test_case_id in enumerate(test_case_ids)
            ]
        else:
            added_test_run_items = [
                {"index": i, "lastTestResult": {"testCaseId": test_case_id}}
                for i, test_case_id in enumerate(test_case_ids)
            ]
        payload = {
            "testRunId": test_run_id,
            "addedTestRunItems": added_test_run_items
        }
        response = self._send_request_with_retries('PUT', url, json=payload)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()

    def get_test_run_items(self, test_run_id):
        """Получение всех тестов из тестового цикла"""

        url = (f"{self.JIRA_URL}/rest/tests/1.0/testrun/{test_run_id}/testrunitems?"
               f"fields=testCaseId,testScriptResults(id),testRunId")
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json().get('testRunItems', [])

    def get_test_script_results(self, test_run_id, item_id):
        """Получение результатов тестовых скриптов (параметризованных ТК)"""

        url = (f"{self.JIRA_URL}/rest/tests/1.0/testrun/{test_run_id}"
               f"/testresults?fields=testScriptResults(id,parameterSetId)&itemId={item_id}")
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json()

    def get_test_statuses(self):
        """Получение статусов для тест-кейсов"""

        url = f'{self.JIRA_URL}/rest/tests/1.0/project/{self.JIRA_PROJECT_ID}/testresultstatus'
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json()

    def get_test_cycle_statuses(self):
        """Получение статусов для тестового цикла"""
        url = f'{self.JIRA_URL}/rest/tests/1.0/project/{self.JIRA_PROJECT_ID}/testrunstatus'
        response = self._send_request_with_retries('GET', url)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()
        return response.json()


    def set_test_case_statuses(self, statuses):
        """Установка статусов для тест-кейсов"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/testresult"
        response = self._send_request_with_retries('PUT', url, json=statuses)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()

    def set_test_script_statuses(self, script_statuses):
        """Установка статусов для шагов тест-кейсов"""

        url = f"{self.JIRA_URL}/rest/tests/1.0/testscriptresult"
        response = self._send_request_with_retries('PUT', url, json=script_statuses)

        data = dump.dump_all(response)
        print(data.decode('utf-8'))

        response.raise_for_status()

    def get_user_key_by_email(self, email: str) -> Optional[str]:
        """Получение Jira userKey по email"""
        url = f"{self.JIRA_URL}/rest/api/2/user/search?username={email}"
        response = self._send_request_with_retries('GET', url)
        response.raise_for_status()
        users = response.json()
        if users and isinstance(users, list):
            return users[0].get("key")  # например, JIRAUSERXXXXXX
        return None
