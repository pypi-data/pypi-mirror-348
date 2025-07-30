/**
 * Configuration for Playwright using default from @jupyterlab/galata
 */
const baseConfig = require('@jupyterlab/galata/lib/playwright-config');

module.exports = {
  ...baseConfig,
  webServer: {
    command:
      'jupyter lab --config ui-tests/jupyter_server_test_config.py --port 8888 --no-browser',
    url: 'http://localhost:8888/lab',
    timeout: 180 * 1000,
    reuseExistingServer: !process.env.CI,
    cwd: '..'
  },
  use: {
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  timeout: 180000
};
