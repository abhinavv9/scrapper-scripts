const puppeteer = require('puppeteer');

(async () => {
  const latitude = '28.5600472'; // Latitude of the specific area
  const longitude = '7.4352572'; // Longitude of the specific area
  const query = 'hospital near me';

  // Construct the URL with latitude, longitude, and search query
  const url = `https://www.google.com/maps/@${latitude},${longitude},15z`;

  const browser = await puppeteer.launch({ headless: false }); // Run Chrome in headless mode
  const page = await browser.newPage();
  await page.goto(url);

  // Perform your scraping operations here
  await page.waitForSelector('#searchboxinput');
  await page.type('#searchboxinput', query);
  await page.keyboard.press('Enter');

  await page.waitForSelector('.qBF1Pd');

  const scrollPauseTime = 2000;
  let lastResults = null;

  while (true) {
    const results = await page.$$('.qBF1Pd');
    if (results.length === lastResults?.length) {
      break;
    }

    lastResults = results;
    const lastElement = results[results.length - 1];
    await page.evaluate((element) => {
      element.scrollIntoView();
    }, lastElement);
    await page.waitForTimeout(scrollPauseTime);
  }

  const results = await page.$$('.qBF1Pd');
  for (const result of results) {
    try {
      const text = await page.evaluate((element) => element.textContent, result);
      console.log(text);
    } catch (error) {
      console.log(`Error occurred: ${error}`);
    }
  }

  await browser.close();
})();
