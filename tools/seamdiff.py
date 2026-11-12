"""Dev helper: show where frame `op` differs from frame 0 (loop seam).

    python tools/seamdiff.py 115   -> /tmp/prev/<id>_seam.png
"""
import glob
import gzip
import json
import os
import sys

import numpy as np
from PIL import Image
from rlottie_python import LottieAnimation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for eid in sys.argv[1:]:
    path = glob.glob(os.path.join(ROOT, "dist", "tgs", eid + "_*.tgs"))[0]
    with gzip.open(path) as fh:
        data = json.loads(fh.read())
    n = int(data["op"])
    data["op"] = n + 1
    for layer in data["layers"]:
        layer["op"] = n + 1
    anim = LottieAnimation.from_data(json.dumps(data))
    a = np.asarray(anim.render_pillow_frame(frame_num=0, width=512, height=512)).astype(int)
    b = np.asarray(anim.render_pillow_frame(frame_num=n, width=512, height=512)).astype(int)
    d = np.abs(a - b).max(axis=2)
    ys, xs = np.nonzero(d > 24)
    print(eid, "max", d.max(), "bbox", (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None)
    vis = np.concatenate([a[:, :, :3], b[:, :, :3], np.stack([np.clip(d * 4, 0, 255)] * 3, axis=2)], axis=1)
    Image.fromarray(vis.astype(np.uint8)).save("/tmp/prev/%s_seam.png" % eid)
    for name in [l["nm"] for l in data["layers"]]:
        pass
