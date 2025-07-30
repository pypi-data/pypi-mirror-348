import requests

BASE = "http://localhost:8000"

# 1. Create Admin
def create_admin():
    res = requests.post(f"{BASE}/admin/init", params={"username": "admin", "password": "adminpass"})
    print("Admin Init:", res.status_code, res.text)

# 2. Admin Login
def login_admin():
    res = requests.post(f"{BASE}/admin/login", json={"username": "admin", "password": "adminpass"})
    print("Admin Login:", res.status_code)
    return res.json()["access_token"]

# 3. Register Agent
def register_agent(admin_token):
    res = requests.post(
        f"{BASE}/agents/register",
        json={"agent_id": "agent007", "agent_secret": "topsecret"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print("Register Agent:", res.status_code, res.text)

# 4. Agent Login via /token (OAuth2)
def login_agent():
    res = requests.post(
        f"{BASE}/token",
        data={"username": "agent007", "password": "topsecret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print("Agent Login:", res.status_code)
    return res.json()["access_token"]

# 5. Get Agent Info (Protected)
def get_agent_info(agent_token):
    res = requests.get(f"{BASE}/me", headers={"Authorization": f"Bearer {agent_token}"})
    print("Agent Info:", res.status_code, res.json())

# 6. Admin lists all agents
def list_agents(admin_token):
    res = requests.get(f"{BASE}/admin/agents", headers={"Authorization": f"Bearer {admin_token}"})
    print("Agents List:", res.status_code, res.json())

# Run sequence
if __name__ == "__main__":
    create_admin()
    admin_token = login_admin()
    register_agent(admin_token)
    agent_token = login_agent()
    get_agent_info(agent_token)
    list_agents(admin_token)
