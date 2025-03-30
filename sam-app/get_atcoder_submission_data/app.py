import json
import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_atcoder_submissions(user_id, from_second):
    """AtCoderのAPIから提出履歴を取得"""
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={from_second}"
    try:
        logger.info(
            f"Fetching submissions for user {user_id} from {datetime.fromtimestamp(from_second)}")
        response = requests.get(url)
        response.raise_for_status()
        submissions = response.json()
        logger.info(f"Successfully retrieved {len(submissions)} submissions")
        return submissions
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None


def analyze_submissions(submissions):
    """提出データの分析"""
    if not submissions:
        logger.info("No submissions to analyze")
        return None

    analysis = {
        'total_submissions': len(submissions),
        'ac_count': 0,
        'unique_problems': set(),
        'languages_used': set(),
        'submissions_by_result': {},
        'contests': {}
    }

    for sub in submissions:
        # 結果の集計
        result = sub['result']
        analysis['submissions_by_result'][result] = analysis['submissions_by_result'].get(
            result, 0) + 1

        # コンテストごとの分析
        contest_id = sub['contest_id']
        if contest_id not in analysis['contests']:
            analysis['contests'][contest_id] = {
                'total_submissions': 0,
                'ac_count': 0,
                'unique_problems': set(),
                'submissions_by_result': {}
            }

        # コンテストごとの詳細を更新
        contest_data = analysis['contests'][contest_id]
        contest_data['total_submissions'] += 1
        contest_data['submissions_by_result'][result] = contest_data['submissions_by_result'].get(
            result, 0) + 1

        # AC（正解）の集計
        if result == 'AC':
            analysis['ac_count'] += 1
            problem_id = f"{sub['contest_id']}_{sub['problem_id']}"
            analysis['unique_problems'].add(problem_id)
            contest_data['ac_count'] += 1
            contest_data['unique_problems'].add(problem_id)

        # 使用言語の集計
        analysis['languages_used'].add(sub['language'])

    # setをリストに変換（JSON化のため）
    analysis['unique_problems'] = list(analysis['unique_problems'])
    analysis['languages_used'] = list(analysis['languages_used'])

    # コンテストデータのsetをリストに変換
    for contest_id in analysis['contests']:
        analysis['contests'][contest_id]['unique_problems'] = list(
            analysis['contests'][contest_id]['unique_problems']
        )

    logger.info(
        f"Analysis completed. Found submissions for {len(analysis['contests'])} contests")
    return analysis


def lambda_handler(event, context):
    try:
        logger.info("Starting lambda execution")
        one_week_ago = int((datetime.now() - timedelta(weeks=1)).timestamp())
        start_date = datetime.fromtimestamp(one_week_ago)
        end_date = datetime.now()

        submissions = get_atcoder_submissions('ZawaP', one_week_ago)

        if submissions is None or len(submissions) == 0:
            logger.info("No submissions found for the past week")
            message = f"先週は提出がなかったみたい。今週は1問解いてみよう。\n\n{start_date} ~ {end_date}"
            return {
                'statusCode': 200,
                'body': json.dumps(message)
            }

        analysis = analyze_submissions(submissions)

        if analysis is None:
            logger.error("Failed to analyze submissions")
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to analyze submissions')
            }

        response = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis
        }

        logger.info("Successfully completed analysis")
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
