import httpx

API_HOST = "localhost"
API_PORT = 5000
API_ENDPOINT = "data"

api_url = f"http://{API_HOST}:{API_PORT}/{API_ENDPOINT}/"

date_to_analyze = "15/03/2025"

response = httpx.request(
  method="GET",
  url=api_url,
  params={"day": date_to_analyze}
)

print(response.json())