import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.mark.asyncio
async def test_app_routes_and_cors():
    app = create_app(skip_lifespan_init=True)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Check root page
        root_resp = await client.get("/")
        assert root_resp.status_code == 200
        assert "TG Stremio" in root_resp.text
        assert "System Overview" in root_resp.text

        # Check admin dashboard page
        admin_resp = await client.get("/admin")
        assert admin_resp.status_code == 200
        assert "TG Stremio" in admin_resp.text

        # Check stremio manifest route exists
        manifest_resp = await client.get("/test_token/manifest.json")
        assert manifest_resp.status_code == 200
        manifest_data = manifest_resp.json()
        assert manifest_data["id"] == "community.telegram.stremio.v2"

        # Check multi-page template routes
        for page_path, expected_text in [
            ("/media/manage", "Media Library"),
            ("/settings", "Live Server Updates"),
            ("/tools", "Channel Scanner"),
            ("/tokens", "Tokens"),
        ]:
            resp = await client.get(page_path)
            assert resp.status_code == 200
            assert expected_text in resp.text

