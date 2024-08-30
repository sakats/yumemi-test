import os
import sys
import csv

def check_import_file(entry_log_path: str, score_log_path: str):
    """ログファイルの仕様と入力ファイルに差異がないか確認

    Args:
        game_entry_log_path (str): _description_
        game_score_log_path (str): _description_
    """
    # TODO:入力ファイルの形式チェック
    pass

def get_entry_data(entry_log_path: str) -> list[list[str]]:
    """CSVファイルを配列データに加工
    """
    entry_data = {}
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        next(csv.reader(entry_file))
        entry_data = list(csv.reader(entry_file))
    return entry_data

def get_score_data(score_log_path: str, entry_data: list[list[str]]) -> list[list[str]]:
    """CSVファイルを配列データに加工
    """
    pass

def sort_score_data(score_data: list[list[str]]) -> list[list[str]]:
    """データをランキング形式にソートする

    Args:
        score_data (list[list[str]]): _description_
    """
    pass

def extract_ranking_data(entry_data: list[list[str]], score_data: list[list[str]]) -> list[list[str]]:
    """ランキングデータを上位10位以内の形式に加工する

    Args:
        entry_data (list[list[str]]): _description_
        score_data (list[list[str]]): _description_
    """
    pass

def output_ranking_data(ranking_data: str):
    """結果を標準出力

    Args:
        ranking_data (str): _description_
    """
    pass

def main(entry_log_path: str, score_log_path: str):
    # 入力ファイルの存在確認
    if not os.path.exists(entry_log_path):
        print("ゲームのエントリーファイルが存在しません。", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(score_log_path):
        print("ゲームのプレイログファイルが存在しません。", file=sys.stderr)
        sys.exit(1)

    check_import_file(entry_log_path, score_log_path)
    entry_data = get_entry_data(entry_log_path)
    score_data = get_score_data(score_log_path, entry_data)
    score_data = sort_score_data(score_data)
    ranking_data = extract_ranking_data(entry_data, score_data)
    output_ranking_data(ranking_data)

if __name__ == "__main__":
    # 引数の数が2個ではない場合はエラー出力
    if len(sys.argv) != 3:
        print("入力引数の数が不正です。", file=sys.stderr)
        sys.exit(1)

    ENTRY_LOG_PATH = sys.argv[1]
    SCORE_LOG_PATH = sys.argv[2]

    main(ENTRY_LOG_PATH,SCORE_LOG_PATH)