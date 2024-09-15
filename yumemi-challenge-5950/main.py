import csv
import os
import sys
from typing import List, Dict


def validate_entry_log(entry_log_path: str, entry_log_header: str) -> bool:
    """入力ファイルがエントリーファイルの仕様と同様か確認

    Args:
        entry_log_path (str): エントリーファイルパス
        entry_log_header (str): エントリーファイルのヘッダー

    Returns:
        bool: 照合結果
    """
        # 入力ファイルの存在確認
    if not os.path.exists(entry_log_path):
        print("ゲームのエントリーファイルが存在しません。", file=sys.stderr)
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
        # 入力ファイルの存在確認
    if not os.path.exists(score_log_path):
        print("ゲームのプレイログファイルが存在しません。", file=sys.stderr)
        return False
    
    return True


def generate_entry_data(entry_log_path: str) -> Dict[str, str]:
    """エントリーファイルを辞書に格納

    Args:
        entry_log_path (str): エントリーファイルパス

    Returns:
        Dict[str,str]: エントリーデータ
    """
    entry_data = {}

    # エントリーファイルを開く
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        csv_reader = csv.reader(entry_file)
        next(csv_reader) # ヘッダーをスキップ

        # 各行を辞書に格納
        for row in csv_reader:
            player_id = row[0]
            handle_name = row[1]
            entry_data[player_id] = handle_name
    
    return entry_data


def generate_score_data(
    score_log_path: str, entry_data: Dict[str, str]
) -> Dict[str, List[str]]:
    """プレイログファイルを配列に格納

    Args:
        score_log_path (str): プレイログファイルパス
        entry_data (Dict[str,str]): エントリーデータ

    Returns:
        Dict[str,List[str]]: プレイログデータ
    """
    score_data = {}

    with open(score_log_path, mode="r", encoding="utf-8") as score_file:
        csv_reader = csv.reader(score_file)
        next(csv_reader)

        for row in csv_reader:
            create_timestamp = row[0]
            player_id = row[1]
            game_score = int(row[2])

            # エントリ―データにプレイヤーIDがなければ記録しない。
            if player_id not in entry_data.keys():
                continue

            # 既にスコアがあれば比較･更新し、無ければ追加する。
            if player_id not in score_data.keys() or game_score > score_data[player_id][1]:
                score_data[player_id] = [create_timestamp, game_score]

    return score_data


def sort_score_data(score_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """プレイログデータをスコア降順、プレイヤーID昇順でソートする

    Args:
        score_data (Dict[str,List[str]]): スコアリスト

    Returns:
        Dict[str,List[str]]: ソート後のスコアリスト
    """
    return dict(sorted(score_data.items(), key=lambda item: (-int(item[1][1]), item[0])))


def extract_ranking_data(
entry_data: Dict[str, str], score_data: Dict[str, List[str]], ranking_threshold: int
) -> List[List[str]]:
    """ランキングデータの配列を作成する

    Args:
        entry_data (Dict[str,str]): エントリーデータ
        score_data (Dict[str,List[str]]): プレイログデータ

    Returns:
        Dict[str,List[str]]: ランキングデータ
    """
    ranking_data = []
    ranking_data_header = "rank,player_id,handle_name,score"
    rank = 0
    previous_score = None

    # ヘッダーを追加
    ranking_data.append(ranking_data_header.split(","))

    for player_id, score_item in score_data.items():
        score = int(score_item[1])
        rank += 1

        # スコアが変わっている場合は順位を変更
        if score != previous_score:
            print_rank = rank

        # ランキング圏外は処理しない
        if print_rank > ranking_threshold:
            break

        ranking_data.append([print_rank, player_id, entry_data[player_id], score])
        previous_score = score

    return ranking_data


def output_ranking_data(ranking_data: Dict[str, List[str]]):
    """結果を標準出力

    Args:
        ranking_data (Dict[str,List[str]]): ランキングデータ
    """
    for data in ranking_data:
        print(','.join(map(str, data)))


def main(entry_log_path: str, score_log_path: str):
    entry_log_header = "player_id,handle_name"
    score_log_header = "create_timestamp,player_id,score"
    RANKING_THRESHOLD = 10

    if not validate_entry_log(entry_log_path, entry_log_header):
        sys.exit(1)
    if not validate_score_log(score_log_path, score_log_header):
        sys.exit(1)
    entry_data = generate_entry_data(entry_log_path)
    score_data = generate_score_data(score_log_path, entry_data)
    score_data = sort_score_data(score_data)
    ranking_data = extract_ranking_data(entry_data, score_data, RANKING_THRESHOLD)
    output_ranking_data(ranking_data)


if __name__ == "__main__":
    # 引数の数が要件と一致しない場合はエラー出力
    if len(sys.argv) != 3:
        print("入力引数の数が不正です。", file=sys.stderr)
        sys.exit(1)

    entry_log_path = sys.argv[1]
    score_log_path = sys.argv[2]

    main(entry_log_path, score_log_path)
