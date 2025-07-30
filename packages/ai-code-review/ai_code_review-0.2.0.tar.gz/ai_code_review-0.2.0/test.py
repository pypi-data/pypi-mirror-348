import textwrap

import microcore as mc
import ai_code_review
from rich.pretty import pprint
def q():
    issues = mc.storage.read_json("code_review.json")["issues"]
    post_process = textwrap.dedent("""
# Remove issues with confidence + severity > 3
for fn in issues: issues[fn] = [i for i in issues[fn] if i["confidence"] + i["severity"] <= 3]
    """)
    exec(post_process, {**globals(), **locals()})
    pprint(issues)
q()