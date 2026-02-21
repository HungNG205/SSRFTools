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
Host: ssrflab.dpdns.org
Cookie: __Host-authjs.csrf-token=81c77277f50db01dfa7cd3c47246451e1f83a5a1534bc62eea1d8e17c06c6c49%7Ca6cf75ab481eed4e2ce5e70a40e6183d97906360f908a8c168c277833ffba786; __Secure-authjs.callback-url=https%3A%2F%2Fssrflab.dpdns.org%2F
Auth-Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5OTFkMTE2OTkzZTA3YWEwZWRkYTFkYSIsImlhdCI6MTc3MTE2OTAzMSwiZXhwIjoxNzczNzYxMDMxfQ.4sn07haRJ6zC884_U_vQvXxSuAD9nPyhTilyVZvdwr4
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: application/json, text/plain, */*
Content-Type: application/json
Origin: https://ssrflab.dpdns.org
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ssrflab.dpdns.org/settings
Priority: u=1, i

{"profilePicture":"https://statictuoitre.mediacdn.vn/thumb_w/640/2017/7-1512755474943.jpg"}
```

Lưu ý: bắt buộc có `Host`, và tên param ở `-p` phải đúng với body/query thật.
