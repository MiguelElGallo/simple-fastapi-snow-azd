import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('/docs', { waitUntil: 'networkidle' });
  await page.getByText('GET/api/customer/get-customerGet Customer').click();
  await page.getByRole('button', { name: 'Try it out' }).click();
  await page.getByPlaceholder('c_custkey').click();
  await page.getByPlaceholder('c_custkey').fill('1');
  await page.getByRole('button', { name: 'Execute' }).click();
  await page.locator('pre').filter({ hasText: '{ "c_name": "Customer#' }).click();
});