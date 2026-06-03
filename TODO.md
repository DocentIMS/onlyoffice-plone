# TODO

Deferred items and ideas for future work.

## ONLYOFFICE editing / co-editing

- **Consider keeping full versions of documents when force saving.** Force
  saves (status 6) currently overwrite the stored file in place to avoid
  unbounded growth of the Plone version history (a force save happens on every
  manual Save). Revisit whether selected force saves should create a retained
  Plone (CMFEditions) version instead.

- **Consider whether to lock the co-editing mode and hide its icon.** The
  Fast/Strict co-editing mode is currently left to the editor default and the
  user's toggle in the Collaboration ribbon. Evaluate seeding a default mode
  from the host config and optionally locking it (hiding the switch) for
  governance.
