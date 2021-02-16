# Converting VIS json label to VOS format

## Usage
* Move `instances.json` from [VIS dataset](https://youtube-vos.org/dataset/vis/#data-download) to the same folder. 
* Prepare video name list to be converted or set `SUBSET` to false
* Call `python convert.py`

## Dependencies

```bash
conda install pillow
pip install git+https://github.com/youtubevos/cocoapi.git#"egg=pycocotools&subdirectory=PythonAPI"
```
