

=========
Changelog
=========




.. towncrier release notes start

4.1.0 (2025-05-18)
==================

Other Changes
-------------

- Use ``__slots__`` to reduce memory usage of ``Version``.



4.0.4 (2024-04-20)
==================

Bug Fixes
---------

- Use ``filter='data'`` for ``extractall`` call on supported Python versions as additional guard to the existing out of path checks against malicious tar files.

- Remove custom ``LegacyVersion`` and use ``packaging-legacy`` instead, which is also used by pypi.org.



4.0.3 (2023-11-23)
==================

Bug Fixes
---------

- Add ``is_prerelease`` and other methods to ``LegacyVersion`` to fix ``get_sorted_versions`` with ``stable=True`` and some other cases.


4.0.2 (2023-10-15)
==================

Bug Fixes
---------

- Do not mark commands with returncode ``None`` from tox 4.x as failed.


4.0.1 (2023-10-15)
==================

Bug Fixes
---------

- Restore flushing after each written line in new TerminalWriter.

