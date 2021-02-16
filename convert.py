import os
import json
import numpy as np
from PIL import Image
from pycocotools.ytvos import YTVOS

SUBSET = True
if SUBSET:
  with open('videos.txt') as f:
    videos = set(f.read().splitlines())

ytvos = YTVOS('instances.json')
os.mkdir('Annotations')
meta = {"videos": {}}
palette = Image.open('palette.png').getpalette()
for vid in ytvos.getVidIds():
  video_name = ytvos.vids[vid]['file_names'][0][:10]
  if SUBSET and video_name not in videos:
    continue
  width = ytvos.vids[vid]['width']
  height = ytvos.vids[vid]['height']
  length = ytvos.vids[vid]['length']
  labels = [
      np.array(Image.new('P', (width, height), color=0)) for _ in range(length)
  ]
  frame_names = [f[11:16] for f in ytvos.vids[vid]['file_names']]
  meta_video = {"objects": {}}
  for ins, ann in enumerate(ytvos.vidToAnns[vid]):
    start_i = None
    for i in range(length):
      if ann['segmentations'][i] is not None:
        if start_i is None:
          start_i = i
        mask = ytvos.annToMask(ann, i)
        labels[i][mask == 1] = ins + 1
    meta_video["objects"][str(ins + 1)] = {
        "frames": frame_names[start_i:],
        "category": ytvos.cats[ann['category_id']]['name']
    }
  meta["videos"][video_name] = meta_video
  os.mkdir(os.path.join('Annotations', video_name))
  for frame_name, label in zip(frame_names, labels):
    im = Image.fromarray(label, 'P')
    im.putpalette(palette)
    im.save(os.path.join('Annotations', video_name, frame_name + '.png'))
with open('meta.json', 'w') as outfile:
  json.dump(meta, outfile, sort_keys=True, indent=4)
