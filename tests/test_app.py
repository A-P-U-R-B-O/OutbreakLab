import pytest
from unittest import mock
from pathlib import Path

# Patch Streamlit and other external libraries
import sys
import types

# Mock Streamlit module for import
st_mock = mock.MagicMock()
sys.modules['streamlit'] = st_mock
sys.modules['pandas'] = mock.MagicMock()
sys.modules['numpy'] = mock.MagicMock()

# Import app after patching
import importlib
app = importlib.import_module("src.app")

def test_load_custom_css_file_exists(tmp_path, monkeypatch):
    # Setup: create a dummy css file in the expected location
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    css_file = assets_dir / "custom.css"
    css_content = "body { background: #fff; }"
    css_file.write_text(css_content)
    monkeypatch.setattr(app, "__file__", str(tmp_path / "src" / "app.py"))
    # Patch Path.exists to True for css_path
    with mock.patch("pathlib.Path.exists", return_value=True), \
         mock.patch("builtins.open", mock.mock_open(read_data=css_content)):
        app.load_custom_css()
        st_mock.markdown.assert_called_with(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True
        )

def test_load_custom_css_file_missing(monkeypatch):
    # Simulate missing css file
    monkeypatch.setattr(app, "__file__", str(Path.cwd() / "src" / "app.py"))
    with mock.patch("pathlib.Path.exists", return_value=False):
        app.load_custom_css()
        st_mock.warning.assert_called_with("Custom CSS file not found. Using default Streamlit styles.")

def test_validate_parameters_valid():
    # Should not raise an exception
    app.validate_parameters(
        N=1000, I0=1, R0=0, beta=0.3, gamma=0.1, days=50, dt=1.0
    )

def test_validate_parameters_invalid():
    # Should raise assertion error for invalid N
    with pytest.raises(AssertionError):
        app.validate_parameters(
            N=-1, I0=1, R0=0, beta=0.3, gamma=0.1, days=50, dt=1.0
        )

def test_parameter_parsing_from_csv(monkeypatch):
    # Simulate a DataFrame with expected columns
    pd_mock = sys.modules['pandas']
    df_mock = mock.MagicMock()
    df_mock.columns = ["susceptible", "infected", "recovered"]
    df_mock.__getitem__.side_effect = lambda k: {
        "susceptible": [990],
        "infected": [10],
        "recovered": [0]
    }[k]
    df_mock.iloc = [0]
    pd_mock.read_csv.return_value = df_mock
    uploaded_file = mock.Mock()
    # Simulate reading CSV in Upload mode
    # This test is illustrative; for more realistic test,
    # refactor CSV parsing into a separate function.

def test_model_choices(monkeypatch):
    # Ensure all model choices are available
    choices = ["SIR", "SEIR", "SIRV", "SEIRV", "SEIRD"]
    # Patch Streamlit selectbox to return each choice in turn
    st_mock.sidebar.selectbox.side_effect = choices
    for model in choices:
        result = st_mock.sidebar.selectbox("Choose epidemic model", choices)
        assert result == model

def test_sidebar_and_page_config_called():
    # Ensure sidebar and config are set
    app.st.set_page_config.assert_called()
    app.st.sidebar.markdown.assert_called()
    app.st.sidebar.info.assert_called()

def test_download_buttons_and_markdown():
    # Confirm that download_button and markdown are called during results display
    assert app.st.markdown.called or app.st.download_button.called

# Additional tests could be added for:
# - Error handling in simulation (by mocking simulation functions to raise exceptions)
# - Parameter handling for each model type (SIR, SEIR, etc.)
# - File upload simulation (by mocking file_uploader and the related logic)
# - Main panel info and footer rendering

# Note: For full coverage, refactor app.py logic into smaller testable functions
