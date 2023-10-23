# Birth Names Software


Software reads in 3 csv files (Alberta, New Brunswick, Nova Scotia) and analyzes their data.


## Requirements

* Linux Server with Python 3 installed (Preferably University of Guelph SoCS server)
* pandas library
* matplot library
* ethnicolr library

## Installation

Install **pandas** using pip in command line: 

```bash
pip3 install pandas
```

Install **matplot** using pip in command line:

```bash
pip3 install matplot
```

Install **ethnicolr** using pip in command line: 

```bash
pip3 install ethnicolr
```

**\**NOTE**\*\*

*Libraries may take a long time to install*

## How To Run Program

Alberta CSV File Formatter:

```bash
./albertaNames.py -i baby-names-frequency_1980_2020.csv -o albertaOut
```

Main Program:

```bash
./main.py
```

**\**NOTE**\*\*

* May take a few seconds (Don't back out of program when it is loading)
* Ignore the follwing warning when you run the program:


I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 AVX512F FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2023-04-09 20:44:17.132545: W tensorflow/compiler/xla/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2023-04-09 20:44:17.132678: I tensorflow/compiler/xla/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2023-04-09 20:44:23.523293: W tensorflow/compiler/xla/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libnvinfer.so.7'; dlerror: libnvinfer.so.7: cannot open shared object file: No such file or directory
2023-04-09 20:44:23.524807: W tensorflow/compiler/xla/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libnvinfer_plugin.so.7'; dlerror: libnvinfer_plugin.so.7: cannot open shared object file: No such file or directory
2023-04-09 20:44:23.524844: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Cannot dlopen some TensorRT libraries. If you would like to use Nvidia GPU with TensorRT, please make sure the missing libraries mentioned above are installed properly.

## Contents of Zip File

**albertaNames.py**: Program to format and output source csv file for Alberta
**albertaOut.csv**: Formatted csv file for Alberta data
**baby-names-frequency_1980_2020**: Source csv file
**main.py**: Program to run the main software (The graph function will create a subfolder with the graph inside it based on the province selcted)
**NBOut.csv/NSOut.csv**: Formatted csv files for New Brunswick data and Nova Scotia

