import os

# NOTE: None of this should be necessary if you start out with Anaconda - it includes the basics!
packages = ['--upgrade pip', '-U pip setuptools', 'numpy', 'pandas', 'xlrd', 'matplotlib', 'statsmodels', 'wheel',
            'scipy', 'patsy', 'keras', 'seaborn', 'scikit-learn']

# SOMEDAY: "QuickFIX" (requires Visual C++ 9.0

for p in packages:
    if os.name == 'nt':
        os.system("c:\Python27\python -m pip install " + p)  # for Windows
    else:
        os.system("pip install " + p)  # for Mac / Linux

print "Setup complete!"
