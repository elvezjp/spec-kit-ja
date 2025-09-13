# ご注意ください。
このリポジトリは、Github Spec kitのテンプレートなどについて、試験的に日本語化するためのものです。2025年9月9日にクローンし、一部日本語化しています。

<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🌱 Spec Kit</h1>
    <h3><em>高品質なソフトウェアをより速く構築しよう。</em></h3>
</div>

<p align="center">
    <strong>Spec-Driven Development（仕様駆動開発）の助けを借りて、組織が差別化されないコードを書くことではなくプロダクトシナリオに集中できるようにする取り組みです。</strong>
</p>

[![Release](https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/github/spec-kit/actions/workflows/release.yml)

---

## 目次

- [🤔 Spec-Driven Developmentとは？](#-spec-driven-developmentとは)
- [⚡ はじめ方](#-はじめ方)
- [📚 コア哲学](#-コア哲学)
- [🌟 開発フェーズ](#-開発フェーズ)
- [🎯 実験目的](#-実験目的)
- [🔧 前提条件](#-前提条件)
- [📖 詳細情報](#-詳細情報)
- [📋 詳細なプロセス](#-詳細なプロセス)
- [🔍 トラブルシューティング](#-トラブルシューティング)
- [👥 メンテナー](#-メンテナー)
- [💬 サポート](#-サポート)
- [🙏 謝辞](#-謝辞)
- [📄 ライセンス](#-ライセンス)

## 🤔 Spec-Driven Developmentとは？

Spec-Driven Development（仕様駆動開発）は、従来のソフトウェア開発の「常識」を覆すものです。何十年もの間、コードこそが主役であり、仕様書は「足場」として使われ、いざ「本番作業」が始まると捨て去られてきました。Spec-Driven Developmentでは仕様が主役となり、開発の根幹をなします。

## ⚡ はじめ方

### 1. Specifyをインストール

使用するコーディングエージェントに応じてプロジェクトを初期化します。

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

### 2. 仕様（Spec）を作成

`/specify`コマンドを使って、作りたいものを記述します。**「何を」「なぜ」作るか**に集中し、技術スタックにはこだわりません。

```bash
/specify 写真を個別のアルバムに整理できるアプリケーションを作成したい。アルバムは日付ごとにグループ化され、メインページでドラッグ＆ドロップで再編成できる。アルバムは決して上書きされないようにしたい。
```

### 3. 技術的な実装計画を作成

`/plan`コマンドで技術スタックやアーキテクチャの選定を指示します。

```bash
/plan このアプリはViteを使用し、ライブラリは最小限に。できるだけバニラのHTML, CSS, JavaScriptを使う。画像はどこにもアップロードせず、メタデータはローカルのSQLiteデータベースに保存する。
```

### 4. ブレークダウンし実装

`/tasks`で実行可能なタスクリストを作成し、エージェントに実装させます。

詳しい手順は[総合ガイド](./spec-driven.md)をご覧ください。

## 📚 コア哲学

Spec-Driven Developmentは以下を重視します：

- **意図駆動開発**：「何を」作るかの仕様が「どう作るか」に先行
- **充実した仕様作成**：ガードレールや組織的原則を活用
- **多段階の洗練**：一発生成ではなく、段階的に仕様を磨き上げる
- **高度なAIモデルの活用**：仕様の解釈にAIを積極的に利用

## 🌟 開発フェーズ

| フェーズ | フォーカス | 主な活動 |
|---------|---------|-----------|
| **0→1開発**（グリーンフィールド） | ゼロからの生成 | <ul><li>高レベル要件から開始</li><li>仕様生成</li><li>実装手順の計画</li><li>プロダクション品質のビルド</li></ul> |
| **創造的探求** | 並列実装 | <ul><li>多様な解決策の模索</li><li>複数の技術スタックやアーキテクチャのサポート</li><li>UXパターンの実験</li></ul> |
| **反復的強化**（ブラウンフィールド） | レガシー近代化 | <ul><li>段階的な機能追加</li><li>レガシーシステムのモダナイズ</li><li>プロセス適応</li></ul> |

## 🎯 実験目的

本リサーチの焦点：

### 技術独立性

- 多様な技術スタックでアプリケーションを作成
- Spec-Driven Developmentが特定技術や言語・フレームワークに依存しないことを検証

### エンタープライズ制約

- ミッションクリティカルなアプリ開発の実証
- 組織的制約（クラウド、技術スタック、エンジニアリング手法等）の組み込み
- エンタープライズ向けデザインシステムやコンプライアンス要件のサポート

### ユーザー中心開発

- 異なるユーザー層と好みに対応したアプリ開発
- 様々な開発アプローチ（「ノリでコーディング」からAIネイティブまで）への対応

### 創造的・反復的プロセス

- 並列実装探求の概念検証
- 強固な反復的機能開発ワークフローの提供
- アップグレードや近代化タスクへの拡張

## 🔧 前提条件

- **Linux/macOS**（WindowsではWSL2も可）
- AIコーディングエージェント：[Claude Code](https://www.anthropic.com/claude-code)、[GitHub Copilot](https://code.visualstudio.com/)、[Gemini CLI](https://github.com/google-gemini/gemini-cli)
- パッケージ管理：[uv](https://docs.astral.sh/uv/)
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 📖 詳細情報

- **[Spec-Driven Development完全ガイド](./spec-driven.md)** - プロセスの詳細解説
- **[詳細な手順](#詳細なプロセス)** - ステップバイステップの実装ガイド

---

## 📋 詳細なプロセス

<details>
<summary>詳細なステップバイステップ手順を展開</summary>

Specify CLIを使ってプロジェクトをブートストラップできます。必要なアーティファクトが環境に導入されます。コマンド例：

```bash
specify init <project_name>
```

カレントディレクトリで初期化する場合：

```bash
specify init --here
```

CLIの表示やテンプレートを日本語にするには、`--lang ja` オプションを付けます。

```bash
specify --lang ja init <project_name>
```

![Specify CLIが新プロジェクトをターミナルでブートストラップ](./media/specify_cli.gif)

AIエージェントを選択するように促されます。ターミナルで直接指定も可能です：

```bash
specify init <project_name> --ai claude
specify init <project_name> --ai gemini
specify init <project_name> --ai copilot
# カレントディレクトリの場合:
specify init --here --ai claude
```

CLIはClaude CodeやGemini CLIのインストール有無を確認します。未インストール、もしくはテンプレートのみ取得したい場合は`--ignore-agent-tools`を付加してください。

```bash
specify init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** プロジェクトのブートストラップ

プロジェクトフォルダに移動し、AIエージェント（例：claude）を起動します。

![Claude Code環境のブートストラップ](./media/bootstrap-claude-code.gif)

/specify, /plan, /tasksコマンドが利用可能なら設定完了です。

まずは新規プロジェクトのスキャフォールディングを作成しましょう。/specifyコマンドで要件を明確に記述します。

> [!IMPORTANT]
> _何を_作りたいか、_なぜ_作るのかをできるだけ明確に書きましょう。**この時点では技術スタックにこだわらないでください。**

プロンプト例：

```text
Taskifyというチーム生産性プラットフォームを開発したい。ユーザーはプロジェクトを作成し、チームメンバーを追加し、タスクを割り当て、コメントを残し、タスクをカンバン形式で移動できるようにしたい。初期フェーズ「Create Taskify」ではユーザーは事前定義されて5人（プロダクトマネージャー1名、エンジニア4名）。3つのサンプルプロジェクトを用意。カンバンのカラムは「To Do」「In Progress」「In Review」「Done」。ログイン機能は不要。ユーザー選択後、プロジェクトリスト画面へ。プロジェクトクリックでカンバン表示。カードはドラッグ＆ドロップで移動可。自分担当カードは色分け。自身のコメントは編集・削除可、他人のコメントは不可。
```

この後、Claude Codeが仕様作成と計画プロセスを開始します。新しいブランチ（例：`001-create-taskify`）、および`specs/001-create-taskify`ディレクトリに仕様が作成されます。

生成される仕様にはユーザーストーリーや機能要件が含まれています。

この段階でプロジェクトフォルダは以下のようになります：

```text
├── memory
│	 ├── constitution.md
│	 └── constitution_update_checklist.md
├── scripts
│	 ├── check-task-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── get-feature-paths.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	 └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

### **STEP 2:** 仕様明確化

ベース仕様ができたら、不明点を追加で明確にします。例：

```text
各サンプルプロジェクトにはタスク数が5〜15個で、いろいろな完了状態にランダムに分布するようにしてほしい。各状態に最低1つタスクがあること。
```

また、**レビューチェックリスト**をAIに読ませて、達成項目をチェックさせましょう。

```text
レビューチェックリストを読んで、仕様が満たしている項目にチェックを入れてください。満たしていない場合は空欄で。
```

Claude Codeの提案を「最終版」とせず、質問や明確化をしながら仕様を洗練しましょう。

### **STEP 3:** 計画の作成

技術スタックや要件を具体化します。/planコマンド例：

```text
.NET Aspire、データベースはPostgres、フロントエンドはBlazorサーバーでカンバンのドラッグ＆ドロップとリアルタイム更新。APIはprojects、tasks、notificationsを用意。
```

この出力で、実装詳細ドキュメントが生成されます。ディレクトリ例：

```text
.
├── CLAUDE.md
├── memory
│	 ├── constitution.md
│	 └── constitution_update_checklist.md
├── scripts
│	 ├── check-task-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── get-feature-paths.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	 ├── contracts
│	 │	 ├── api-spec.json
│	 │	 └── signalr-spec.md
│	 ├── data-model.md
│	 ├── plan.md
│	 ├── quickstart.md
│	 ├── research.md
│	 └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

research.mdで技術スタックが指示通りか確認し、必要ならAIに修正・調査させましょう。

新しい技術の場合はAIに更なる調査タスクを分割・並列化して指示できます。

> [!NOTE]
> Claude Codeが不要な要素を加えた場合は、理由や変更源を確認しましょう。

### **STEP 4:** 計画の検証

AIに計画や詳細ファイルを監査させ、不足がないか確認しましょう。例：

```text
実装計画と詳細を監査し、やるべきタスクに抜け漏れがないか確認してください。特にコア実装や洗練プロセスの各ステップがどこに書かれているかも明示してください。
```

抜けや過剰設計がないかもクロスチェックさせましょう。

### STEP 5: 実装

準備ができたらAIに実装を指示します（例：）

```text
implement specs/002-create-taskify/plan.md
```

AIが自動で実装を進めます。

> [!IMPORTANT]
> AIはローカルCLI（例：dotnet）を実行します。必要なツールはあらかじめインストールしてください。

実装後はアプリを動かし、ビルド・ランタイムエラーがあればAIに解決させましょう。

</details>

---

## 🔍 トラブルシューティング

### LinuxでのGit Credential Manager

LinuxでGit認証に問題がある場合、以下でGit Credential Managerをインストールできます：

```bash
#!/usr/bin/env bash
set -e
echo "Git Credential Manager v2.6.1をダウンロード中..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Git Credential Managerをインストール中..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "GitでGCMを設定中..."
git config --global credential.helper manager
echo "後始末中..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 メンテナー

- Den Delimarsky（[@localden](https://github.com/localden)）
- John Lam（[@jflam](https://github.com/jflam)）

## 💬 サポート

サポートは[GitHub Issue](https://github.com/github/spec-kit/issues/new)からお願いします。バグ報告、機能要望、Spec-Driven Developmentの利用相談など歓迎します。

## 🙏 謝辞

本プロジェクトは[John Lam](https://github.com/jflam)の研究と成果に多大な影響を受けています。

## 📄 ライセンス

本プロジェクトはMITオープンソースライセンスの下で公開されています。詳細は[LICENSE](./LICENSE)をご参照ください。