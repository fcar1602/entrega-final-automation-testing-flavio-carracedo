import os
import time
import base64
import pytest
import logging
import io
from entregaFinal.utils.api_utils import APIClient
from selenium import webdriver
import pytest
from faker import Faker
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,

        "autofill.profile_enabled": False,
        "autofill.password_manager_enabled": False,
        "autofill.credit_card_enabled": False,
        "autofill.address_enabled": False,

        "profile.password_manager_leak_detection": False,
    }

    options.add_experimental_option("prefs", prefs)

    options.add_argument(
        "--disable-features=PasswordManagerEnabled,PasswordManagerUI"
    )

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()



# fixture for Faker instance
@pytest.fixture(scope="session")
def fake():
    return Faker()

# fixture for APIClient instance
@pytest.fixture(scope="session")
def api():
    return APIClient("https://dummyjson.com")

# optional logger fixture (kept as fallback)
@pytest.fixture
def logger(request):
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    handler.setLevel(logging.INFO)

    lg = logging.getLogger(f"test.{request.node.name}")
    lg.setLevel(logging.INFO)
    lg.addHandler(handler)
    lg.propagate = False

    yield lg

    handler.flush()
    # store logs on node as fallback (if caplog is not used)

    request.node._captured_log = buf.getvalue()
    lg.removeHandler(handler)
    try:
        buf.close()
    except Exception:
        pass

def _ensure_report_extras(rep):
    """Ensures and returns the list of 'extras' compatible with new/old versions."""
    if hasattr(rep, "extras"):
        cur = getattr(rep, "extras", None)
        if cur is None:
            rep.extras = []
            return rep.extras
        if not isinstance(cur, list):
            rep.extras = list(cur)
        return rep.extras
    else:
        cur = getattr(rep, "extra", None)
        if cur is None:
            rep.extra = []
            return rep.extra
        if not isinstance(cur, list):
            rep.extra = list(cur)
        return rep.extra

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # only during the "call" phase

    if rep.when != "call":
        return

    extras = _ensure_report_extras(rep)

    # obtain html plugin safely
    try:
        plugin_html = item.config.pluginmanager.get_plugin("html")
    except Exception:
        plugin_html = None

    # 1) traceback if failed

    try:
        if rep.failed:
            long_text = getattr(rep, "longreprtext", None) or str(getattr(rep, "longrepr", ""))
            if long_text:
                if plugin_html:
                    extras.append(plugin_html.extras.text("FAILURE TRACEBACK:\n" + long_text))
                else:
                    extras.append("FAILURE TRACEBACK:\n" + long_text)
    except Exception:
        pass

    # 2) logs: preferir caplog (pytest builtin), luego fallback a request.node._captured_log

    try:
        caplog = item.funcargs.get("caplog")
        caplog_text = None
        if caplog:
            # caplog.text contains everything captured

            try:
                caplog_text = getattr(caplog, "text", None) or "\n".join(r.getMessage() for r in getattr(caplog, "records", []))
            except Exception:
                caplog_text = None

        captured = caplog_text or getattr(item, "_captured_log", None)
        if captured:
            if plugin_html:
                extras.append(plugin_html.extras.text("TEST LOGS:\n" + captured))
            else:
                extras.append("TEST LOGS:\n" + captured)
    except Exception:
        pass

    # 3) screenshot + URL + title
    try:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            fname = f"{item.name}_{rep.outcome}_{int(time.time())}.png"
            path = os.path.join(screenshots_dir, fname)

            try:
                driver.save_screenshot(path)
            except Exception:
                path = None

            if path and plugin_html:
                try:
                    with open(path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    try:
                        extras.append(plugin_html.extras.png(b64))
                    except Exception:
                        try:
                            extras.append(plugin_html.extras.image(path))
                        except Exception:
                            extras.append(plugin_html.extras.text(f"Screenshot saved: {path}"))
                    # Context

                    try:
                        extras.append(plugin_html.extras.text(f"URL: {driver.current_url}"))
                        extras.append(plugin_html.extras.text(f"Title: {driver.title}"))
                    except Exception:
                        pass
                except Exception:
                    extras.append(plugin_html.extras.text(f"Screenshot saved: {path}"))
            elif path:
                extras.append(f"Screenshot saved: {path}")
    except Exception:
        pass