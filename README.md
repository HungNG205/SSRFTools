# SSRFTools

Tool test SSRF đơn giản cho lab/pentest được ủy quyền.

## Cài đặt

```bash
git clone <repo-url>
cd SSRFTools
pip install -r requirements.txt
```

## Chạy

```bash
python CloudSSRF.py -f request_exam.txt -p profilePicture -s https -o scanNet
```

Tuỳ chọn: thêm `--rps 5` để giới hạn tổng request/s (0 = không giới hạn).

Tham số:

- `-f`: file raw HTTP request
- `-p`: param chứa URL cần test SSRF
- `-s`: `http` hoặc `https`
- `-o`: `scanNet` | `scanPort` | `scanAPI` | `exploitMetadata`

## Format request mẫu

```http
PUT /api-v1/api/user/update/avatar HTTP/2
Host: target.example.com
Content-Type: application/json

{"profilePicture":"https://example.com/avatar.jpg"}
```

Lưu ý: bắt buộc có `Host`, và tên param ở `-p` phải đúng với body/query thật.
