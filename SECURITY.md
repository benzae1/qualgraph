# Security Policy

## Supported Versions

Qualgraph is currently alpha software. Security fixes target the `main` branch
until versioned releases are established.

## Reporting A Vulnerability

Please do not open a public issue for suspected vulnerabilities. Use GitHub's
private vulnerability reporting feature if it is enabled for the repository, or
contact the maintainers privately.

Include:

- affected version or commit
- operating system and Python version
- reproduction steps
- impact and any known workarounds

Qualgraph analyzes local source code and can optionally send focused code
context to an LLM provider. User code remains local unless an API-backed LLM
provider is explicitly selected.
