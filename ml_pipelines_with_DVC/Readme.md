# dvc commands 
git init 
dvc init 
dvc repro 
dvc dag 
dvc metrics show 


# build and track ML pipelines with DVC 
## how to run 

conda create -n test test python = 3.13 -y 
conda create test 
pip install -r requirements.txt 

## macOS xgboost fix

If `import xgboost` fails with `Library not loaded: @rpath/libomp.dylib`, run:

```bash
./fix_xgboost_macos.sh
```

The script installs a repo-local OpenMP runtime in `../.xgboost-runtime` and
patches the `xgboost` wheel inside `../.venv`.
