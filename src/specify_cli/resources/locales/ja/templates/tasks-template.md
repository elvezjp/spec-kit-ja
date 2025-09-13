# タスク: [FEATURE NAME]

**入力**: `/specs/[###-feature-name]/` の設計ドキュメント  
**前提条件**: plan.md (required), research.md, data-model.md, contracts/

## 実行フロー（メイン）
```
1. feature ディレクトリから plan.md を読み込む
   → 見つからない場合: ERROR "No implementation plan found"
   → 抽出: tech stack, libraries, structure
2. 追加の設計ドキュメントを読み込む（任意）:
   → data-model.md: エンティティを抽出 → model tasks
   → contracts/: 各ファイル → contract test task
   → research.md: 決定事項を抽出 → setup tasks
3. カテゴリごとにタスクを生成:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. タスクルールを適用:
   → 異なるファイル = [P]（並列実行可）
   → 同一ファイル = 逐次（[P] なし）
   → 実装前にテスト（TDD）
5. タスクに連番を付与（T001, T002...）
6. 依存関係グラフを生成
7. 並列実行サンプルを作成
8. タスク完全性を検証:
   → すべての契約にテストがあるか？
   → すべてのエンティティにモデルがあるか？
   → すべてのエンドポイントが実装されているか？
9. 返却: SUCCESS（タスク実行準備完了）
```

## フォーマット: `[ID] [P?] 説明`
- **[P]**: 依存がなくファイルが異なれば並列実行可
- 説明には正確なファイルパスを含めること

## パス規約
- **単一プロジェクト**: `src/`, `tests/` はリポジトリルート
- **Web アプリ**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` または `android/src/`
- 以下は単一プロジェクト前提。plan.md の構造に合わせて調整すること

## Phase 3.1: Setup
- [ ] T001 実装計画に従ってプロジェクト構造を作成
- [ ] T002 [language] プロジェクトを [framework] 依存関係で初期化
- [ ] T003 [P] リンティングとフォーマッタを設定

## Phase 3.2: Tests First (TDD) ⚠️ 3.3 より前に必須
**CRITICAL: これらのテストは実装前に必ず作成し、かつ失敗していなければならない**
- [ ] T004 [P] Contract test POST /api/users in tests/contract/test_users_post.py
- [ ] T005 [P] Contract test GET /api/users/{id} in tests/contract/test_users_get.py
- [ ] T006 [P] Integration test user registration in tests/integration/test_registration.py
- [ ] T007 [P] Integration test auth flow in tests/integration/test_auth.py

## Phase 3.3: Core Implementation（テストが失敗している状態を確認後）
- [ ] T008 [P] User model in src/models/user.py
- [ ] T009 [P] UserService CRUD in src/services/user_service.py
- [ ] T010 [P] CLI --create-user in src/cli/user_commands.py
- [ ] T011 POST /api/users endpoint
- [ ] T012 GET /api/users/{id} endpoint
- [ ] T013 入力バリデーション
- [ ] T014 エラーハンドリングとロギング

## Phase 3.4: Integration
- [ ] T015 Connect UserService to DB
- [ ] T016 Auth middleware
- [ ] T017 Request/response logging
- [ ] T018 CORS and security headers

## Phase 3.5: Polish
- [ ] T019 [P] Unit tests for validation in tests/unit/test_validation.py
- [ ] T020 Performance tests (<200ms)
- [ ] T021 [P] Update docs/api.md
- [ ] T022 Remove duplication
- [ ] T023 Run manual-testing.md

## 依存関係
- Tests (T004-T007) は実装 (T008-T014) より前
- T008 は T009, T015 をブロック
- T016 は T018 をブロック
- 実装は Polish (T019-T023) より前

## 並列実行例
```
# T004-T007 を同時に起動:
Task: "Contract test POST /api/users in tests/contract/test_users_post.py"
Task: "Contract test GET /api/users/{id} in tests/contract/test_users_get.py"
Task: "Integration test registration in tests/integration/test_registration.py"
Task: "Integration test auth in tests/integration/test_auth.py"
```

## 注意事項
- [P] タスク = 異なるファイル、依存なし
- 実装前にテストが失敗していることを確認
- 各タスク終了ごとにコミット
- 曖昧なタスクや同一ファイルを同時に触る [P] は避ける

## タスク生成ルール（main() 実行時に適用）
1. **Contracts 由来**:
   - 各契約ファイル → contract test タスク [P]
   - 各エンドポイント → 実装タスク
2. **Data Model 由来**:
   - 各エンティティ → model 作成タスク [P]
   - リレーション → service 層タスク
3. **User Stories 由来**:
   - 各ストーリー → integration test [P]
   - Quickstart シナリオ → 検証タスク
4. **順序**:
   - Setup → Tests → Models → Services → Endpoints → Polish

## 検証チェックリスト
*GATE: main() が返却前にチェック*
- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task

