import csv
import os
import re
import sys
from datetime import datetime
from typing import List, Dict


def validate_entry_log(entry_log_path: str, entry_log_header: str) -> bool:
    """入力ファイルがエントリーファイルの仕様と同様か確認

    Args:
        entry_log_path (str): エントリーファイルパス
        entry_log_header (str): エントリーファイルのヘッダー

    Returns:
        bool: 照合結果
    """
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    regexp_format = r"^\w+$"

    # 入力ファイルの存在確認
    if not os.path.exists(entry_log_path):
        print("ゲームのエントリーファイルが存在しません。", file=sys.stderr)
        return False

    # ヘッダー確認と要素数の確認
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        csv_reader = csv.reader(entry_file)
        headers = next(csv_reader)
        if headers != entry_log_header.split(","):
            print("エントリーファイルのヘッダーが正しくありません。", file=sys.stderr)
            return False

        for row in csv_reader:
            if len(row) != len(headers):
                print("エントリーファイルの要素数が正しくありません。", file=sys.stderr)
                return False

            # タイムスタンプが正しいフォーマットか確認
            create_timestamp = row[0]
            try:
                datetime.strptime(create_timestamp, timestamp_format)
            except ValueError:
                print(
                    "エントリーファイルのcreate_timestamp列に不正な値が含まれています。",
                    file=sys.stderr,
                )
                return False

            # プレイヤーIDが正しいフォーマットか確認
            player_id = row[1]
            pattern = re.compile(regexp_format)
            if (
                len(player_id) <= 0
                or len(player_id) > 20
                or not pattern.match(player_id)
            ):
                print("プレイヤーIDに不正な文字列が含まれています。", file=sys.stderr)
                return False

            # ハンドルネームが正しいフォーマットか確認
            handle_name = row[2]
            pattern = re.compile(regexp_format)
            if (
                len(handle_name) <= 0
                or len(handle_name) > 20
                or not pattern.match(handle_name)
            ):
                print("ハンドルネームに不正な文字列が含まれています。", file=sys.stderr)
                return False

    return True


def validate_score_log(score_log_path: str, score_log_header: str) -> bool:
    """入力ファイルがプレイログファイルの仕様と同様か確認

    Args:
        score_log_path (str): エントリーファイルパス
        score_log_header (str): エントリーファイルのヘッダー

    Returns:
        bool: 照合結果
    """
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    regexp_format = r"^\w+$"

    # 入力ファイルの存在確認
    if not os.path.exists(score_log_path):
        print("ゲームのプレイログファイルが存在しません。", file=sys.stderr)
        return False

    # ヘッダー確認と要素数の確認
    with open(score_log_path, mode="r", encoding="utf-8") as score_file:
        csv_reader = csv.reader(score_file)
        headers = next(csv_reader)
        if headers != score_log_header.split(","):
            print("プレイログファイルのヘッダーが正しくありません。", file=sys.stderr)
            return False

        for row in csv_reader:
            if len(row) != len(headers):
                print("プレイログファイルの要素数が正しくありません。", file=sys.stderr)
                return False

            # タイムスタンプが正しいフォーマットか確認
            create_timestamp = row[0]
            try:
                datetime.strptime(create_timestamp, timestamp_format)
            except ValueError:
                print(
                    "プレイログファイルのcreate_timestamp列に不正な値が含まれています。",
                    file=sys.stderr,
                )
                return False

            # プレイヤーIDが正しいフォーマットか確認
            player_id = row[1]
            pattern = re.compile(regexp_format)
            if (
                len(player_id) <= 0
                or len(player_id) > 20
                or not pattern.match(player_id)
            ):
                print("プレイヤーIDに不正な文字列が含まれています。", file=sys.stderr)
                return False

            # スコアが正しいフォーマットか確認
            score = row[2]
            if not score.isdigit() or int(score) < 0:
                print(
                    "プレイログファイルのスコアに不正な値が含まれています。",
                    file=sys.stderr,
                )
                return False

    return True


def generate_entry_data(entry_log_path: str) -> Dict[str, List[str]]:
    """エントリーデータを生成

    Args:
        entry_log_path (str): エントリーファイルパス

    Returns:
        Dict[str, List[str]]: エントリーデータ
    """
    entry_data = {}

    # エントリーファイルを開く
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        csv_reader = csv.reader(entry_file)
        next(csv_reader)  # ヘッダーをスキップ

        # 各行を辞書に格納
        for row in csv_reader:
            entry_time = row[0]
            player_id = row[1]
            handle_name = row[2]
            # 既にエントリーしている場合はハンドルネームのみ更新
            if player_id in entry_data.keys():
                existing_entry_time = entry_data[player_id][0]
                entry_data[player_id] = [existing_entry_time, handle_name]
            else:
                entry_data[player_id] = [entry_time, handle_name]

    return entry_data


def generate_score_data(
    score_log_path: str, entry_data: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """プレイログデータを生成

    Args:
        score_log_path (str): プレイログファイルパス
        entry_data (Dict[str, List[str]]): エントリーデータ

    Returns:
        Dict[str,List[str]]: プレイログデータ
    """
    score_data = {}

    with open(score_log_path, mode="r", encoding="utf-8") as score_file:
        csv_reader = csv.reader(score_file)
        next(csv_reader)  # ヘッダーをスキップ

        # 各行を辞書に格納
        for row in csv_reader:
            create_timestamp = row[0]
            player_id = row[1]
            game_score = int(row[2])

            # エントリ―データにプレイヤーIDがなければ記録しない
            if player_id not in entry_data.keys():
                continue

            # エントリー日時より古いプレイログは集計しない
            entry_time = entry_data[player_id][0]
            if create_timestamp < entry_time:
                continue

            # 既存スコアがあればプレイ回数･最高スコア･合計スコア更新
            if player_id in score_data.keys():
                entry_time = entry_data[player_id][0]
                total_plays = score_data[player_id][1] + 1
                best_score = score_data[player_id][2]
                total_score = score_data[player_id][3] + game_score
                average_score = round(total_score / total_plays)
                # 最高スコアの更新
                if game_score > best_score:
                    best_score = game_score
            # 既存スコアがなければ新規追加
            else:
                entry_time = entry_data[player_id][0]
                total_plays = 1
                best_score = game_score
                total_score = game_score
                average_score = game_score
            # プレイログデータ更新
            score_data[player_id] = [
                entry_time,
                total_plays,
                best_score,
                total_score,
                average_score,
            ]

    return score_data


def extract_ranking_data(
    entry_data: Dict[str, List[str]],
    score_data: Dict[str, List[str]],
    aggregate_mode: str,
    lowest_play_times: int,
    ranking_threshold: int,
) -> List[List[str]]:
    """ランキングデータを作成する

    Args:
        entry_data (Dict[str, List[str]]): エントリーデータ
        score_data (Dict[str, List[str]]): プレイログデータ
        aggregate_mode (str): 集計モードを表す文字列
        lowest_play_times (int): average集計時の最低プレイ回数
        ranking_threshold (int): 出力するランキングの閾値

    Returns:
        List[List[str]]: ランキングデータ
    """
    ranking_data = []
    rank = 0
    previous_score = None
    ranking_data_header = "rank,player_id,handle_name,score"

    # ランキング集計(スコア降順、エントリー日時昇順、プレイヤーID昇順)
    if aggregate_mode == "highscore":
        score_data = dict(
            sorted(
                score_data.items(),
                key=lambda item: (-int(item[1][2]), item[1][0], item[0]),
            )
        )
    elif aggregate_mode == "average":
        # プレイ回数が指定回数に満たないユーザは集計しない
        score_data = {k: v for k, v in score_data.items() if v[1] >= lowest_play_times}
        score_data = dict(
            sorted(
                score_data.items(),
                key=lambda item: (-int(item[1][4]), item[1][0], item[0]),
            )
        )

    # ヘッダーを追加
    ranking_data.append(ranking_data_header.split(","))

    # 集計データを基にランキングデータ生成
    for player_id, score_item in score_data.items():
        if aggregate_mode == "highscore":
            score = int(score_item[2])
        elif aggregate_mode == "average":
            score = int(score_item[4])
        rank += 1

        # スコアが変わっている場合は順位を変更
        if score != previous_score:
            print_rank = rank

        # ランキング圏外は処理しない
        if print_rank > ranking_threshold:
            break

        # ランキングデータに格納
        handle_name = entry_data[player_id][1]
        ranking_data.append([print_rank, player_id, handle_name, score])
        previous_score = score

    return ranking_data


def output_ranking_data(ranking_data: Dict[str, List[str]]):
    """ランキングデータを標準出力

    Args:
        ranking_data (Dict[str,List[str]]): ランキングデータ
    """
    # 配列をCSV形式で出力
    for output_data in ranking_data:
        print(",".join(map(str, output_data)))


def main(aggregate_mode: str, entry_log_path: str, score_log_path: str):
    """eスポーツ大会のランキングを出力するプログラム

    Args:
        aggregate_mode (str): 集計モードを表す文字列
        entry_log_path (str): エントリーファイルパス
        score_log_path (str): プレイログファイルパス
    """
    entry_log_header = "create_timestamp,player_id,handle_name"
    score_log_header = "create_timestamp,player_id,score"
    LOWEST_PLAY_TIMES = 10  # average集計時の最低プレイ回数
    RANKING_THRESHOLD = 10  # 出力するランキングの閾値

    # 集計モードの確認
    if aggregate_mode not in ["highscore", "average"]:
        print("不正な集計モードが指定されています。", file=sys.stderr)
        sys.exit(1)

    # 入力ファイルのバリデーションチェック
    if not validate_entry_log(entry_log_path, entry_log_header):
        sys.exit(1)
    if not validate_score_log(score_log_path, score_log_header):
        sys.exit(1)

    # ファイルを辞書に格納
    entry_data = generate_entry_data(entry_log_path)
    score_data = generate_score_data(score_log_path, entry_data)

    # ランキングデータ作成
    ranking_data = extract_ranking_data(
        entry_data, score_data, aggregate_mode, LOWEST_PLAY_TIMES, RANKING_THRESHOLD
    )

    # ランキングデータ出力
    output_ranking_data(ranking_data)


if __name__ == "__main__":
    # 引数の数が要件と一致しない場合はエラー出力
    EXPECTED_ARG_COUNT = 4
    if len(sys.argv) != EXPECTED_ARG_COUNT:
        print("入力引数の数が不正です。", file=sys.stderr)
        sys.exit(1)

    aggregate_mode = sys.argv[1]
    entry_log_path = sys.argv[2]
    score_log_path = sys.argv[3]

    main(aggregate_mode, entry_log_path, score_log_path)
