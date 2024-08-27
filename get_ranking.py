import os
import sys

def check_import_file(entry_log_path: str, score_log_path: str):
    """ログファイルの仕様と入力ファイルに差異がないか確認

    Args:
        game_entry_log_path (str): _description_
        game_score_log_path (str): _description_
    """
    # TODO:入力ファイルの形式チェック
    pass

def get_entry_data(ENTRY_LOG_PATH: str) -> list[str]:
    """CSVファイルを配列データに加工
    """
    pass

def get_score_data(SCORE_LOG_PATH: str, entry_data: str) -> list[str]:
    """CSVファイルを配列データに加工
    """
    pass

def sort_score_data(score_data: list[str]) -> list[str]:
    """データをランキング形式にソートする

    Args:
        score_data (list[str]): _description_
    """
    pass

def extract_ranking_data(entry_data: list[str], score_data: list[str]) -> list[str]:
    """ランキングデータを上位10位以内の形式に加工する

    Args:
        entry_data (list[str]): _description_
        score_data (list[str]): _description_
    """
    pass

def output_ranking_data(ranking_data: str):
    """結果を標準出力

    Args:
        ranking_data (str): _description_
    """
    pass

def main(ENTRY_LOG_PATH: str, SCORE_LOG_PATH: str):
    # 入力ファイルの存在確認
    if not os.path.exists(ENTRY_LOG_PATH) or not os.path.exists(ENTRY_LOG_PATH):
        print("入力ファイルが存在しません。", file=sys.stderr)
        sys.exit(1)
    
    check_import_file(ENTRY_LOG_PATH, SCORE_LOG_PATH)
    entry_data = get_entry_data(ENTRY_LOG_PATH)
    score_data = get_score_data(SCORE_LOG_PATH, entry_data)
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