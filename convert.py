import yaml
from pyhf.cli.rootio import json2xml
from pathlib import Path
import tempfile
import os
import ROOT, glob

def pyhf2hf(infile, outdir):
    json2xml.callback(infile, outdir, 'config', 'data', 'FitConfig', [])

def hf2ws(configdir):
    os.system(f'hist2workspace {configdir}/FitConfig.xml')

def ws2hs3(outfile, rootdir):
    infile = ROOT.TFile.Open(*glob.glob(f'{rootdir}/config/FitConfig_combined*.root'),"READ")
    ws = infile.Get("combined")
    tool = ROOT.RooJSONFactoryWSTool(ws)
    tool.exportJSON(outfile)

def pyhf2hs3(infile, outfile):
    with tempfile.TemporaryDirectory() as tmpdir:
        pyhf2hf(infile, tmpdir)
        hf2ws(tmpdir)
        ws2hs3(outfile, tmpdir)

def files_in_tree(path=Path('.')):
    for entry in path.iterdir():
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from files_in_tree(entry)

if __name__=="__main__":
    with open('links.yaml', 'r') as linkfile:
        links = yaml.load(linkfile, Loader=yaml.SafeLoader)

    ids = links.keys()
    basedirs = [Path(id) for id in ids]

    hs3dir = Path('hs3models/')
    hs3dir.mkdir(exist_ok=True)

    saved_models = []
    for dir in basedirs:
        for file in files_in_tree(dir):
            outfile = Path(str(file).replace(f'{dir}/', f'{hs3dir}/'))
            outfile.parent.mkdir(parents=True, exist_ok=True)
            try:
                pyhf2hs3(str(file), str(outfile))
                print(f'Processed {file}')
                saved_models.append(str(file))
            except:
                print(f'Not a model {file}')

    print(saved_models)