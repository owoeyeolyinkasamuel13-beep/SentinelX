# SentinelX Development Rules

## Project

SentinelX is a modular cybersecurity toolkit built for educational,
professional portfolio, and authorized security-testing purposes.

## Development Principles

- Security first.
- Keep modules modular.
- Keep functions focused on one responsibility.
- Prefer readable Python over clever Python.
- Do not introduce unnecessary dependencies.
- Do not break existing functionality.
- Test changes before considering a task complete.
- Keep CLI output consistent across modules.

## Module Structure

Each module should:

- Inherit from `Module`.
- Define `name`.
- Define `category`.
- Define `description`.
- Implement `run()`.

## CLI

Use the utilities in:

`utils/display.py`

Do not create separate formatting systems for individual modules.

## Git

Before making significant changes:

1. Inspect the existing implementation.
2. Make the smallest necessary change.
3. Test it.
4. Report what changed.
5. Do not modify unrelated files.

## Security

SentinelX must only be used against systems the user is authorized
to test.

Do not add malware, persistence, credential theft, stealth,
unauthorized access, destructive behavior, or hidden telemetry.