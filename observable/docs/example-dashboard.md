---
theme: dashboard
title: Example dashboard
toc: false
---

# Ecommerce analytics 🚀

<!-- Load and transform the data -->

```js
const ordersCountByStatus = FileAttachment("data/orders-count-by-status.csv").csv({typed: true});
```

```js
const ordersByDayData = FileAttachment("data/orders-count-by-status-and-day.csv").csv({typed: true});
```

```js
const ordersByDay = ordersByDayData.map((row) => {
  return {
    ...row,
    "Orders.createdAt.day": new Date(row["Orders.createdAt.day"])
  };
})
```

<!-- A shared color scale for consistency, sorted by the number of orders -->

```js
const color = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(ordersByDay, (D) => -D.length, (row) => row["Orders.status"]),
    unknown: "var(--theme-foreground-muted)"
  }
});
```

<!-- Cards with big numbers -->
```js
display(ordersCountByStatus);
```


```js
html`<div class="grid grid-cols-3">
  ${ordersCountByStatus.map((row) => {
    return html.fragment`
      <div class="card">
        <h2>${row["Orders.status"]}</h2>
        <span class="big">${row["Orders.count"]}</span>
      </div>
    `
  })}
</div>`
```

<!-- Plot of orders history -->

```js
function ordersBarChart(data, {width} = {}) {
  const minDate = new Date(2023, 0, 1);
  const maxDate = new Date(2023, 12, 1);

  const newData = data.filter((row) => row["Orders.createdAt.day"] >= minDate && row["Orders.createdAt.day"] <= maxDate);

  return Plot.plot({
    title: "Orders by Day (this year)",
    width,
    height: 300,
    y: {grid: true, label: "Count"},
    x: {type: "time", grid: true, label: "Date", tickFormat: "%b %d", tickCount: 5, domain: [minDate, maxDate], },
    color: {...color, legend: true},
    marks: [
      Plot.rectY(newData, {y: "Orders.count", x: "Orders.createdAt.day", fill: "Orders.status", interval: "day"}),
      Plot.ruleY([0])
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => ordersBarChart(ordersByDay, {width}))}
  </div>
</div>