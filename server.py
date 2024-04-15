import socket
import os
import json
import math

#  10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
def floorArea(x):
    return math.floor(x)

#  方程式 rn = x における、r の値を計算する。
def nrootArea(n, x):
    return math.pow(x, 1/n)

# 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
def reverseArea(s):
    return s[::-1]

#  2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
def validAnagramArea(str1, str2):
    return sorted(str1) == sorted(str2)

#  文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
def sortArea(strArr):
    return sorted(strArr)

function_map = {
    'floorArea': floorArea,
    'nrootArea': nrootArea,
    'reverseArea': reverseArea,
    'validAnagramArea': validAnagramArea,
    'sortArea': sortArea

}

# UNIXソケットをストリームモードで作成します
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# このサーバが接続を待つUNIXソケットのパスを設定します
server_address = '/tmp/socket_file'

# 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）します
try:
    os.unlink(server_address)
# サーバアドレスが存在しない場合、例外を無視します
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

# サーバアドレスにソケットをバインド（接続）します
sock.bind(server_address)

# ソケットが接続要求を待機するようにします
sock.listen(1)

# 無限ループでクライアントからの接続を待ち続けます
try:
    while True:
        # クライアントからの接続を受け入れます
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    # JSONデータの解析
                    request_data = json.loads(data.decode('utf-8'))
                    print('Received:', request_data)
                    function_name = request_data['method']
                    params = request_data['params']
                    # ここで適切な応答を生成

                    if function_name in function_map:
                        # リストの引数を関数に渡す
                        if isinstance(params, list):
                            result = function_map[function_name](*params)
                            # 応答のフォーマット
                            response_data = {
                                "results": str(result),
                                "result_type": type(result).__name__,
                                "id": request_data.get('id', 0)  # IDがない場合はデフォルトで0
                            }
                        else:
                            response_data = {"error": "Invalid parameters type"}
                    else:
                        response_data = {"error": "Function not found"}

                    connection.sendall(json.dumps(response_data).encode('utf-8'))
                else:
                    break
        finally:
            connection.close()
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sock.close()
    print("Server closed.")

