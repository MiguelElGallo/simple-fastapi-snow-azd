# SIMPLE-FASTAPI-SNOW-AZD Application Tests

The included [Playwright](https://playwright.dev/) smoke test will hit the /docs api endpoint, and request customer with key 1
## Run Tests

The endpoint it hits will be discovered in this order:

1. Value of `FX_WEB_BASE_URL` environment variable
1. Value of `FX_WEB_BASE_URL` found in default .azure environment
1. Defaults to `http://localhost:7071`

To run the tests:

1. CD to /tests
1. Run `npm i && npx playwright install`
1. Run `npx playwright test`

You can use the `--headed` flag to open a browser when running the tests.

## Debug Tests

Add the `--debug` flag to run with debugging enabled. You can find out more info here: https://playwright.dev/docs/next/test-cli#reference

```bash
npx playwright test --debug
```

More debugging references: https://playwright.dev/docs/debug and https://playwright.dev/docs/trace-viewer
