import csv
import os
import sys
from typing import List, Dict

def check_import_file(entry_log_path: str, score_log_path: str):
    """ログファイルの仕様と入力ファイルに差異がないか確認

    Args:
        game_entry_log_path (str): _description_
        game_score_log_path (str): _description_
    """
    # TODO:入力ファイルの形式チェック
    pass

def generate_entry_data(entry_log_path: str) -> Dict[str,str]:
    """エントリーファイルを辞書に格納

    Args:
        entry_log_path (str): エントリーファイルパス

    Returns:
        Dict[str,str]: エントリーデータ
    """
    entry_data = {}
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        csv_reader = csv.reader(entry_file)
        next(csv_reader)
        for row in csv_reader:
            player_id = row[0]
            handle_name = row[1]
            entry_data[player_id] = handle_name
    return entry_data

def generate_score_data(score_log_path: str, entry_data: Dict[str,str]) -> Dict[str,List[str]]:
    """スコアファイルを配列に格納

    Args:
        score_log_path (str): スコアファイルパス
        entry_data (Dict[str,str]): エントリーデータ

    Returns:
        Dict[str,List[str]]: スコアデータ
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
            for score in score_data:
                best_score = int(score[2])
                if player_id in score and (player_id not in score_data.keys() or game_score > best_score):
                    score_data[player_id] = [create_timestamp,game_score]
                    break
    return score_data

def sort_score_data(score_data: List[List[str]]) -> List[List[str]]:
    """データをスコア降順、記録時間昇順にソートする

    Args:
        score_data (List[List[str]]): スコアリスト

    Returns:
        List[List[str]]: ソート後のスコアリスト
    """
    # TODO:要件に合致したソート方法になっているか確認。現時点ではスコア同順は時間を優先。
    return sorted(score_data, key=lambda row: (-int(row[2]),row[0]))

def extract_ranking_data(entry_data: List[List[str]], score_data: List[List[str]]) -> List[List[str]]:
    """ランキングデータを上位10位以内の形式に加工する

    Args:
        entry_data (List[List[str]]): エントリーデータ
        score_data (List[List[str]]): スコアデータ

    Returns:
        List[List[str]]: ランキングデータ
    """
    pass

def output_ranking_data(ranking_data: str):
    """結果を標準出力

    Args:
        ranking_data (str): ランキングデータ
    """
    for data in ranking_data:
        print(data)

def main(entry_log_path: str, score_log_path: str):
    entry_log_header = "player_id,handle_name"
    score_log_header = "create_timestamp,player_id,score"
    ranking_data_header = "rank,player_id,handle_name,score"

    # 入力ファイルの存在確認
    if not os.path.exists(entry_log_path):
        print("ゲームのエントリーファイルが存在しません。", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(score_log_path):
        print("ゲームのプレイログファイルが存在しません。", file=sys.stderr)
        sys.exit(1)

    # 入力ファイルの名前確認
    if os.path.basename(entry_log_path) != "game_entry_log.csv":
        print("エントリーファイルのファイル名または拡張子が異なります")
        sys.exit(1)
    if os.path.basename(score_log_path) != "game_score_log.csv":
        print("プレイログファイルのファイル名または拡張子が異なります")
        sys.exit(1)

    check_import_file(entry_log_path, score_log_path)
    entry_data = generate_entry_data(entry_log_path)
    score_data = generate_score_data(score_log_path, entry_data)
    score_data = sort_score_data(score_data)
    print(score_data)
    ranking_data = extract_ranking_data(entry_data, score_data)
    output_ranking_data(ranking_data)

if __name__ == "__main__":
    # 引数の数が2個ではない場合はエラー出力
    if len(sys.argv) != 3:
        print("入力引数の数が不正です。", file=sys.stderr)
        sys.exit(1)

    entry_log_path = sys.argv[1]
    score_log_path = sys.argv[2]

    main(entry_log_path,score_log_path)