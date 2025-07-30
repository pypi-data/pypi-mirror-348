# CacheGuard

A simple and secure Python datastore protected by [Sops](https://getsops.io/).

Comes in two varieties: simple key-value and simple text stores.

## Cache Types

* `KeyCache` - Simple key-value store
* `TextCache` - Simple text file store



## Sops Integrations

This project is powered by [Sopsy](https://github.com/nikaro/sopsy), which means all Sops tools will work with this project.

At-rest files can be examined if they are decrypted by sops, without needing an active Python session.  The type of file is "binary" from a sops perspective, this fully encrypts the body where keys are also not visible without decrytpion.

## Requires

This is an integration with Sops, and will *require* a functional Sops setup.

For assistance with Sops, see their [documentation](https://getsops.io/docs/).

## Threat Models

This modules protects data at rest.  It does not protect data at run time.  It may be possible for other modules/processes/logging/etc to view it.

Potenmtially useful for operational caches and other sensitive record keeping that needs to be local and transferred via git.

## Examples

<Coming Soon>
