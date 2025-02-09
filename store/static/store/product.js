function setPriceBreakdown(event) {

  const quantity = parseInt(event.target.value);
  const priceBreaks = getPriceBreaks();
  const currencySymbol = '£';

  let breakdownString = 'Price Breakdown: ';

  let total = 0;

  let breakdowns = [];

  const priceMap = priceBreaks.map(([qty, price], i) => {

    if (i === priceBreaks.length - 1) {
      return 0;
    }

    const count = priceBreaks[i + 1][0] - qty;

    breakdowns.push(count + ' x ' + Number(price).toFixed(2));

    return count * price;
  });

  for (let i = 0; i < priceBreaks.length; i++) {
    const [qty, price] = priceBreaks[i];

    if (i === priceBreaks.length - 1 || priceBreaks[i + 1][0] > quantity) {
      const currentQty = quantity - qty;
      const amount = currentQty * price;
      total += amount;
      if (amount !== 0) {
        breakdownString += currentQty + ' x ' + currencySymbol + Number(price).toFixed(2);
      }
      break;
    } else {
      breakdownString += breakdowns[i] + ' + ';
      total += priceMap[i];
    }
  }

  breakdownString += ' = ' + currencySymbol + Number(total).toFixed(2);

  document.getElementById('price-breakdown').innerText = breakdownString;
  document.getElementById('total-price').innerText = currencySymbol + Number(total).toFixed(2);

}

function getPriceBreaks() {
  const table = document.getElementById('price-breaks-tbody');

  const priceBreaks = [];

  for (const row of table.children) {
    const quantityTd = row.firstElementChild;
    const priceTd = row.lastElementChild;
    const qty = parseInt(quantityTd.innerText);
    const price = parseFloat(priceTd.innerText.substring(1));
    priceBreaks.push([qty, price])
  }

  return priceBreaks;
}