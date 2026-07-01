import json
import traceback


def collect_failure_context(item, report, driver=None, api_response=None):
    """Build a text payload for the Failure Explainer from test state."""
    lines = [
        f"Test: {item.nodeid}",
        f"Outcome: {report.outcome}",
        f"Phase: {report.when}",
    ]

    if report.longrepr:
        lines.append(f"Error:\n{report.longrepr}")

    if driver is not None:
        try:
            lines.extend(
                [
                    f"URL: {driver.current_url}",
                    f"Title: {driver.title}",
                ]
            )
            error_el = driver.find_elements("css selector", "[data-test='error']")
            if error_el:
                lines.append(f"UI error message: {error_el[0].text}")

            source = driver.page_source[:3000]
            lines.append(f"Page source (truncated):\n{source}")
        except Exception as exc:
            lines.append(f"Could not collect browser state: {exc}")

    if api_response is not None:
        try:
            lines.append(f"API status: {api_response.status_code}")
            lines.append(f"API body:\n{api_response.text[:3000]}")
        except Exception as exc:
            lines.append(f"Could not collect API response: {exc}")

    stored = getattr(item, "stored_api_response", None)
    if stored is not None:
        lines.append(f"Stored API status: {stored.status_code}")
        lines.append(f"Stored API body:\n{stored.text[:3000]}")

    lines.append(f"Traceback:\n{traceback.format_exc()}")
    return "\n".join(lines)


def format_api_request(method, url, payload=None, response=None):
    parts = [f"{method.upper()} {url}"]
    if payload is not None:
        parts.append(f"Request body: {json.dumps(payload, indent=2)}")
    if response is not None:
        parts.append(f"Status: {response.status_code}")
        parts.append(f"Response: {response.text[:2000]}")
    return "\n".join(parts)
