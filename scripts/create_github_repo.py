import subprocess
import urllib.request
import json
import sys

print("=========================================================================")
print("  GITHUB REPOSITORY CREATION & PUSH - SIPANDU SMART CITY")
print("  Penyusun: Mutia Afif Ramadhani (24311124) | Dosen: Dr. Erliyan Redy Susanto, M.Kom")
print("=========================================================================\n")

# 1. Ambil token dari git credential manager
input_data = 'protocol=https\nhost=github.com\n\n'
p = subprocess.run(['git', 'credential', 'fill'], input=input_data, text=True, capture_output=True)

creds = {}
for line in p.stdout.splitlines():
    if '=' in line:
        k, v = line.split('=', 1)
        creds[k] = v

username = creds.get('username')
token = creds.get('password')

if not token:
    print("Gagal mengambil token GitHub dari Credential Manager.")
    sys.exit(1)

print(f"Menggunakan akun GitHub: {username}")

# 2. Cek apakah repository sudah ada atau buat baru
repo_name = "sipandu-smart-city"
check_url = f"https://api.github.com/repos/{username}/{repo_name}"

req = urllib.request.Request(check_url, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Antigravity-Agent'
})

repo_exists = False
try:
    with urllib.request.urlopen(req) as resp:
        if resp.status == 200:
            repo_exists = True
            print(f"Repository {repo_name} sudah ada di GitHub.")
except urllib.error.HTTPError as e:
    if e.code == 404:
        repo_exists = False
    else:
        print(f"Status cek repo: {e.code}")

if not repo_exists:
    print(f"Membuat repository publik baru: {username}/{repo_name}...")
    create_url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": repo_name,
        "description": "SIPANDU Smart City - Sistem Pengaduan dan Penanganan Infrastruktur Kota Terpadu Kota Bandar Lampung (UTS PPSI 2026 - Mutia Afif Ramadhani)",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": False
    }).encode('utf-8')

    req_create = urllib.request.Request(create_url, data=payload, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'Antigravity-Agent'
    })

    try:
        with urllib.request.urlopen(req_create) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Repository berhasil dibuat: {data['html_url']}")
    except urllib.error.HTTPError as e:
        print(f"Gagal membuat repository: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

print(f"Target Remote: https://github.com/{username}/{repo_name}.git")

