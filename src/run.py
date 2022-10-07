import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        forwarded_allow_ips='*',
        proxy_headers=True,
        # root_path="",
    )

# uvicorn src.main:app --host 0.0.0.0 --port 4030 --proxy-headers --root-path /api/v2

# pip install psycopg2-binary
# pip install pydantic[email]