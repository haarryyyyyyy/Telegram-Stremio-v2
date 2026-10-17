import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.mark.asyncio
async def test_app_routes_and_cors():
    app = create_app(skip_lifespan_init=True)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Check root redirect to /admin
        root_resp = await client.get("/")
        assert root_resp.status_code in (200, 307, 308)

        # Check admin dashboard page
        admin_resp = await client.get("/admin")
        assert admin_resp.status_code == 200
        assert "Telegram Stremio V2" in admin_resp.text

        # Check stremio manifest route exists
        manifest_resp = await client.get("/test_token/manifest.json")
        assert manifest_resp.status_code == 200
        manifest_data = manifest_resp.json()
        assert manifest_data["id"] == "community.telegram.stremio.v2"

        # Check legacy redirects to admin tabs
        for legacy_path, target_tab in [
            ("/media/manage", "/admin#media"),
            ("/settings", "/admin#settings"),
            ("/tools", "/admin#tools"),
            ("/tokens", "/admin#tokens"),
            ("/bots", "/admin#bots"),
        ]:
            legacy_resp = await client.get(legacy_path, follow_redirects=False)
            assert legacy_resp.status_code in (307, 308, 302, 301)
            assert legacy_resp.headers["location"] == target_tab

