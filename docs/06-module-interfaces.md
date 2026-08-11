# Module Interfaces

Status: Revised per researcher decisions of 2026-08-11 (doc 00)
Depends on: doc 01 (layout), doc 02–03 (types)

Interfaces are Python `Protocol`s in `app/domain/interfaces/`. All return rich
result objects carrying a stage state (doc 04 §3) — none raise for
domain-level failure. Types abbreviated; `Locator`, `DataPointDraft`, etc.
mirror doc 03 (drafts carry scientific_basis + acquisition_method + evidence
for rule-based confidence — extractors never self-assign confidence).

---

## 1. Document layer (A12: orchestrated, no single source of truth)

```python
class DocumentParsingOrchestrator(Protocol):
    def parse(self, doc: StoredDocument) -> OrchestratedParseResult:
        """Runs the configured parser stack: native text/layout (PyMuPDF
        baseline), scholarly-structure/reference enrichment (GROBID when
        available), table extraction, figure extraction, OCR fallback.
        Combines artifacts without privileging one parser as truth; result
        details what could and could not be extracted. Missing enrichment →
        PARTIAL_SUCCESS, never UNSUPPORTED_FORMAT (A12)."""

class DocumentParser(Protocol):          # one member of the stack
    def parse(self, doc: StoredDocument) -> ParseResult
    def capabilities(self) -> set[ParseCapability]

class FigureInterpreter(Protocol):       # §26 forest plots
    def interpret(self, region: FigureRegion, ctx: AnalysisContext) -> FigureResult:
        """§26 ladder (embedded text → layout → vision → OCR); rows carry
        row_kind (STUDY | SUBGROUP_TOTAL | ...), cells are DataPointDrafts
        with locator + acquisition_method."""
```

## 2. Extraction layer (AI-facing; proposes, never decides — §5)

```python
class ReferenceExtractor(Protocol):
    def extract(self, parse: OrchestratedParseResult) -> list[CitationMention]

class StudyIdentifier(Protocol):         # in-scope: labels *within* the review (A19)
    def find_study_labels(self, parse) -> list[StudyLabelMention]

class StatedRuleExtractor(Protocol):     # A20
    def extract_rules(self, parse: OrchestratedParseResult,
                      sources: list[StoredDocument]  # Methods/protocol/prereg/suppl
                      ) -> list[StatedRuleDraft]
        # verbatim rule_text + locator + structured_form where extractable

class StructuredDataExtractor(Protocol):
    def extract_effects(self, table: ParsedTable, ctx) -> list[PublishedEffectDraft]
    def extract_primary_values(self, parse, targets: ExtractionTargets
                               ) -> list[PrimaryValueCandidate]   # §31

class PrimaryStudyExtractor(Protocol):
    def identify_structure(self, parse) -> StudyStructureDraft
        # samples, arms, sample_arm_membership drafts (A13),
        # measures with higher_is_better evidence (A17), outcomes, timepoints

class LLMProvider(Protocol):             # §59, A16
    def complete(self, req: LLMRequest) -> LLMResponse
    def interpret_image(self, req: VisionRequest) -> LLMResponse

class ModelRouter(Protocol):             # A16
    def resolve(self, role: ModelRole, ctx: TaskContext) -> ConcreteModel
        """role ∈ {FAST_MODEL, DEFAULT_EXTRACTION_MODEL,
        COMPLEX_EXTRACTION_MODEL, ESCALATION_MODEL}. Assignment is
        configuration driven by gold-corpus benchmarks; supports escalation of
        low-confidence cases. Every call records the concrete model_id."""
```

## 3. Resolution layer (cited works only — A19)

```python
class BibliographicProvider(Protocol):   # CrossrefProvider, OpenAlexProvider, PubMedProvider
    def search_citation(self, c: CitationFields) -> list[MatchCandidate]
    def resolve_doi(self, doi: str) -> BibRecord | NoMatch | ApiFailure

class BibliographicResolver(Protocol):
    def resolve(self, pub: Publication) -> ResolutionResult
        """Resolves publications already cited by the review. Performs no
        discovery of external literature (A19)."""

class OpenAccessProvider(Protocol):      # §28 — never fabricates links
    def locate(self, pub: Publication) -> OAResult

class DocumentRetriever(Protocol):       # legal retrieval only (§66)
    def retrieve(self, oa: OALocation) -> RetrievalResult
```

## 4. Statistical layer (deterministic; separate package `statengine`)

```python
class StatisticalEngine(Protocol):
    def compute(self, formula_id: str, inputs: Mapping[str, Decimal | int]
                ) -> EngineResult:
        """values + formula_id/version + engine_version + warnings. Orientation
        transforms (A10) are explicit formula steps. Domain problems return
        warnings/INSUFFICIENT_DATA, never silent fixes."""
    def formulas(self) -> list[FormulaSpec]

# Families: md, cohen_d, hedges_g (+variances/SEs/CIs), change scores;
# or/rr/rd (+log forms, zero-cell policies); r/fisher_z; hr/log_hr/ci_to_se;
# generic inverse-variance; composites for non-1:1 correspondences (O5);
# pooling: fixed_iv, random effects (DL first, alternatives for O1
# method-variant testing), q, i2, tau2, prediction_interval.
```

## 5. Audit layer

```python
class CorrespondenceBuilder(Protocol):   # A23
    def build(self, analysis: AnalysisId) -> list[EffectCorrespondence]
        # one-to-one / one-to-many / many-to-one; composites computed via engine

class AuditEngine(Protocol):             # A8 three-question model
    def compare(self, corr: EffectCorrespondence,
                tol: ToleranceRules, sev: SeverityRules) -> AuditComparison
        # Q1 rounding_match; Q2 numerical_match (computational tolerance only,
        # AMBIGUOUS_METHOD when methods UNRESOLVED, O1); Q3 severity separately
    def compare_pool(self, analysis: AnalysisId, tol, sev) -> AuditComparison
    def diagnose(self, comparison: AuditComparison) -> FindingDiagnosis  # §38

class RuleConsistencyChecker(Protocol):  # A20 / O2
    def check(self, rule: StatedRule, observed: ObservedSelection
              ) -> RuleCheckResult
        # emits POSSIBLE-level evidence only; requires quoted textual spans

class ValidationEngine(Protocol):        # §33, §54
    def check_record(self, effect: PublishedEffect) -> list[ValidationIssue]
    def check_project(self, project: ProjectId) -> list[ValidationIssue]
```

## 6. Export & infrastructure

```python
class ExportEngine(Protocol):            # §49–52; workbook = audit_workbook.xlsx (A14)
    def export_xlsx(self, project) -> Path
    def export_csv(self, project) -> Path
    def export_json(self, project) -> Path
    def export_archive(self, project) -> Path   # §52 + A21 scope note in README

class JobQueue(Protocol):                # A11: durable, at-least-once,
    def enqueue(self, stage_id, work_item, idempotency_key, parent=None) -> JobId
    def claim(self, worker_id, lease_ttl) -> Job | None      # lease-based
    def heartbeat(self, job) -> None
    def complete(self, job, result: StageResult) -> None
        # SQLite-compatible impl first; PG/Redis behind same interface

class CacheStore(Protocol):              # §62
    def get(self, ns, key_hash) -> CacheHit | None
    def put(self, ns, key_hash, payload) -> None
    def invalidate(self, ns, key_hash=None) -> None
```

## 7. Testing seams

Every adapter has (a) an in-memory **fake** and (b) a **replay** implementation
over recorded fixtures, so the full pipeline runs offline in CI. Real adapters
run in a small, explicitly marked live suite. The `ModelRouter` has a fixture
mode pinning concrete models for reproducible benchmark runs (A16).
