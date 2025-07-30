from vais_mcp.config import Settings


def test_settings_initialization_with_required_env_vars(monkeypatch):
    expected_project_id = "test-project"
    expected_engine_id = "test-engine"
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT_ID", expected_project_id)
    monkeypatch.setenv("VAIS_ENGINE_ID", expected_engine_id)

    current_settings = Settings()

    assert current_settings.GOOGLE_CLOUD_PROJECT_ID == expected_project_id
    assert current_settings.VAIS_ENGINE_ID == expected_engine_id


def test_settings_default_values(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT_ID", "default-test-project")
    monkeypatch.setenv("VAIS_ENGINE_ID", "default-test-engine")

    current_settings = Settings()

    assert current_settings.IMPERSONATE_SERVICE_ACCOUNT is None
    assert current_settings.VAIS_LOCATION == "global"
    assert current_settings.PAGE_SIZE == 5
    assert current_settings.MAX_EXTRACTIVE_SEGMENT_COUNT == 2
    assert current_settings.LOG_LEVEL == "WARNING"
    assert current_settings.model_config.get("extra") == "ignore"
