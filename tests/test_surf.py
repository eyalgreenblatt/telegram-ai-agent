from surf_tools import get_surf_forecast

def test_surf_returns_tuple():
    report, hours = get_surf_forecast("tel aviv", 1, "en")
    assert isinstance(report, str)

def test_surf_hours_type():
    report, hours = get_surf_forecast("tel aviv", 1, "en")
    assert isinstance(hours, list)

def test_hebrew_mode():
    report, hours = get_surf_forecast("habonim", 1, "he")
    assert "גלישה" in report or "תחזית" in report
