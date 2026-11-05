import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.beforeEach(async ({ page }) => {
  // Local regression tests must not send analytics or contact real services.
  await page.route('**/*', (route) => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
});

for (const path of ['/', '/fr/', '/skills/', '/fr/skills/', '/publications/', '/fr/publications/', '/privacy/', '/fr/privacy/', '/404.html', '/fr/404.html']) {
  test(`${path} layout and accessibility`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(path);
    await expect(page.locator('h1')).toHaveCount(1);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(result.violations.map(({ id, nodes }) => ({ id, targets: nodes.map((node) => node.target) }))).toEqual([]);
    expect(errors).toEqual([]);
  });
}

for (const path of ['/', '/fr/']) {
  test(`${path} keyboard navigation and contact`, async ({ page }, testInfo) => {
    await page.goto(path);
    await expect(page.locator('[data-menu-button]')).toHaveAttribute('aria-label', /menu/i);
    // iOS WebKit does not tab to links unless full keyboard access is enabled.
    if (testInfo.project.name === 'mobile-webkit') await page.locator('.skip-link').focus();
    else await page.keyboard.press('Tab');
    await expect(page.locator('.skip-link')).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
    if (testInfo.project.name.startsWith('mobile')) {
      const toggle = page.locator('[data-menu-button]');
      await toggle.click();
      await expect(toggle).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('#site-menu')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    }
    const form = page.locator('form[data-contact-form]');
    await expect(form).toBeVisible();
    expect(await form.evaluate((element) => element.checkValidity())).toBe(false);
  });

  for (const status of [200, 500]) {
    test(`${path} contact response ${status} (mock service)`, async ({ page }) => {
      await page.route('https://formspree.io/f/mdaqgjny', (route) => route.fulfill({
        status, contentType: 'application/json', body: JSON.stringify(status === 200 ? { ok: true } : { error: 'Test failure' }),
        headers: { 'Access-Control-Allow-Origin': '*' },
      }));
      await page.goto(path);
      const form = page.locator('form[data-contact-form]');
      await form.locator('[name="name"]').fill('Quality test');
      await form.locator('[name="email"]').fill('test@example.com');
      await form.locator('[name="topic"]').selectOption({ index: 1 });
      await form.locator('[name="message"]').fill('This is a local automated test with a mocked service.');
      await form.locator('[name="privacy_acknowledged"]').check();
      await form.locator('button[type="submit"]').click();
      await expect(form.locator('[data-contact-status]')).toHaveAttribute('data-state', status === 200 ? 'success' : 'error');
      await expect(form.locator('button[type="submit"]')).toBeEnabled();
      if (status === 500) await expect(form.locator('[name="message"]')).not.toHaveValue('');
    });
  }
}
