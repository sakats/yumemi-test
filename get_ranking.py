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
    with open(entry_log_path, mode="r", encoding="utf-8") as entry_file:
        next(csv.reader(entry_file))
        entry_data = list(csv.reader(entry_file))
    return entry_data

def get_score_data(score_log_path: str, entry_data: list[list[str]]) -> list[list[str]]:
    """CSVファイルを配列データに加工
    """
    score_data=[]
    # エントリーデータからプレイヤ―IDを抽出
    entry_player_id = [row[0] for row in entry_data]
    
    with open(score_log_path, mode="r", encoding="utf-8") as score_file:
        csv_reader = csv.reader(score_file)
        next(csv_reader)
        for row in csv_reader:
            player_id = row[1]
            game_score = row[2]
            # エントリ―データにプレイヤーIDがなければ記録しない
            if player_id not in entry_player_id:
                continue
            # 既存のスコアがあれば比較して更新、なければ追加する
            for score in score_data:
                now_game_score = score[2]
                if player_id in score: 
                    if int(game_score) > int(now_game_score):
                        score_data.remove(score)
                        score_data.append(row)
                        break
                    else:
                        break
            else:
                score_data.append(row)
    return score_data

def sort_score_data(score_data: list[list[str]]) -> list[list[str]]:
    """データをスコア降順、記録時間昇順にソートする

    Args:
        score_data (list[list[str]]): スコアリスト

    Returns:
        list[list[str]]: ソート後のスコアリスト
    """
    # TODO:要件に合致したソート方法になっているか確認。現時点ではスコア同順は時間を優先。
    return sorted(score_data, key=lambda row: (-int(row[2]),row[0]))

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
    print(score_data)
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