import os, sys

good = os.getenv("GOOD_HASH")
bad = os.getenv("BAD_HASH", "HEAD")

if not good:
    print("GOOD_HASH manquant (définis-le dans le workflow).", file=sys.stderr)
    sys.exit(2)

os.system("git bisect reset || true")
rc = os.system(f"git bisect start {bad} {good}")
if rc != 0:
    sys.exit(rc)

rc = os.system("git bisect run sh -c 'python manage.py test || exit 1'")
os.system("git bisect reset")
sys.exit(0 if rc == 0 else 1)
