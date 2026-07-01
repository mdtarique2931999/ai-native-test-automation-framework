# Prompts

Raw prompts used for LLM test generation. Copied exactly as written.

---

## Prompt 1 — Login module

```
You are a senior SDET writing regression tests for the Sauce Demo login page at https://www.saucedemo.com/.

Generate exactly 5 test cases covering:
1. Valid login
2. Invalid credentials
3. Forgot password
4. Session expiry
5. Brute-force lockout

Output format: JSON array with fields id, title, steps, expected, priority, tags.

Constraints:
- Use Sauce Demo usernames: standard_user, locked_out_user, problem_user
- Password is secret_sauce
- If a scenario is not supported by the app, adapt it and note the adaptation in the expected field
- Do not include markdown fences in the response
```

### Login module notes

First pass assumed a forgot-password link existed on Sauce Demo, which it does not. I changed the prompt to require adaptation for unsupported flows and mapped forgot password to a negative check for link absence. Session expiry also needed refinement because the app redirects to login rather than showing an explicit expiry message.

---

## Prompt 2 — Dashboard module

```
You are a senior SDET writing regression tests for the Sauce Demo inventory page (post-login dashboard) at https://www.saucedemo.com/inventory.html.

Generate exactly 5 test cases covering:
1. Widget loading
2. Data accuracy
3. Filter/sort behavior
4. Responsive layout
5. Permission-based visibility

Output format: JSON array with fields id, title, steps, expected, priority, tags.

Constraints:
- Use standard_user and problem_user where relevant
- Sort dropdown options are: Name (A to Z), Name (Z to A), Price (low to high), Price (high to low)
- Sauce Demo has sort but no product filters; adapt filter/sort to sorting only
- Do not include markdown fences in the response
```

### Dashboard module notes

Initial output included filter-by-category tests, but Sauce Demo only supports sorting. I tightened the prompt to mention available sort options and removed filter assumptions. Responsive layout tests also needed viewport dimensions specified so Selenium could reproduce them consistently.

---

## Prompt 3 — REST API module

```
You are a senior SDET writing API regression tests using free public APIs:
- CRUD and schema: https://jsonplaceholder.typicode.com
- Auth bearer and status codes: https://httpbin.org

Generate exactly 5 test cases covering:
1. Auth token validation
2. CRUD operations
3. Error handling for 4xx responses
4. Error handling for 5xx or unavailable resources
5. JSON schema validation

Output format: JSON array with fields id, title, steps, expected, priority, tags.

Constraints:
- Use httpbin /bearer for token auth validation
- Use jsonplaceholder /posts for CRUD
- Use httpbin /status/{code} for 4xx/5xx and 429 rate-limit simulation
- Do not include markdown fences in the response
```

### API module notes

The first pass used reqres.in, which later started requiring an `x-api-key` header and caused 401 failures. I switched to JSONPlaceholder plus httpbin so the suite runs without signup. Rate limiting is simulated via httpbin `/status/429` instead of asserting real throttling behavior.
