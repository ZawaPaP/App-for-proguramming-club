import json
import requests
from datetime import datetime, timedelta


def get_atcoder_submissions(user_id, from_second):
    """AtCoderのAPIから提出履歴を取得"""
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={from_second}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # エラーチェック
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None


def analyze_submissions(submissions):
    """提出データの分析"""
    if not submissions:
        return None

    analysis = {
        'total_submissions': len(submissions),
        'ac_count': 0,
        'unique_problems': set(),
        'languages_used': set(),
        'submissions_by_result': {}
    }

    for sub in submissions:
        # 結果の集計
        result = sub['result']
        analysis['submissions_by_result'][result] = analysis['submissions_by_result'].get(
            result, 0) + 1

        # AC（正解）の集計
        if result == 'AC':
            analysis['ac_count'] += 1
            analysis['unique_problems'].add(
                f"{sub['contest_id']}_{sub['problem_id']}")

        # 使用言語の集計
        analysis['languages_used'].add(sub['language'])

    # setをリストに変換（JSON化のため）
    analysis['unique_problems'] = list(analysis['unique_problems'])
    analysis['languages_used'] = list(analysis['languages_used'])

    return analysis


def lambda_handler(event, context):
    try:
        # 1週間前からの時間を計算
        one_week_ago = int((datetime.now() - timedelta(weeks=1)).timestamp())

        # AtCoderのデータを取得
        submissions = get_atcoder_submissions('ZawaP', one_week_ago)

        if submissions is None:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to fetch AtCoder data')
            }

        # データを分析
        analysis = analyze_submissions(submissions)

        if analysis is None:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to analyze submissions')
            }

        return {
            'statusCode': 200,
            'body': json.dumps({
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
