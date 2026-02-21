# SSRFTools

Tool SSRF phục vụ chính cho việc khai thác SSRF trên Cloud

## Cài đặt tools

```bash
git clone <repo-url>
cd SSRFTools
pip install -r requirements.txt
```

## Chạy tools

```bash
python CloudSSRF.py -f request_exam.txt -p profilePicture -s https -o scanNet
```

Tham số:

- `-f`: file raw request
- `-p`: param cần test SSRF
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
