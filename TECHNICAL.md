# Tài liệu mô tả kỹ thuật – SSRFTools (CloudSSRF)

Ngày cập nhật: 2026-02-22

## 1) Tổng quan
SSRFTools là một tool hỗ trợ kiểm thử/khai thác SSRF trong bối cảnh môi trường Cloud. Tool nhận vào một “raw HTTP request” (đã được bạn trích xuất từ proxy), sau đó **thay thế** một tham số (param) mục tiêu bằng các payload SSRF để:

- Quét dải mạng nội bộ (scanNet)
- Quét cổng (scanPort)
- Probe các endpoint/API phổ biến (scanAPI)
- Khai thác các endpoint metadata Cloud (exploitCloud)

## 2) Kiến trúc tổng thể
### 2.1 Luồng xử lý
1. `CloudSSRF.py` parse CLI arguments
2. `Utils/parseRequest.py` đọc request file → tách method/path/headers/body
3. Ghép URL mục tiêu: `{scheme}://{Host}{path}`
4. Nạp module theo `-m` bằng `importlib` → gọi `Module.<module>.run(...)`
5. Module thực thi scan/exploit bằng `httpx` (HTTP/2), sử dụng `Utils/makeRequest.py` để inject payload vào param
6. Kết quả in ra stdout (status code, đánh giá open/closed, response text/json tuỳ module)

### 2.2 Interface giữa entrypoint và module
Tất cả module trong `Module/` đều export hàm:

- `run(request_info, params, url)`

Trong đó `request_info` là tuple:

- `method`: `GET|POST|PUT`
- `api_path`: path gốc + query (nếu có) như trong request file
- `headers`: dict header
- `body`: dict body (JSON hoặc x-www-form-urlencoded đã parse)
- `is_json`: bool
- `verify`: bool (cấu hình TLS verify cho httpx)

`params` là tên tham số cần test SSRF (VD: `profilePicture`).

`url` là URL target đã ghép từ scheme/host/path (bỏ phần query từ request file).

## 3) Cấu trúc thư mục
- `CloudSSRF.py`: entrypoint CLI, load module
- `Module/`
  - `scanNet.py`: quét IP/CIDR nội bộ qua SSRF
  - `scanPort.py`: quét port trên một host/network qua SSRF
  - `scanAPI.py`: probe danh sách endpoint phổ biến
  - `exploitCloud.py`: thử endpoint metadata Cloud
- `Utils/`
  - `parseRequest.py`: parse raw request
  - `makeRequest.py`: inject payload vào param và gửi request
  - `runThread.py`: chạy concurrent workers (ThreadPoolExecutor + progress)
- `PayloadSSRF/`
  - `ApiTesting.txt`: danh sách endpoint để probe trong scanAPI
  - `ApiMetadata.json`: danh sách endpoint metadata theo cloud provider
- `request_exam.txt`: request mẫu
- `requirements.txt`: dependency

## 4) Đầu vào: format request file
File request phải theo format đơn giản:

- Dòng 1: `METHOD <path> HTTP/<version>` (ví dụ `PUT /api-v1/... HTTP/2`)
- Các dòng tiếp: header dạng `Key: Value`
- 1 dòng trống ngăn cách header và body
- Body có thể là:
  - JSON (ví dụ `{"profilePicture":"https://..."}`), hoặc
  - Form URL-encoded (ví dụ `a=1&b=2`)

Yêu cầu:
- Bắt buộc có header `Host`.
- `Content-Length` và `Accept-Encoding` sẽ bị bỏ qua khi parse (tool tự gửi lại request mà không cần 2 header này).

## 5) CLI & hành vi runtime
Ví dụ (theo README):

```bash
python CloudSSRF.py -f request_exam.txt -p profilePicture -s https -m scanNet
```

Tham số:
- `-f/--file`: đường dẫn request file
- `-p/--params`: param mục tiêu để thay payload SSRF
- `-s/--scheme`: `http` hoặc `https`
- `-m/--module`: `scanNet | scanPort | scanAPI | exploitCloud`


Ghi chú triển khai:
- Tool dựng URL theo `scheme://Host + api_path` nhưng **bỏ query**: `api_path.split('?')[0]`.
- Với `-s https`, biến `verify` hiện được set `False` (tức disable TLS verification). Điều này phù hợp cho lab/self-signed nhưng không an toàn nếu dùng ngoài môi trường kiểm thử.

## 6) Cách inject payload SSRF
Logic nằm tại `Utils/makeRequest.py`:
- Clone body dict → `body_data = body.copy()`
- Gán `body_data[params] = payload`

Gửi request theo method:
- `POST|PUT`:
  - Nếu JSON: gửi `json=body_data`
  - Nếu form: tự build string `k=v&...` và gửi `data=body_str`
- `GET`:
  - Gửi query param duy nhất `{params: payload}` (không merge với query cũ)

Nếu method khác `GET/POST/PUT` → raise `ValueError`.

## 7) Chi tiết module
### 7.1 Module scanNet
File: `Module/scanNet.py`

Mục tiêu: quét IP trong CIDR để suy luận khả năng truy cập network nội bộ từ vị trí SSRF.

Cách chạy:
- Tool hỏi input: `Target IP/CIDR (e.g., 192.168.0.1/20)`
- Dùng `ipaddress.ip_network(..., strict=False)` → list host
- Tạo payload: `http://<ip>`
- Gửi request với timeout 3 giây

Đánh giá kết quả (heuristic):
- `status_code == 200` → coi như open
- else:
  - nếu response chứa `ECONNREFUSED` → “open but connection refused”
  - còn lại → “closed/filtered”
- `httpx.RequestError` → coi như timeout

Concurrency:
- `Utils/runThread.run_threads()` mặc định `max_threads=40`.

### 7.2 Module scanPort
File: `Module/scanPort.py`

Mục tiêu: quét port trên một `network_target` (thường là hostname/IP nội bộ) bằng SSRF.

Cách chạy:
- Tool hỏi input:
  - `Network to scan:` (ví dụ `127.0.0.1` hoặc `10.0.0.5`)
  - `Ports:` nhận một trong:
    - `80`
    - `80,443,8080`
    - `1-1024`

Payload: `http://<network_target>:<port>`

Kết quả:
- `status_code == 200` → “Port open”
- else: in `response.text` và báo “closed/filtered”
- timeout → “closed by timeout”

### 7.3 Module scanAPI
File: `Module/scanAPI.py`

Mục tiêu: probe các path phổ biến (admin panels, actuator, docker API, k8s, v.v.) trên **chính host mục tiêu** bằng SSRF.

Dữ liệu:
- Đọc danh sách path từ `PayloadSSRF/ApiTesting.txt`.

Payload:
- `baseUrl = scheme://netloc` lấy từ URL mục tiêu
- `payload = baseUrl + api` (api là từng dòng path)

Kết quả:
- `status_code == 200` → “API accessible”
- else → “closed/filtered”
- timeout → “not accessible/exist by timeout”

### 7.4 Module exploitCloud
File: `Module/exploitCloud.py`

Mục tiêu: thử các endpoint metadata phổ biến của cloud provider.

Dữ liệu:
- Đọc `PayloadSSRF/ApiMetadata.json` (map provider → list endpoints)

Payload:
- `payload = "http://" + endpoint_cloud`

Header đặc thù:
- Nếu `cloud_env` chứa chuỗi `GCP` → thêm header `Metadata-Flavor: Google`

Luồng “bonus” khi status 200:
- In `response.json()`
- Lấy `API_exploit = response.json().get("data").get(params)`
- Gọi tiếp `GET {baseUrl}/{API_exploit}` với `headers=header`
- In status/text và báo “Successfully exploited...”

Lưu ý:
- Flow này giả định server trả JSON theo cấu trúc `{ data: { <param>: <path> } }` (phù hợp một số lab), không phải format chuẩn của mọi target.

## 8) Concurrency & hiệu năng
`Utils/runThread.py`:
- Dùng `ThreadPoolExecutor(max_workers=40)`
- Có progress bar dạng `completed/total` và %
- Mỗi task bắt exception và in `Thread error: ...` (không dừng toàn bộ tiến trình)

Timeout:
- Các module dùng `httpx.Client(..., timeout=3)` (giá trị cố định).

## 9) Dependency
`requirements.txt`:
- `httpx[http2]>=0.24.0` (sử dụng HTTP/2)

## 10) Mở rộng dự án
- Thêm module mới:
  1. Tạo file trong `Module/` (ví dụ `scanDns.py`) export `run(request_info, params, url)`
  2. Thêm tên module vào `choices=[...]` ở `CloudSSRF.py`
- Thêm payload:
  - scanAPI: bổ sung path vào `PayloadSSRF/ApiTesting.txt`
  - exploitCloud: bổ sung endpoint trong `PayloadSSRF/ApiMetadata.json`

## 11) Hạn chế hiện tại (theo code)
- Chỉ hỗ trợ method `GET`, `POST`, `PUT`.
- Với `GET`, tool không merge query param hiện hữu trong `api_path`.
- Inject param chỉ ở level 1 của JSON (không hỗ trợ nested object/array).
- TLS verify bị tắt khi chọn `https` (phù hợp lab, nhưng có rủi ro MITM nếu dùng thật).
- Timeout cố định 3 giây, không retry.

## 12) Lưu ý sử dụng
Tool phục vụ kiểm thử bảo mật. Chỉ sử dụng trên hệ thống bạn có quyền kiểm thử (được uỷ quyền). Quét mạng/port/API có thể gây ảnh hưởng hiệu năng hoặc tạo log/alert trên hệ thống.
