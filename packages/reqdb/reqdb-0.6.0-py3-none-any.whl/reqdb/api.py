import requests


class API:

    def __init__(self, fqdn: str, bearer: str, insecure: bool = False) -> None:
        self.fqdn = fqdn
        self.headers = {
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        s = "s" if not insecure else ""
        self.baseURL = f"http{s}://{self.fqdn}/api"

    @staticmethod
    def handleResponse(response: requests.Response) -> dict|bool:
        if response.status_code in (200, 201):
            return response.json()["data"]
        elif response.status_code == 204:
            return True
        else:
            raise RuntimeError(response.json())

    def get(self, endpoint: str) -> dict|bool:
        response = requests.get(f"{self.baseURL}/{endpoint}", headers=self.headers)
        return API.handleResponse(response)

    def update(self, endpoint: str, data: dict) -> dict|bool:
        response = requests.patch(f"{self.baseURL}/{endpoint}", headers=self.headers, json=data)
        return API.handleResponse(response)

    def delete(self, endpoint: str, force: bool = False, cascade: bool = False) -> dict|bool:
        if not force and cascade:
            raise ValueError("Cascade can only be true when force is also true")
        parameters = ""
        if force:
            parameters += "?force=true"
            if cascade:
                parameters += "&cascade=true"
        response = requests.delete(f"{self.baseURL}/{endpoint}{parameters}", headers=self.headers)
        return API.handleResponse(response)

    def add(self, endpoint: str, data: dict) -> dict|bool:
        response = requests.post(f"{self.baseURL}/{endpoint}", headers=self.headers, json=data)
        return API.handleResponse(response)
