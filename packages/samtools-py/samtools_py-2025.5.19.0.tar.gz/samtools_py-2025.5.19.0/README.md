# samtools-py
samtools python wrapper (Windows only)


## build wheel from scratch

1. init a msys2 venv using `msys2_venv --venv samtools`
1. run `samtools\bin\fish.ps1` to enter msys2
1. install samtools: `pacman -S mingw-w64-ucrt-x86_64-samtools`
1. remove python: `pacman -Rs mingw-w64-ucrt-x86_64-python` because it's not needed to run samtools
