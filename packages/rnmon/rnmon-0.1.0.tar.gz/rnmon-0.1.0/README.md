# RNMon - Reticulum Application Monitoring Daemon

RNMon is a simple monitoring daemon designed to monitor the status of multiple RNS applications and push the metrics over http using the influx line protocol.

## Installing

## Configuration

Configure the daemon via `scraping.yaml`, the example config has comments explaining the options.

The configuration for reticulum is auto-discovered, but you can specify the location of the configuration directory using the `--rns-config` argument.

## Operational principles

The metric pusher and all targets are executed in their own thread. The main thread starts a new RNS instance, and closes it on exit.

A link is established for each scrape target to reduce network overhead. If a link is broken for any reason, the thread is terminated and restarted - this avoids having to deal with the built-in RNS link retry mechanisms, their associated timeouts and any edge cases caused by using shared RNS intances. This might be changed in the future if RNS fixes the issues particular to this use case.
