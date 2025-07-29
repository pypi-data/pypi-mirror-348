# tap-freshservice

`tap-freshservice` is a Singer tap for Freshservice.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

Install from PyPi:

```bash
pipx install tap-freshservice
```

Install from GitHub:

```bash
pipx install git+https://github.com/Datateer/tap-freshservice.git@main
```


## Configuration

### Accepted Config Options

<!--
This section can be created by copy-pasting the CLI output from:

```
tap-freshservice --about --format=markdown
```
-->
## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| api_key             | True     | None    | The Freshservice API key |
| updated_since       | False    | 2000-01-01T00:00:00Z | The earliest record date to sync. You probably need this! The Freshservice API only returns items less than 30 days old. To override this, you must include an 'updated_since' value in the URL querystring. Providing a value here will ensure this value is used if there is no state (i.e. for a full refresh).  |
| base_url            | False    | https://<replace with your org>.freshservice.com/api/v2 | The url for the Freshservice API |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |


A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-freshservice --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-freshservice` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-freshservice --version
tap-freshservice --help
tap-freshservice --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-freshservice` CLI interface directly using `poetry run`:

```bash
poetry run tap-freshservice --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-freshservice
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-freshservice --version
# OR run a test `elt` pipeline:
meltano elt tap-freshservice target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
