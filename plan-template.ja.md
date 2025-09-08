# 実装計画: [FEATURE]

**ブランチ**: `[###-feature-name]` | **日付**: [DATE] | **仕様**: [link]  
**入力**: `/specs/[###-feature-name]/spec.md` からの機能仕様

## 実行フロー (/plan コマンドのスコープ)
```
1. 入力パスから機能仕様を読み込む
   → 見つからない場合: ERROR "No feature spec at {path}"
2. 技術的コンテキストを埋める（NEEDS CLARIFICATION をスキャン）
   → コンテキストからプロジェクトタイプを判定（web=frontend+backend, mobile=app+api）
   → プロジェクトタイプに基づき Structure Decision を設定
3. 下記の Constitution Check を評価
   → 違反がある場合: Complexity Tracking に記録
   → 正当化できない場合: ERROR "Simplify approach first"
   → Progress Tracking を更新: Initial Constitution Check
4. Phase 0 を実行 → research.md
   → NEEDS CLARIFICATION が残る場合: ERROR "Resolve unknowns"
5. Phase 1 を実行 → contracts, data-model.md, quickstart.md, エージェント固有テンプレートファイル（例: `CLAUDE.md`、`.github/copilot-instructions.md`、`GEMINI.md`）
6. Constitution Check を再評価
   → 新たな違反があれば: 設計をリファクタし、Phase 1 に戻る
   → Progress Tracking を更新: Post-Design Constitution Check
7. Phase 2 を計画 → タスク生成アプローチを記述（tasks.md は作成しない）
8. STOP - /tasks コマンドの準備完了
```

**重要**: /plan コマンドはステップ 7 で停止します。Phase 2–4 は他のコマンドが実行します:
- Phase 2: /tasks コマンドが tasks.md を作成
- Phase 3–4: 実装の実行（手動またはツール）

## サマリー
[Extract from feature spec: primary requirement + technical approach from research]

## 技術的コンテキスト
**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]  
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check
*ゲート: Phase 0 のリサーチ前に必須。Phase 1 の設計後にも再チェック。*

**Simplicity（単純さ）**:
- Projects: [#] (max 3 - e.g., api, cli, tests)
- フレームワークを直接使用しているか？（ラッパークラスなし）
- 単一のデータモデルか？（シリアライゼーション差異がない限り DTO は使わない）
- パターンを乱用していないか？（必要性が証明されるまで Repository/UoW を使わない）

**Architecture（アーキテクチャ）**:
- すべての機能をライブラリとして実装しているか？（アプリ直書き禁止）
- ライブラリ一覧: [name + purpose for each]
- ライブラリごとの CLI: [commands with --help/--version/--format]
- ライブラリの文書: llms.txt 形式を計画しているか？

**Testing（非交渉事項）**:
- RED-GREEN-Refactor サイクルを強制しているか？（テストは必ず先に失敗する）
- Git コミットは実装より先にテストが存在することを示しているか？
- 順序: Contract→Integration→E2E→Unit を厳守しているか？
- 実物の依存関係を使用しているか？（実DB、モック禁止）
- 次に対する統合テストがあるか: 新ライブラリ、契約変更、共有スキーマ？
- 禁止事項: 実装が先、RED フェーズのスキップ

**Observability（可観測性）**:
- 構造化ログは含まれているか？
- フロントエンドのログ → バックエンドへ集約できているか？（統一ストリーム）
- エラーコンテキストは十分か？

**Versioning（バージョニング）**:
- バージョン番号を割り当てたか？（MAJOR.MINOR.BUILD）
- BUILD を変更のたびに増やしているか？
- 破壊的変更をどう扱うか？（並行テスト、移行計画）

## プロジェクト構造

### ドキュメント（この機能）
```
specs/[###-feature]/
├── plan.md              # このファイル（/plan コマンドの出力）
├── research.md          # Phase 0 の出力（/plan コマンド）
├── data-model.md        # Phase 1 の出力（/plan コマンド）
├── quickstart.md        # Phase 1 の出力（/plan コマンド）
├── contracts/           # Phase 1 の出力（/plan コマンド）
└── tasks.md             # Phase 2 の出力（/tasks コマンド - /plan では作らない）
```

### ソースコード（リポジトリルート）
```
# オプション 1: 単一プロジェクト（DEFAULT）
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# オプション 2: Web アプリ（"frontend" + "backend" を検出した場合）
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# オプション 3: Mobile + API（"iOS/Android" を検出した場合）
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: アウトライン & リサーチ
1. 上記 Technical Context から **不明点** を抽出:
   - 各 NEEDS CLARIFICATION → research タスク
   - 各依存関係 → ベストプラクティス調査タスク
   - 各インテグレーション → パターン調査タスク

2. **リサーチエージェントを生成して実行**:
```
For each unknown in Technical Context:
  Task: "Research {unknown} for {feature context}"
For each technology choice:
  Task: "Find best practices for {tech} in {domain}"
```

3. **調査結果を統合**して `research.md` に次の形式で記録:
- Decision: [what was chosen]
- Rationale: [why chosen]
- Alternatives considered: [what else evaluated]

**出力**: research.md（すべての NEEDS CLARIFICATION を解消）

## Phase 1: 設計 & 契約
*前提: research.md 完了*

1. **機能仕様からエンティティを抽出** → `data-model.md`:
   - エンティティ名、フィールド、リレーション
   - 要件からのバリデーション規則
   - 状態遷移（該当時）

2. **機能要件から API 契約を生成**:
   - 各ユーザーアクション → エンドポイント
   - 標準 REST/GraphQL パターンを使用
   - 出力: OpenAPI/GraphQL スキーマを `/contracts/` へ

3. **契約から契約テストを生成**:
   - エンドポイント毎に1テストファイル
   - リクエスト/レスポンスのスキーマを検証
   - テストは必ず失敗させる（実装はまだ）

4. **ユーザーストーリーからテストシナリオを抽出**:
   - 各ストーリー → 統合テストシナリオ
   - Quickstart テスト = ストーリー検証手順

5. **エージェントファイルを漸進更新**（O(1) 操作）:
   - `/scripts/update-agent-context.sh [claude|gemini|copilot]` を実行
   - 既存があれば: 今回の計画で **新規** の技術だけを追加
   - マーカー間の手動追記は保持
   - 直近の変更を更新（最新3件）
   - トークン効率のため 150 行以内に抑える
   - 出力はリポジトリルートへ

**出力**: data-model.md、/contracts/*、失敗するテスト、quickstart.md、エージェント固有ファイル

## Phase 2: タスク計画アプローチ
*このセクションは /tasks コマンドが行う処理の説明です - /plan 中に実行しないこと*

**タスク生成戦略**:
- `/templates/tasks-template.md` をベースとして読み込む
- Phase 1 の設計ドキュメント（contracts, data model, quickstart）からタスク生成
- 各契約 → contract test タスク [P]
- 各エンティティ → model 作成タスク [P]
- 各ユーザーストーリー → integration test タスク
- テストを合格させるための実装タスク

**順序戦略**:
- TDD の順序: 実装前にテスト
- 依存順序: Models → Services → UI
- [P] は並列実行（独立ファイル）に付与

**見込み出力**: tasks.md に 25–30 個の番号付き・順序付きタスク

**重要**: このフェーズは /tasks コマンドが実行し、/plan は実行しない

## Phase 3+: 将来の実装
*/plan コマンドのスコープ外*

**Phase 3**: タスク実行（/tasks が tasks.md を生成）  
**Phase 4**: 実装（constitution 原則に従い tasks.md を実行）  
**Phase 5**: 検証（テスト実行、quickstart.md 実行、性能検証）

## Complexity Tracking
*Constitution Check の違反があり、正当化が必要な場合のみ記入*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Progress Tracking
*実行フロー中に更新されるチェックリスト*

**Phase ステータス**:
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate ステータス**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
