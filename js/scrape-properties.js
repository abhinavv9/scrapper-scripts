const puppeteer = require("puppeteer");
const fs = require('fs');
const jsBeautify = require('js-beautify').js_beautify;

async function extractArray() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(
    "https://www.99acres.com/search/property/buy/delhi-ncr?city=1&preference=S&area_max=1000&area_min=900&area_unit=1&budget_min=0&res_com=C&isPreLeased=N"
  );

  const scriptTags = await page.evaluate(() => {
    const scripts = Array.from(document.querySelectorAll('script'));
    return scripts.map(script => script.innerHTML);
  });

  const str1 = scriptTags[4].replace("window.__initialData__=", "").replace("window.__masked__ = false", "");

  const unminifiedString = jsBeautify(str1, {
    indent_size: 2,
    space_in_empty_paren: true,
  });

  const formattedCode = `let res = ${unminifiedString};\n\nmodule.exports = res.srp.pageData;`;

  fs.writeFile('output.js', formattedCode, (err) => {
    if (err) throw err;
    console.log('The file has been saved!');
  });

  await browser.close();
  return true;
}

(async () => {
  await extractArray().then(() => {
    const res = require('./output');
    console.log(res);
    //delete output.js file
    fs.unlink('output.js', (err) => {
      if (err) throw err;
      console.log('output.js was deleted');
    });
  });

})();
