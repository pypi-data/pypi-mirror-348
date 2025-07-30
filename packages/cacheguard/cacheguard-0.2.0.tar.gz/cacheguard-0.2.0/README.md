# CacheGuard

A simple and secure Python key-value store protected by [Sops](https://getsops.io/).

## Requires

This is an integration with Sops, and will *require* a functional Sops setup.

For assistance with Sops, see their [documentation](https://getsops.io/docs/).

## Threat Models

This modules protects data at rest.  It does not protect data at run time.  It may be possible for other modules/processes/logging/etc to view it.

Potenmtially useful for operational caches and other sensitive record keeping that needs to be local and transferred via git.

## Examples

<Coming Soon>
