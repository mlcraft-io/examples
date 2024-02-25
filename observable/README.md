# Integrating Synmetrix with Observable: A Quick Guide

This is a guide to integrating [Synmetrix](https://synmetrix.org) with [Observable](https://observablehq.com/), a leading platform for creating and sharing data visualizations. With Synmetrix's REST API, you can easily connect to Observable and create interactive dashboards and reports. Embedable visualizations can be shared across your organization, enabling data-driven decision-making.

## Getting Started

Before proceeding, ensure you have completed Synmetrix's [Quick Start guide](https://docs.synmetrix.org/docs/quickstart#prerequisite-software).

## Setting Up Synmetrix with Observable

### Copy the Synmetrix API Key

1. **Access Synmetrix**: Go to the [Synmetrix Stack](https://localhost/) website and sign into your account. For demonstration, utilize the provided default seed data.
2. **Retrieve the API Key**: Move to the [Explore -> REST API](https://docs.synmetrix.org/docs/user-guide/explore#example-api-utilization) section and copy the API key provided there.
3. Insert the copied API key as `ACCESS_TOKEN` into the `config.js` file found within the `docs` directory.

### Starting Observable

Go to the root of the example project and run the following command to install the dependencies:

```bash
yarn install
```

Then, start the local preview server:

```bash
yarn dev
```

Then visit <http://localhost:3000> to preview your project.

For more, see <https://observablehq.com/framework/getting-started>.

## Project structure

A typical Framework project looks like this:

```ini
.
├─ docs
│  ├─ components
│  │  └─ timeline.js           # an importable module
│  ├─ data
│  │  ├─ launches.csv.js       # a data loader
│  │  └─ events.json           # a static data file
│  ├─ example-dashboard.md     # a page
│  ├─ example-report.md        # another page
│  └─ index.md                 # the home page
├─ .gitignore
├─ observablehq.config.ts      # the project config file
├─ package.json
└─ README.md
```

**`docs`** - This is the “source root” — where your source files live. Pages go here. Each page is a Markdown file. Observable Framework uses [file-based routing](https://observablehq.com/framework/routing), which means that the name of the file controls where the page is served. You can create as many pages as you like. Use folders to organize your pages.

**`docs/index.md`** - This is the home page for your site. You can have as many additional pages as you’d like, but you should always have a home page, too.

**`docs/data`** - You can put [data loaders](https://observablehq.com/framework/loaders) or static data files anywhere in your source root, but we recommend putting them here.

**`docs/components`** - You can put shared [JavaScript modules](https://observablehq.com/framework/javascript/imports) anywhere in your source root, but we recommend putting them here. This helps you pull code out of Markdown files and into JavaScript modules, making it easier to reuse code across pages, write tests and run linters, and even share code with vanilla web applications.

**`observablehq.config.ts`** - This is the [project configuration](https://observablehq.com/framework/config) file, such as the pages and sections in the sidebar navigation, and the project’s title.

## Command reference

| Command           | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `yarn install`            | Install or reinstall dependencies                        |
| `yarn dev`        | Start local preview server                               |
| `yarn build`      | Build your static site, generating `./dist`              |
| `yarn deploy`     | Deploy your project to Observable                        |
| `yarn clean`      | Clear the local data loader cache                        |
| `yarn observable` | Run commands like `observable help`                      |


## About the data loaders

The Observable Framework leverages [data loaders](https://observablehq.com/framework/loaders) to incorporate data into projects. These loaders are essentially modules that return a promise, which upon resolution, provides the required data. This mechanism allows for a variety of data integration methods, including file-based loading, API fetching, or dynamic data generation.

Within the `data` folder of your project, you'll find specific data loaders designed for fetching data from the Synmetrix API. Presently, we have two main loaders available:

- `orders-count-by-status.csv.js`: This loader retrieves data on `orders`, categorized by `status`, directly from the Synmetrix API. It is primarily used to generate single-value cards within the framework.
- `orders-count-by-status-and-day.csv.js`: Similarly, this loader fetches `orders` data, but with an additional layer of grouping by both `status` and `day`. The data fetched by this loader is ideal for constructing bar charts that depict the distribution of orders based on status and day.


## Video Tutorial

[![](https://img.youtube.com/vi/VcAP4vrL8cY/0.jpg)](https://youtu.be/VcAP4vrL8cY)
