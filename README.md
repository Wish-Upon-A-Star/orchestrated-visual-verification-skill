# Orchestrated Visual Verification (OVV)

OVV는 Codex가 작업을 “구현 완료”에서 끝내지 않고, 요구사항 추출, 필요시 오케스트레이션, 시각 검증, 반복 리뷰, 증거 기반 완료 판단, 자기 개선 기록까지 수행하도록 만드는 Codex 스킬입니다.

짧은 이름: **OVV**

명시 호출:

```text
$orchestrated-visual-verification
```

자연어 호출:

```text
OVV 써서 이 작업을 계획, 구현, 시각 검증, 리뷰, 최종 보고까지 해줘.
```

## 이 스킬이 하는 일

OVV는 Codex가 완료를 주장하기 전에 다음 질문에 답하게 만듭니다.

1. 정확히 무엇이 요구되었는가?
2. 혼자 처리해도 되는가, 아니면 worker/validator를 나누는 오케스트레이션이 필요한가?
3. 각 요구사항은 어떤 증거로 검증되는가?
4. UI나 사용자에게 보이는 작업이라면 브라우저, 스크린샷, viewport, 렌더링 결과 같은 시각 증거가 있는가?
5. 실제 리뷰 라운드는 몇 번 수행되었고, 무엇을 발견했으며, 수정 후 무엇을 다시 확인했는가?

포함된 구성요소:

- `SKILL.md`: Codex 스킬 본문.
- `references/feasible-upgrades.md`: 실현 가능한 워크플로/검증 개선책 125개.
- `references/eval-fixtures.md`: 약한 보고서/강한 보고서 fixture.
- `scripts/audit_ovv_report.py`: 계획서나 최종 보고서의 증거 완성도를 점수화.
- `scripts/record_ovv_learning.py`: 실제 놓친 점을 JSONL learning log에 기록.
- `scripts/summarize_ovv_learnings.py`: 반복 실패를 집계하고 스킬 패치 후보를 제안.
- `agents/openai.yaml`: Codex 스킬 UI 메타데이터.

## 왜 필요한가

에이전트 작업은 자주 같은 방식으로 실패합니다.

- 요구사항이 흐릿하거나 빠짐.
- “완료”라고 말하지만 증거가 없음.
- UI 작업을 코드나 테스트만 보고 끝냄.
- 리뷰 라운드를 실제로 수행하지 않고 요약만 함.
- 반복되는 실수를 기록하지 않아 다음 작업에서도 같은 문제가 재발함.

OVV는 이런 약한 완료를 빨리 실패시키기 위한 스킬입니다. 테스트, Playwright, 수동 리뷰, 제품 판단을 대체하지 않습니다. 대신 “완료 주장에 필요한 증거가 빠져 있다”는 사실을 드러내는 강제 장치입니다.

## 설치법

### Windows PowerShell

레포를 clone한 뒤 Codex skills 디렉터리에 복사합니다.

```powershell
git clone https://github.com/Wish-Upon-A-Star/orchestrated-visual-verification-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force orchestrated-visual-verification-skill "$env:USERPROFILE\.codex\skills\orchestrated-visual-verification"
```

설치 후 Codex를 재시작하면 스킬 목록이 갱신됩니다.

### macOS / Linux

```bash
git clone https://github.com/Wish-Upon-A-Star/orchestrated-visual-verification-skill.git
mkdir -p "$HOME/.codex/skills"
cp -R orchestrated-visual-verification-skill "$HOME/.codex/skills/orchestrated-visual-verification"
```

설치 후 Codex를 재시작하면 스킬 목록이 갱신됩니다.

## 기본 사용법

스킬을 직접 호출:

```text
$orchestrated-visual-verification
이 기능을 구현하고 브라우저 스크린샷과 리뷰 라운드까지 포함해서 검증해줘.
```

짧은 이름으로 호출:

```text
OVV 써서 이 작업을 구현, 시각 검증, 리뷰 라운드까지 끝내줘.
```

최종 보고서만 audit:

```bash
python ~/.codex/skills/orchestrated-visual-verification/scripts/audit_ovv_report.py final-report.md
```

Windows:

```powershell
python "$env:USERPROFILE\.codex\skills\orchestrated-visual-verification\scripts\audit_ovv_report.py" final-report.md
```

## Audit 스크립트

`audit_ovv_report.py`는 계획서나 최종 보고서가 OVV가 요구하는 증거를 포함하는지 검사합니다.

점수화 항목:

- 요구사항,
- 증거,
- 오케스트레이션 판단,
- 시각/브라우저 증거,
- 리뷰 라운드,
- 이슈/수정/recheck 루프,
- 회귀 확인,
- 남은 제한사항,
- 사용법,
- 근거 없는 완료 주장 anti-pattern.

실행:

```bash
python scripts/audit_ovv_report.py final-report.md
```

JSON 출력:

```bash
python scripts/audit_ovv_report.py final-report.md --json
```

audit 실패를 learning log에 자동 기록:

```bash
python scripts/audit_ovv_report.py final-report.md --record-failures
```

learning log 경로 지정:

```bash
python scripts/audit_ovv_report.py final-report.md --record-failures --learning-log memory/ovv_skill_learnings.jsonl
```

중요: audit 통과가 실제 제품의 정확성을 증명하지는 않습니다. audit은 보고서가 필요한 증거 범주를 갖추었는지 확인합니다.

## 자기 개선 루프

OVV는 실제 놓친 점에서 개선되도록 설계되어 있습니다.

1. audit을 실행합니다.
2. audit이 실패하면 현재 산출물을 먼저 고칩니다.
3. `--record-failures`로 실패 범주를 자동 기록합니다.
4. 반복 실패를 요약합니다.
5. 반복되는 실패 범주를 스킬 규칙, audit check, fixture 개선 후보로 승격합니다.
6. 스킬을 고친 뒤 fixture를 다시 실행합니다.

learning log 요약:

```bash
python scripts/summarize_ovv_learnings.py --log memory/ovv_skill_learnings.jsonl --min-count 2
```

예시 출력:

```text
## Patch Candidates
- `visual_browser` (3): 사용자에게 보이는 작업에는 브라우저, 스크린샷, viewport, 렌더링 증거를 더 강하게 요구.
- `evidence` (2): 최종 signoff 전에 요구사항별 증거 매핑을 더 강하게 요구.
```

수동 learning 기록:

```bash
python scripts/record_ovv_learning.py \
  --task "settings panel" \
  --failure visual_browser \
  --lesson "UI signoff에는 스크린샷 증거가 필요함" \
  --resolution "desktop/mobile screenshot check를 추가함"
```

## 검증 Fixture

`references/eval-fixtures.md`에 검증 fixture가 들어 있습니다.

기대 동작:

- 약한 보고서: FAIL
- 강한 보고서: PASS
- UI 작업인데 시각 증거가 없는 보고서: FAIL
- 약한 실패가 반복됨: patch candidates 생성

빠른 로컬 smoke test:

```bash
mkdir -p tmp
printf "Done. I implemented the UI and reviewed it thoroughly. Tests passed.\n" > tmp/weak.md
python scripts/audit_ovv_report.py tmp/weak.md --record-failures --learning-log tmp/learnings.jsonl
python scripts/audit_ovv_report.py tmp/weak.md --record-failures --learning-log tmp/learnings.jsonl
python scripts/summarize_ovv_learnings.py --log tmp/learnings.jsonl --min-count 2
```

## 언제 OVV를 쓰면 좋은가

OVV가 적합한 작업:

- 브라우저나 스크린샷 검증이 필요한 UI/frontend 작업,
- 게임 UI나 시각 상태 작업,
- 회귀 위험이 있는 다중 파일 코딩 작업,
- 정확한 리뷰 라운드가 필요한 작업,
- agent prompt나 workflow 설계,
- 완료 주장이 증거 기반이어야 하는 작업,
- 오케스트레이션이 필요할 수 있지만 무조건 쓰면 안 되는 작업.

OVV 전체 루프가 과한 작업:

- 아주 작은 한 줄 수정,
- 단순 사실 답변,
- 구현이나 검증 주장이 없는 작업.

작은 작업에서는 lightweight path를 쓰면 됩니다. 요구사항을 짧게 추출하고, 최소 수정, 가장 좁은 의미 있는 검증, diff self-review, 증거 보고까지만 수행합니다.

## 레포 구조

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── strong-report.md
│   └── weak-report.md
├── references/
│   ├── eval-fixtures.md
│   └── feasible-upgrades.md
└── scripts/
    ├── audit_ovv_report.py
    ├── record_ovv_learning.py
    └── summarize_ovv_learnings.py
```

## 개발 및 검증

Python 스크립트 문법 확인:

```bash
python -m py_compile scripts/audit_ovv_report.py scripts/record_ovv_learning.py scripts/summarize_ovv_learnings.py
```

약한 보고서 audit:

```bash
printf "Done. I implemented the UI and reviewed it thoroughly. Tests passed.\n" > weak.md
python scripts/audit_ovv_report.py weak.md
```

약한 보고서는 실패해야 합니다.

강한 보고서 audit:

```bash
python scripts/audit_ovv_report.py examples/strong-report.md
```

강한 보고서는 통과해야 합니다.

## 라이선스

MIT
