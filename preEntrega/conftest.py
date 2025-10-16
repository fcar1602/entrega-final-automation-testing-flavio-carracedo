import os
import time
import base64
import pytest
import logging
import io
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")
    # DEBUG: confirmar que conftest se cargó
    print("[DEBUG] conftest.py loaded, pytest_html =", bool(pytest_html))
    import sys; sys.stdout.flush()

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
    # almacenar logs en el nodo como fallback (si caplog no se usa)
    request.node._captured_log = buf.getvalue()
    lg.removeHandler(handler)
    try:
        buf.close()
    except Exception:
        pass

def _ensure_report_extras(rep):
    """Asegura y devuelve la lista de 'extras' compatible con versiones nuevas/antiguas."""
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

    # solo durante la fase "call"
    if rep.when != "call":
        return

    extras = _ensure_report_extras(rep)

    # 1) traceback si falló
    try:
        if rep.failed:
            long_text = getattr(rep, "longreprtext", None) or str(getattr(rep, "longrepr", ""))
            if long_text:
                if pytest_html:
                    extras.append(pytest_html.extras.text("FAILURE TRACEBACK:\n" + long_text))
                else:
                    extras.append("FAILURE TRACEBACK:\n" + long_text)
    except Exception:
        pass

    # 2) logs: preferir caplog (pytest builtin), luego fallback a request.node._captured_log
    try:
        caplog = item.funcargs.get("caplog")
        caplog_text = None
        if caplog:
            # caplog.text contiene todo lo capturado
            try:
                caplog_text = getattr(caplog, "text", None) or "\n".join(r.getMessage() for r in getattr(caplog, "records", []))
            except Exception:
                caplog_text = None

        captured = caplog_text or getattr(item, "_captured_log", None)
        if captured:
            if pytest_html:
                extras.append(pytest_html.extras.text("TEST LOGS:\n" + captured))
            else:
                extras.append("TEST LOGS:\n" + captured)
    except Exception:
        pass

    # 3) screenshot + URL + title (si hay driver fixture)
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

            if path and pytest_html:
                try:
                    with open(path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    try:
                        extras.append(pytest_html.extras.png(b64))
                    except Exception:
                        try:
                            extras.append(pytest_html.extras.image(path))
                        except Exception:
                            extras.append(pytest_html.extras.text(f"Screenshot saved: {path}"))
                    # contexto
                    try:
                        extras.append(pytest_html.extras.text(f"URL: {driver.current_url}"))
                        extras.append(pytest_html.extras.text(f"Title: {driver.title}"))
                    except Exception:
                        pass
                except Exception:
                    extras.append(pytest_html.extras.text(f"Screenshot saved: {path}"))
            elif path:
                extras.append(f"Screenshot saved: {path}")
    except Exception:
        pass