import socket
import os
import time

READ_BUFFER_SIZE = 1024

HOST = "localhost"
PORT = 80


def getInfomation(directory):
    file_list = []
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory, i))
        file_list.append([i, time.ctime(a.st_atime), a.st_size])
    return file_list


def serverSocket(server):
    while True:

        # Chấp nhận kết nối
        (conn, addr) = server.accept()

        request = conn.recv(READ_BUFFER_SIZE).decode("utf8")
        print(request)

        # Phân tích các yêu cầu của client bằng " "
        file_part = request.split(" ")

        # Xử lý request của client
        method = file_part[0]
        request_file = file_part[1]

        # Phân tích file
        out_file = request_file.lstrip("/")

        # Nếu file request trống thì sẽ trả về file index.html
        if(out_file == ""):
            out_file = ("index.html")

        if (method == "POST"):
            accuracy = request.split("\n")[-1]
            print(accuracy)

            # Kiểm tra username và password
            if('{"username":"admin","password":"admin"}' in accuracy):
                buffer = ("HTTP/1.1 200 OK\n")
                buffer += ("Content-type: text/json\n")
                buffer += ("\n")
                buffer += ('{ "login": "passed" }')
                conn.send(buffer.encode("utf8"))

            else:
                buffer = ("HTTP/1.1 200 OK\n")
                buffer += ("Content-type: text/json\n")
                buffer += ("\n")
                buffer += ('{ "login": "failed" }')
                conn.send(buffer.encode("utf8"))

        else:
            file = open(out_file, "rb")
            res = file.read()

            if(out_file.endswith(".png")):
                mimetype = "image/png"
            elif(out_file.endswith(".css")):
                mimetype = "text/css"
            elif(out_file.endswith(".jpg")):
                mimetype = "image/jpg"
            elif(out_file.endswith(".html")):
                mimetype = "text/html"
            elif(out_file.endswith(".mp3")):
                mimetype = "video/mp3"
            elif(out_file.endswith(".txt")):
                mimetype = "text/plain"
            elif(out_file.endswith(".webm")):
                mimetype = "audio/webm"
            elif(out_file.endswith(".pdf")):
                mimetype = "application/pdf"
            else:
                mimetype = "image/vnd.microsoft.ico"

            buffer = ("HTTP/1.1 200 OK\n")

            if ((method == "GET") and ("/download" in request_file)):
                buffer += ("Transfer Encoding: " 'chunked\n')

            buffer += "Content-Type: "
            buffer += mimetype
            buffer += "\n\n"

            print(buffer)
            end = buffer.encode("utf-8")
            end += res
            conn.send(end)

            file.close()

        # Đóng socket
        conn.close()


if __name__ == "__main__":
    try:

        # Tạo socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket listening on port", PORT)

    # Nếu không khởi tạo được thì sẽ in ra lỗi
    except socket.error as err:
        print("Socket creation failed with error %s" % (err))

    # Bind tại địa chỉ host và port
    server.bind((HOST, PORT))

    # Lắng nghe client request
    server.listen(1)

    serverSocket(server)
