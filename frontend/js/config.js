/**
 * config.js
 * ---------------------------------------------------------------------------
 * ONE FLAG to flip when Person C's real backend is ready.
 *
 * USE_MOCK = true   -> all calls are served by js/mockApi.js (in-memory,
 *                       no network) so the frontend can be built and demoed
 *                       before Person C's service exists.
 * USE_MOCK = false  -> all calls go to BASE_URL over HTTP, using the exact
 *                       same request/response shapes the mock uses. No other
 *                       file needs to change.
 *
 * When Person C hands off real endpoints, set USE_MOCK = false and point
 * BASE_URL at their service. If their route paths differ from the ones
 * below, adjust only the paths inside api.js — app.js never talks to fetch()
 * directly, so the UI layer is unaffected either way.
 * ---------------------------------------------------------------------------
 */
const CONFIG = {

  USE_MOCK: false,

  BASE_URL:
    "http://127.0.0.1:8000",

  MOCK_LATENCY_MS:
    250,

};