import requests


def upload_file():
    # 사용자로부터 파일 경로와 프로젝트 이름 입력받기
    file_path = input("Enter the path to the file you want to upload: ")
    project_name = input("Enter the project name: ")

    # API 엔드포인트 설정
    upload_url = "http://localhost:8000/api/projects/upload"

    try:
        # 파일 업로드 요청 보내기
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            data = {"project_name": project_name}
            response = requests.post(upload_url, files=files, data=data)

        # 응답 출력
        if response.status_code == 200:
            print("Upload successful:", response.json())
        else:
            print("Upload failed:", response.status_code, response.text)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    upload_file()
