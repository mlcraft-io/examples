import { csvFormat } from "d3-dsv";
import config from "../config.js";

const fetchData = async () => {
  const req = await fetch(config.API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: config.ACCESS_TOKEN,
      "x-hasura-datasource-id": config.DATASOURCE_ID,
      "x-hasura-branch-id": config.BRANCH_ID,
    },
    body: JSON.stringify({
      query: {
        limit: 1000,
        order: {},
        offset: 0,
        filters: [],
        measures: ["Orders.count"],
        segments: [],
        timezone: "UTC",
        dimensions: ["Orders.status"],
        timeDimensions: [],
      },
    }),
  }).then((response) => response.json());

  return req;
};

let req;

for (let i = 0; i < 100; i++) {
  req = await fetchData();

  if (req?.error) {
    console.error(req.error);
    break;
  }

  // reqiest again if the data is still loading.
  if (req?.progress?.loading) {
    console.log("Still loading...");
  } else {
    break;
  }
}

// Write out csv formatted data.
process.stdout.write(csvFormat(req.data));
