# Publishable output checklist

Only deliberately reviewed release artifacts belong in this directory.
Generated runs remain ignored by default, including files placed here, so a
release artifact must be staged intentionally with `git add -f`.

Before publishing, verify all of the following:

- [ ] no API key, credential, local absolute path, or personal identifier;
- [ ] no private gold proof, private source bundle, or privileged checker detail;
- [ ] redistribution rights for every paper excerpt and third-party artifact;
- [ ] exact target statement and provenance are preserved;
- [ ] candidate, partial, cascade-only, and private-checker outcomes are labeled correctly;
- [ ] terminal status and reached gates agree with the public description;
- [ ] raw model traces are included only when their publication is intentional;
- [ ] links, manifests, and checksums resolve from a fresh clone.

Intentional staging example:

```bash
git add -f Outputs/publishable/<reviewed-artifact>
```

This checklist reduces accidental disclosure; it does not determine copyright
or establish mathematical correctness.
