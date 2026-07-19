#!/usr/bin/env python3
"""Offline regression tests for check_claims._probe_url.

The URL liveness probe once declared two live sites dead — including a UK
government-backed equality helpline — because it only tried the apex host and
treated any connection failure as death. These tests pin that behavior so it
cannot regress. All network calls are stubbed; this runs anywhere, no sockets.

Run: python3 scripts/test_check_claims.py
"""
import socket
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_claims as cc  # noqa: E402


class FakeResp:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def make_urlopen(behavior):
    """behavior: host -> ('ok', status) | ('http', code) | ('dns',) | ('refused',)."""
    def fake(req, timeout=None):
        host = urllib.parse.urlsplit(req.full_url).hostname
        act = behavior.get(host)
        if act is None:
            raise urllib.error.URLError(socket.gaierror("Name or service not known"))
        if act[0] == "ok":
            return FakeResp(act[1])
        if act[0] == "http":
            raise urllib.error.HTTPError(req.full_url, act[1], "", {}, None)
        if act[0] == "dns":
            raise urllib.error.URLError(socket.gaierror("Name or service not known"))
        if act[0] == "refused":
            raise urllib.error.URLError(ConnectionRefusedError("Connection refused"))
        raise AssertionError(act)
    return fake


import urllib.parse  # noqa: E402  (after helpers, used by make_urlopen)


class ProbeUrlTests(unittest.TestCase):
    def probe(self, behavior, url):
        with mock.patch.object(urllib.request, "urlopen", make_urlopen(behavior)):
            return cc._probe_url(url, timeout=5)

    def test_apex_dead_but_www_live_is_clean(self):
        # THE regression: apex has no DNS, www. answers. Site is alive.
        r = self.probe(
            {"www.equalityadvisoryservice.com": ("ok", 200)},
            "https://equalityadvisoryservice.com",
        )
        self.assertIsNone(r, f"apex-only live site wrongly flagged: {r}")

    def test_no_dns_anywhere_is_dead(self):
        r = self.probe({}, "https://adapt-canada.ca")
        self.assertIsNotNone(r)
        self.assertEqual(r[0], "org-url-dead")
        self.assertIn("DNS", r[1])

    def test_403_is_blocked_not_dead(self):
        r = self.probe({"ssa.gov": ("http", 403)}, "https://ssa.gov")
        self.assertEqual(r[0], "org-url-blocked")

    def test_plain_200_is_clean(self):
        r = self.probe({"acpanow.com": ("ok", 200)}, "https://acpanow.com")
        self.assertIsNone(r)

    def test_connection_refused_is_unreachable_not_dead(self):
        # We couldn't connect, but DNS resolved — may be us, not the site.
        r = self.probe(
            {"canadabusiness.ca": ("refused",), "www.canadabusiness.ca": ("refused",)},
            "https://canadabusiness.ca",
        )
        self.assertIsNotNone(r)
        self.assertEqual(r[0], "org-url-unreachable")

    def test_head_405_falls_back_to_get(self):
        calls = {"n": 0}
        real = make_urlopen({"example.org": ("ok", 200)})

        def counting(req, timeout=None):
            calls["n"] += 1
            if req.get_method() == "HEAD":
                raise urllib.error.HTTPError(req.full_url, 405, "", {}, None)
            return real(req, timeout=timeout)

        with mock.patch.object(urllib.request, "urlopen", counting):
            r = cc._probe_url("https://example.org", timeout=5)
        self.assertIsNone(r, "GET fallback after HEAD 405 should be clean")
        self.assertGreaterEqual(calls["n"], 2)

    def test_real_404_is_dead(self):
        r = self.probe(
            {"example.org": ("http", 404), "www.example.org": ("http", 404)},
            "https://example.org",
        )
        self.assertEqual(r[0], "org-url-dead")


if __name__ == "__main__":
    import warnings
    # Python 3.14 emits ResourceWarning for the file-like HTTPError objects our
    # mock raises. They are never opened against a real socket; the noise is
    # spurious and would undermine a test log meant to be read for trust.
    warnings.simplefilter("ignore", ResourceWarning)
    unittest.main(verbosity=2)
