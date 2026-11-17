# Emprico dataset card

## Purpose

Emprico supports models that recommend project-management actions from observable project facts. A useful recommendation states an action, cites comparable cases, explains its judgment, exposes uncertainty and can be checked against later outcomes.

## Record layers

- `raw`: immutable source facts and collection provenance.
- `normalized`: stable repository, work-item, change and event records.
- `judgment`: human or agent interpretations with rationale and confidence.
- `outcome`: later checks, delivery evidence and observed consequences.
- `recommendation`: training or evaluation examples assembled from reviewed layers.

Derived labels never overwrite source facts. Records retain event time and observation time so later knowledge does not leak into earlier decisions.

## Initial slice

The first slice contains metadata from public GitOps pull requests and a small set of manually reviewed recommendation examples. PR bodies, comments, diffs and personal attributes are excluded initially. Repository licenses are recorded; `training_eligible` remains false until a dataset reviewer confirms the intended use.

## Intended use

- recommend Issue, Project, review, CI and delivery practices;
- retrieve comparable historical cases;
- evaluate whether a recommendation is supported and calibrated;
- study how project decisions relate to later outcomes.

## Excluded use

- ranking individual contributors;
- inferring personal productivity, intent or performance;
- reproducing credentials, private topology or raw telemetry;
- treating correlation as proof of a universal management rule;
- training on records without reviewed visibility, license and redaction metadata.

## Splits

Owned, collaboration and external repositories remain separate. Training and evaluation splits are grouped by project and time, not randomized by individual PR, to reduce history leakage.

## Publication

Schemas, collectors, aggregate manifests and reviewed public examples live in this public repository. Private source records require a private dataset with access control and an auditable export. Hugging Face publication is pending write-scoped organization credentials.
