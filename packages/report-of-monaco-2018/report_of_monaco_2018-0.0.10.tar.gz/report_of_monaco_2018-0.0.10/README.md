# 🏎️ Application to create Formula 1 Report
   This tool can build a Formula 1 report. It works from CLI and you from import in your code.
The app reads and analyzes some files from a passing directory in CLI (read data by default package),
   or you can import it in your code and pass your own files  

---
## Installation 

Report-of-monaco-2018 can be installed by running
``` bash $
pip install report-of-monaco-2018==0.0.10
```


## 💻 Run from CLI 
You can use this package to run it from CLI and receive a report by default this command:
 
`report-monaco` - you can pass optional ` --asc | --desc ` to sort it;

or you can choose some driver and receive a result by him:

`report-monaco --file --driver 'Sebastian Vettel'` 

## 💻 Import in your project
You can import this package in your code and pass your own files:

```
import report_of_monaco_2018

report_of_monaco_2018.race_report()
```
After import, you should pass a path to directory with files to read, to cli



## Options flag:
 - `--file` - directory with files to read
 - `--desc` or `--asc` - sort report
 - `--driver`  - show info for a specific driver


## 📁 Requirements to directory
`abbreviations.txt`: contains driver abbreviations, full names, and team names.
`start.log`: contains timestamps of when each driver's start race.
`end.log`: contains timestamps of when each driver's end race.

### Example entry for start.log and end.log files:
SVF2018-05-24_12:02:58.917

- `SVF`: Driver abbreviation  
- `2018-05-24`: Date  
- `12:02:58.917`: Start or end time (used for lap duration calculation)

---
### Example entry for abbreviations.txt:
DRR_Daniel Riccardo_RED BULL RACING TAG HEUER

- `DRR`:  Driver abbreviation 
- `Daniel Riccardo`: Driver name
- `RED BULL RACING TAG HEUER`: Driver team

## 🏁 Report print Example

After parsing and calculating lap times, the output will look like:

```
1. Daniel Ricciardo      | RED BULL RACING TAG HEUER     | 1:12.013

2. Sebastian Vettel      | FERRARI                       | 1:12.415

3. ...

------------------------------------------------------------------------

16. Brendon Hartley   | SCUDERIA TORO ROSSO HONDA         | 1:13.179

17. Marcus Ericsson  | SAUBER FERRARI                     | 1:13.265

```



### License
MIT


