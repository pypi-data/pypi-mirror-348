import { expect, test } from '@jupyterlab/galata';

test('ActivateCellButton should appear and function correctly', async ({
  page
}) => {
  console.debug('Starting test...');

  // Create a new notebook
  console.debug('Creating new notebook...');
  await page.menu.clickMenuItem('File>New Notebook');

  // Wait for the notebook to be ready
  console.debug('Waiting for notebook to be ready...');
  await page.waitForSelector('.jp-Notebook', { timeout: 30000 });

  // Add a markdown cell
  console.debug('Adding markdown cell...');
  await page.keyboard.press('b');
  await page.keyboard.type('# Markdown Cell');

  // Add a code cell
  console.debug('Adding code cell...');
  await page.keyboard.press('b');
  await page.keyboard.type('print("hello")');

  // Focus on the markdown cell
  console.debug('Focusing on markdown cell...');
  await page.click('.jp-MarkdownCell');

  // Wait for and verify the button appears with correct text
  console.debug('Waiting for markdown button...');
  const markdownButton = await page.waitForSelector(
    '.jv-cell-ai-button-container',
    { timeout: 10000 }
  );
  console.debug('Markdown button found, checking text...');
  const markdownText = await markdownButton.textContent();
  console.debug('Markdown button text:', markdownText);
  expect(markdownText).toContain('Generate code');

  // Focus on the code cell
  console.debug('Focusing on code cell...');
  await page.click('.jp-CodeCell');

  // Wait for and verify the button appears with correct text
  console.debug('Waiting for code button...');
  const codeButton = await page.waitForSelector(
    '.jv-cell-ai-button-container',
    { timeout: 10000 }
  );
  console.debug('Code button found, checking text...');
  const codeText = await codeButton.textContent();
  console.debug('Code button text:', codeText);
  expect(codeText).toContain('Change code');

  // Verify only one button exists at a time
  console.debug('Verifying button count...');
  const buttons = await page.$$('.jv-cell-ai-button-container');
  console.debug('Button count:', buttons.length);
  expect(buttons.length).toBe(1);
});
