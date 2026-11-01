import json
import urllib.request
import urllib.error

questions = [
    "where do I get my exam hall ticket",
    "can I pay tuition in parts",
    "mess food timing",
    "how many books can I issue",
    "which companies come for recruitment",
    "documents needed to join college",
    "what is the weather today",
    ""
]

print("="*60)
print("TESTING COLLEGE FAQ CLASSIFIER")
print("="*60)

for q in questions:
    data = json.dumps({"question": q}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/classify",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"\nQuestion: \"{q}\"")
            print(f"  Category:   {res['category']} ({res['title']})")
            print(f"  Confidence: {res['confidence']*100:.1f}% (Confident: {res['confident']})")
            print(f"  Department: {res['department']}")
            print(f"  Contact:    {res['contact']}")
            print(f"  Answer:     {res['answer']}")
    except urllib.error.HTTPError as e:
        print(f"\nQuestion: \"{q}\"")
        print(f"  Error {e.code}: {e.read().decode('utf-8').strip()}")
print("\n" + "="*60)
