# Adoption

Add a caller workflow to a repository:

```yaml
name: Collaboration
on:
  pull_request:
    types: [opened, edited, reopened, synchronize, ready_for_review, closed]
  issues:
    types: [closed, reopened]

permissions:
  contents: read
  issues: write
  pull-requests: read

jobs:
  entry:
    if: github.event_name == 'pull_request' && github.event.action != 'closed'
    uses: re8ch/Emprico/.github/workflows/pr-entry.yml@309da81d020078d728845a540a8c24718cb8c78d
  state:
    uses: re8ch/Emprico/.github/workflows/state.yml@309da81d020078d728845a540a8c24718cb8c78d
```

`pr-entry` accepts same-repository and `owner/repository#number` closing references. It verifies that each referenced Issue exists and reports whether native Project membership is visible to the caller token.

`state` applies only transitions established by current cases:

| Event | Issue status label |
| --- | --- |
| PR opened, reopened, synchronized or ready | `status:in-progress` |
| PR merged | `status:verifying` |
| Issue closed | `status:done` |
| Issue reopened | `status:in-progress` |

Cross-repository status writes require an installation token with access to the target repository. Without that authority the workflow records the reference and leaves the target unchanged.
