import sys
import os
import shutil
import re
import subprocess
import yaml

def is_variable_modified(variable_name, line):
    pattern = rf'\b{variable_name}\b\s*(?:\.|\+=|-=|\*=|/=|=)'
    return re.search(pattern, line) is not None

def edit_and_save_python_file(file_path):
    # 絶対パスに変換
    abs_file_path = os.path.abspath(file_path) 

    # ファイルが存在するか確認
    if not os.path.isfile(abs_file_path):
        print(f"Error: {abs_file_path} は存在しません。")
        return

    try:
        # ファイルを行ごとに読み込み
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 編集結果を保存するリスト
        updated_lines = []
        modified_line = []
        variable_name_list = []
        used_name_list = []
        pvc_block_list = []  # # PVC のブロックを保存

        inside_function = False
        inside_pvc_block = False
        current_pvc_block = []

        # 各行を処理
        for line in lines:
            stripped_line = line.strip()

            # PVC ブロックの処理
            if inside_pvc_block:
                if stripped_line == "":  # 空行が出たらブロック終了
                    pvc_block_list.append("\n".join(current_pvc_block))
                    current_pvc_block = []
                    inside_pvc_block = False
                else:
                    current_pvc_block.append(stripped_line)
                continue

            if "# PVC" in stripped_line:
                inside_pvc_block = True
                continue

            # 関数の開始を検出
            if re.match(r"^def\s+\w+\s*\(", stripped_line):
                inside_function = True

            # 関数の外にいるかチェック
            if not inside_function:
                match = re.match(r"^(\w+)\s*=\s*(.+)", stripped_line)
                if match:
                    variable_name, value = match.groups()
                    variable_name_list.append(variable_name)
                    continue
            else:
                for search_name in variable_name_list:
                    if search_name in stripped_line:
                        if is_variable_modified(search_name, stripped_line):
                            if search_name not in used_name_list:
                                used_name_list.append(search_name)

            # 関数の終了を検出（簡易チェック）
            if inside_function and stripped_line == "":
                inside_function = False
        
        # 「# PVC」から空行までのブロックを抽出してused_name_listに追加    
        for block in pvc_block_list:
            for pvc in block.split("\n"):  # ここで改行ごとに分割
                match = re.match(r"^(\w+)\s*=\s*(.+)", pvc.strip())
                if match:
                    variable_name = match.group(1)
                    used_name_list.append(variable_name)                    
                    print(variable_name)
                    
        for line in lines:
            stripped_line = line
            
            for search_name in used_name_list:
                if search_name in stripped_line:
                    modified_line = re.sub(fr'\b{search_name}\b', f'p.{search_name}', stripped_line)
                    updated_lines.append(modified_line)
                    continue
                else:
                    # 元の行を保持
                    updated_lines.append(line)
                    continue
                
        # 1行目に "import persistentvals" を追加
        updated_lines.insert(0, "import persistentvals\n")
        updated_lines.insert(1, "p = persistentvals.PersistentVals('./test.dat')\n")

        # 保存先ディレクトリを設定
        build_dir = "build"
        shutil.rmtree(build_dir)
        os.makedirs(build_dir)  # buildフォルダを作成（既に存在している場合はスキップ）

        # 元のファイル名を取得し、buildフォルダ内に保存
        file_name = os.path.basename(abs_file_path)
        new_file_path = os.path.join(build_dir, file_name)

        # 編集後の内容を保存
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

        print(f"1行目に 'import persistentvals' を追加し、'{new_file_path}' に保存しました。")
                                
    except Exception as e:
        print(f"Error: {e}")

        
        
# def is_variable_modified(variable, line):
#     """
#     指定された行において、変数が変更されているかを判定する
#     """
#     # 代入演算子を含む場合
#     for op in modifying_operators:
#         if re.search(fr"\b{variable}\b\s*{op}", line):
#             return True

#     # メソッド呼び出しを含む場合
#     for method in modifying_methods:
#         if re.search(fr"\b{variable}\b\s*\.\s*{method}\s*\(", line):
#             return True

#     return False

def copy_auto_persistent(script_dir, file_dir, build_dir):
    # persistentvals.py を build フォルダにコピー
    persistentvals_path = os.path.join(script_dir, "persistentvals.py")
    dockerfile_path = os.path.join(file_dir, "Dockerfile")
    requirements_path = os.path.join(file_dir, "requirements.txt")

    if os.path.isfile(persistentvals_path):
        try:
            shutil.copy(persistentvals_path, build_dir)
            print(f"'auto_persistent.py' を '{build_dir}' にコピーしました。")
        except Exception as e:
            print(f"エラーが発生しました (auto_persistent.py コピー中): {e}")
    else:
        print(f"Warning: 'auto_persistent.py' が {script_dir} に存在しません。")
    
    if os.path.isfile(dockerfile_path):
        try:
            shutil.copy(dockerfile_path, build_dir)
            print(f"'Dockerfile' を '{build_dir}' にコピーしました。")
        except Exception as e:
            print(f"エラーが発生しました (Dockerfile コピー中): {e}")
    else:
        print(f"Warning: 'Dockerfile' が {file_dir} に存在しません。")
    
    if os.path.isfile(requirements_path):
        try:
            shutil.copy(requirements_path, build_dir)
            print(f"'requirements.txt' を '{build_dir}' にコピーしました。")
        except Exception as e:
            print(f"エラーが発生しました (requirements.txt コピー中): {e}")
    else:
        print(f"Warning: 'requirements.txt' が {file_dir} に存在しません。")

def update_yaml_template(template_path, output_path, **kwargs):
    # YAMLテンプレートを読み込む
    with open(template_path, 'r') as file:
        template = file.read()

    # 引数で受け取った内容をプレースホルダーに置き換える
    for key, value in kwargs.items():
        placeholder = f"{{{{{key}}}}}"  # プレースホルダー（例: {{name}}, {{age}}）
        template = template.replace(placeholder, str(value))
    print(template)
    # 置き換えた内容をYAMLとして保存する
    with open(output_path, 'w') as file:
        file.writelines(template)

if __name__ == "__main__":
    # コマンドライン引数を確認
    if len(sys.argv) != 5 and len(sys.argv) != 3:
        print("使い方: python auto_persistent.py build ファイルパス イメージ名 Kubernetesリソース名")
        sys.exit(1)
    if len(sys.argv) == 5 and sys.argv[1] == "build":
        # 引数を取得
        file_path = sys.argv[2]
        file_dir = os.path.dirname(os.path.abspath(file_path))
        
        # スクリプトのディレクトリを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 保存先ディレクトリを設定
        build_dir = os.path.join(script_dir, "build")
        os.makedirs(build_dir, exist_ok=True)

        # ファイルを編集して保存
        edit_and_save_python_file(file_path)

        # auto_persistent.py をコピー
        copy_auto_persistent(script_dir, file_dir, build_dir)

        image_name = sys.argv[3]
        res_name = sys.argv[4]
        try:
            print("ビルド開始")
            cmd = subprocess.run(['docker', 'build', '-t', image_name, './build/.'], encoding='utf-8', stdout=subprocess.PIPE, check=True)
            print("push開始")
            cmd = subprocess.run(['docker', 'push', image_name], encoding='utf-8', stdout=subprocess.PIPE, check=True)
            
            # 使用例
            update_yaml_template(
                'app.yaml',  # テンプレートYAMLファイル
                'build/app.yaml',    # 出力先のYAMLファイル
                name = res_name,
                image = image_name,
            )

        except subprocess.CalledProcessError as e:
            # 終了コードが0以外の場合、例外が発生
            print(e)
        
        print("クラスタへ適用")
        cmd = subprocess.run(['kubectl', 'apply', '-f', 'build/app.yaml'], encoding='utf-8', stdout=subprocess.PIPE)
    if len(sys.argv) == 3 and sys.argv[1] == "delete":
        res_name = sys.argv[2]
        print(f"{res_name}を削除します")
        subprocess.run(['kubectl', 'delete', 'deploy', res_name], encoding='utf-8', stdout=subprocess.PIPE)
        subprocess.run(['kubectl', 'delete', 'service', res_name], encoding='utf-8', stdout=subprocess.PIPE)
