# Trackmate-Data-Processing
 Intended to extract, compile, and filter velocity/displacement/distance data from many Fiji's TrackMate results files at once

1. Run TrackMate on Fiji, export Tracks result csv file on Display options page
2. Save each results file in separate folder within directory
3. Run python script which will filter out tracks under 10 or 20sec durations, extract desired metric, and compile in new excel file in the same directory