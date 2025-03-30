# AtCoder Progress Tracker

AtCoder の進捗を定期的に Slack に通知するサーバーレスアプリケーション

### Phase 1: AtCoder の進捗を Slack に通知する機能 (実装中)

- [x] AtCoder API からの提出データ取得
  - 指定期間内の提出履歴取得
  - コンテストごとの提出データ集計
- [x] 基本的なデータ分析
  - 総提出数、AC 数のカウント
  - 使用言語の集計
  - コンテストごとの成績分析
- [x] EventBridge による定期実行（週次）
- [ ] 通知メッセージのフォーマット設計
  - コンテストごとの成績
  - 総提出数、AC 数
  - 解いた問題のリスト
- [ ] エラー通知の実装
- [ ] 通知テスト機能の追加

### Phase 2: ユーザー登録システム (次期実装)

- [ ] DynamoDB テーブルの作成
  ```json
  {
    "user_id": "string (Slack User ID)",
    "atcoder_id": "string",
    "slack_webhook_url": "string",
    "notification_interval": "string (CRON式)",
    "active": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
  ```
- [ ] API Endpoints
  - POST /users (ユーザー登録)
  - PUT /users/{user_id} (設定更新)
  - DELETE /users/{user_id} (登録解除)
  - GET /users/{user_id}/report (即時レポート取得)

### 将来の拡張機能

- 通知頻度のカスタマイズ
- 問題難易度別の分析
- 進捗グラフの生成

## アーキテクチャ

## セットアップ手順

1. 必要な AWS リソースのデプロイ

```bash
sam build
sam deploy --guided
```

2. Slack App の設定

- Incoming Webhook の作成
- 環境変数の設定

## 今後の開発予定

1. Slack Command 統合

- Slack 通知機能
- ユーザー登録 API
- 設定変更 API
- 即時レポート取得 API

2. 分析機能の拡張

   - 他の人のために問題のリンクを Slack メッセージに添付
   - コンテストごとのパフォーマンス分析
   - 問題難易度別の解答状況
   - 時系列での進捗グラフ

3. 通知のカスタマイズ
   - 通知頻度の柔軟な設定
   - 通知内容のテンプレート化
   - 条件付き通知の実装

## コントリビューション

プルリクエストは大歓迎です。大きな変更を加える場合は、まず issue を作成して変更内容を議論しましょう。
