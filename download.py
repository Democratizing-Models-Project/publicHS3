import yaml
import pyhf
import pyhf.contrib.utils
from pathlib import Path

if __name__=="__main__":
    with open('links.yaml', 'r') as linkfile:
        links = yaml.load(linkfile, Loader=yaml.SafeLoader)

    ids = links.keys()
    basedirs = [Path(id) for id in ids]

    for id, dir in zip(ids, basedirs):
        dir.mkdir(exist_ok=True)
        for link in links[id]:
            outdir = dir / link.split('/')[-2]
            print(f'Downloading {link}')
            pyhf.contrib.utils.download(link, outdir)